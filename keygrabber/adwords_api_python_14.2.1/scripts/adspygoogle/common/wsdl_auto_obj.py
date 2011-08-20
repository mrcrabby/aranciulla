#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Transforms type declarations from a set of WSDLs into a pickle dictionary."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import pickle
import sys
import urllib

from xml.sax import make_parser
from xml.sax import saxutils
from xml.sax.handler import feature_namespaces


def main(location, types_name, ops_name, api_targets, wsdl_url_function):
  """Loops through given WSDLs, saving a dictionary representation to a pickle.

  Args:
    location: str Path to output pickle to.
    types_name: str Filename of types output pickle.
    ops_name: str Filename of operations output pickle.
    api_targets: list A list of dictionaries providing information on WSDLs.
    wsdl_url_function: function Takes in a dictionary from api_targets and a
                       specific service name and returns a URL pointing to that
                       service's WSDL.
  """
  for filename in (types_name, ops_name):
    if os.path.exists(os.path.abspath(os.path.join(location, filename))):
      print '%s already exists... deleting.' % filename
      os.unlink(os.path.abspath(os.path.join(location, filename)))

  wsdl_type_map = {}
  wsdl_operation_map = {}
  content_handler = WsdlHandler()
  parser = make_parser()
  parser.setFeature(feature_namespaces, 0)
  parser.setContentHandler(content_handler)

  for target in api_targets:
    for wsdl_map in (wsdl_type_map, wsdl_operation_map):
      if not target['version'] in wsdl_map:
        wsdl_map[target['version']] = {}
    for service in target['services']:
      for wsdl_map in (wsdl_type_map, wsdl_operation_map):
        wsdl_map[target['version']][service] = {}
      content_handler.SetTypesDict(wsdl_type_map[target['version']][service])
      content_handler.SetOpsDict(wsdl_operation_map[target['version']][service])
      wsdl_loc = wsdl_url_function(target, service)
      parser.parse(urllib.urlopen(wsdl_loc))

  pickle.dump(wsdl_type_map, open(os.path.abspath(os.path.join(
      location, types_name)), 'w'))
  pickle.dump(wsdl_operation_map, open(os.path.abspath(os.path.join(
      location, ops_name)), 'w'))


class WsdlHandler(saxutils.DefaultHandler):

  """Parses WSDLs, extracting type definitions and operation details."""

  def __init__(self):
    """Inits a WsdlHandler object."""
    self._current_types_dict = None
    self._current_ops_dict = None
    self._xpath = []
    self._type = None
    self._type_name = None
    self._base_type = ''
    self._params = []
    self._is_array = False
    self._has_native_type = False
    self._generated_arrays = set()
    self._message_parts = {}
    self._operations = {}

  def SetTypesDict(self, types_dict):
    """Sets the dictionary to output types to.

    Args:
      types_dict: dict The target dictionary to output types to.
    """
    self._current_types_dict = types_dict

  def SetOpsDict(self, ops_dict):
    """Sets the dictionary to output operations to.

    Args:
      ops_dict: dict The target dictionary to output operations to.
    """
    self._current_ops_dict = ops_dict

  def HandleComplexStart(self, attrs):
    """Takes appropriate action upon finding an opening complex type XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    if attrs.has_key('name'):
      self._type = 'complex'
      self._type_name = attrs.get('name')

  def HandleComplexEnd(self):
    """Takes appropriate action upon finding an ending complex type XML tag."""
    if self._is_array:
      self._current_types_dict[self._type_name] = {
          'base_type': self._base_type,
          'soap_type': 'array'
      }
    else:
      self._current_types_dict[self._type_name] = {
          'base_type': self._base_type,
          'soap_type': 'complex',
          'has_native_type': self._has_native_type,
          'parameters': tuple(self._params)
      }

  def HandleSimpleStart(self, attrs):
    """Takes appropriate action upon finding an opening simple type XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    if attrs.has_key('name'):
      self._type = 'simple'
      self._type_name = attrs.get('name')

  def HandleSimpleEnd(self):
    """Takes appropriate action upon finding an ending simple type XML tag."""
    self._current_types_dict[self._type_name] = {
        'soap_type': 'simple',
        'base_type': self._base_type,
        'allowed_values': tuple(self._params)
    }

  def HandleRestrictionStart(self, attrs):
    """Takes appropriate action upon finding an opening restriction XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    if self._type == 'simple':
      self._base_type = attrs.get('base')
    elif self._type == 'complex':
      self._is_array = True

  def HandleEnumerationStart(self, attrs):
    """Takes appropriate action upon finding an opening enumeration XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    self._params.append(attrs.get('value'))

  def HandleAttributeStart(self, attrs):
    """Takes appropriate action upon finding an opening attribute XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    if attrs.has_key('wsdl:arrayType'):
      # Trim the trailing "[]" from the type by slicing off 2 characters.
      self._base_type = self.TrimNonstandardNamespace(attrs.get(
          'wsdl:arrayType')[:-2])
      self._is_array = True

  def HandleExtensionStart(self, attrs):
    """Takes appropriate action upon finding an opening extension XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    self._base_type = self.TrimNonstandardNamespace(attrs.get('base'))

  def HandleElementStart(self, attrs):
    """Takes appropriate action upon finding an opening element XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    # If this element can occur more than one time, we're going to treat it
    # as an array. Generate an array entry for it and change the element's
    # type to this new array type.
    if attrs.get('name') == 'type': self._has_native_type = True
    trim_type = self.TrimNonstandardNamespace(attrs.get('type'))
    if (attrs.has_key('maxOccurs') and
        (attrs.get('maxOccurs') == 'unbounded' or
         int(attrs.get('maxOccurs')) > 1)):
      self._generated_arrays.add(trim_type)
      self._params.append([attrs.get('name'), 'ArrayOf_%s' % '_'.join(
          trim_type.split(':'))])
    else:
      self._params.append([attrs.get('name'), trim_type])

  def HandleOperationStart(self, attrs):
    """Takes appropriate action upon finding an opening operation XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    if attrs.has_key('name'):
      self._type_name = attrs.get('name')

  def HandleOutputStart(self, attrs):
    """Takes appropriate action upon finding an opening output XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    self._operations[self._type_name] = attrs.get('name')

  def HandleMessageStart(self, attrs):
    """Takes appropriate action upon finding an opening message XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    self._type = 'message'
    self._type_name = attrs.get('name')

  def HandleMessageEnd(self):
    """Takes appropriate action upon finding an ending message XML tag."""
    if not self._type_name in self._message_parts:
      self._message_parts[self._type_name] = self._params

  def HandleMessagePartStart(self, attrs):
    """Takes appropriate action upon finding an opening message part XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    if attrs.has_key('type'):
      self._params.append(self.TrimNonstandardNamespace(attrs.get('type')),)
    elif attrs.has_key('element'):
      self._params.append(self.TrimNonstandardNamespace(attrs.get('element')),)

  def HandleTopLevelElementStart(self, attrs):
    """Takes appropriate action upon finding an opening top-level element tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    self._type = 'element'
    self._type_name = attrs.get('name')

  def HandleTopLevelElementEnd(self):
    """Takes appropriate action upon finding an ending top-level element tag."""
    self._message_parts[self._type_name] = self._params

  def HandleNestedElementStart(self, attrs):
    """Takes appropriate action upon finding an opening nested element XML tag.

    Args:
      attrs: Attributes The attributes set within this XML tag.
    """
    trim_type = self.TrimNonstandardNamespace(attrs.get('type'))
    if attrs.has_key('maxOccurs') and (attrs.get('maxOccurs') == 'unbounded' or
                                       int(attrs.get('maxOccurs')) > 1):
      self._generated_arrays.add(trim_type)
      self._params.append('ArrayOf_%s' % '_'.join(trim_type.split(':')))
    else:
      self._params.append(trim_type)

  def TrimNonstandardNamespace(self, xsi_type):
    """Removes namespaces from SOAP types except for 'xsd' and 'soapenc' prefix.

    Args:
      xsi_type: str The type to trim.
    Returns:
      str The trimmed SOAP type.
    """
    if (not (xsi_type.startswith('xsd') or xsi_type.startswith('soapenc'))
        and xsi_type.find(':') > -1):
      xsi_type = xsi_type[xsi_type.find(':') + 1:]
    return xsi_type

  def startElement(self, name, attrs):
    """Called every time an XML tag begins.

    Args:
      name: str The name of the XML tag.
      attrs: Attributes The attributes set within this XML tag.
    """
    self._xpath.append(self.TrimNonstandardNamespace(name))

    # Check to see if this is a top-level type definition.
    if (len(self._xpath) > 1 and self._xpath[-2] == 'types' or
        (len(self._xpath) > 2 and self._xpath[-3] == 'types' and
         self._xpath[-2] == 'schema')):
      if name == 'complexType':
        self.HandleComplexStart(attrs)
      elif name == 'simpleType':
        self.HandleSimpleStart(attrs)
      elif name == 'element':
        self.HandleTopLevelElementStart(attrs)
    # Check to see if this is within a top-level complexType definition.
    elif self._type == 'complex':
      if name == 'extension':
        self.HandleExtensionStart(attrs)
      elif name == 'element':
        self.HandleElementStart(attrs)
      elif name == 'attribute':
        self.HandleAttributeStart(attrs)
      elif name == 'restriction':
        self.HandleRestrictionStart(attrs)
    # Check to see if this is within a top-level simpleType definition.
    elif self._type == 'simple':
      if name == 'restriction':
        self.HandleRestrictionStart(attrs)
      elif name == 'enumeration':
        self.HandleEnumerationStart(attrs)
    # Check to see if this is within a top-level element definition.
    elif self._type == 'element':
      if name == 'element':
        self.HandleNestedElementStart(attrs)
    # Check to see if within the binding portion of the WSDL document.
    elif 'binding' in self._xpath:
      if name.endswith('output'):
        self.HandleOutputStart(attrs)
      elif name.endswith('operation'):
        self.HandleOperationStart(attrs)
    # Check for other tags that need to be parsed and do not match any of the
    # above criteria.
    elif name.endswith('message'):
      self.HandleMessageStart(attrs)
    elif self._type == 'message' and name.endswith('part'):
      self.HandleMessagePartStart(attrs)

  def endElement(self, name):
    """Called every time an XML tag ends.

    Args:
      name: str The name of the XML tag.
    """
    self._xpath.pop()

    if name == 'complexType' and self._type == 'complex':
      self.HandleComplexEnd()
    elif name == 'simpleType' and self._type == 'simple':
      self.HandleSimpleEnd()
    elif (name == 'element' and self._type == 'element' and not
          'element' in self._xpath):
      self.HandleTopLevelElementEnd()
    elif name.endswith('message') and not self._type is None:
      self.HandleMessageEnd()

    if ((name in ('complexType', 'simpleType') and
         self._type in ('complex', 'simple')) or
        (name == 'element' and self._type == 'element' and
         not 'element' in self._xpath)):
      self._type = None
      self._type_name = None
      self._base_type = ''
      self._params = []
      self._is_array = False
      self._has_native_type = False

    if name.endswith('message') or name.endswith('binding'):
      self._type = None
      self._type_name = None
      self._params = []

  def characters(self, content):
    """Handles characters not enclosed in XML tags.

    Args:
      content: str A single character found unenclosed in XML tags.
    """
    pass

  def endDocument(self):
    """Called every time a document has been fully parsed."""
    for xsi_type in self._generated_arrays:
      self._current_types_dict['ArrayOf_%s' % '_'.join(xsi_type.split(':'))] = {
          'base_type': xsi_type,
          'soap_type': 'array'
      }
    self._generated_arrays = set()

    for operation in self._operations:
      outputs = []
      for output in self._message_parts[self._operations[operation]]:
        if (output not in self._current_types_dict and not
            (output.startswith('xsd') or output.startswith('soapenc'))):
          # This type is not defined as a complex or simple type under the
          # wsdl:types definitions. This means it was defined as an element
          # under wsdl:types.
          outputs.append(self._message_parts[output])
        else:
          outputs.append(output)
      self._current_ops_dict[operation] = outputs

    self._message_parts = {}
    self._operations = {}
