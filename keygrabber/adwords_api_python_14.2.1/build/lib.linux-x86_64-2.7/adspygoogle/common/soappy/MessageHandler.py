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

"""Handler functions for outgoing and incoming messages."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import re
import types

from adspygoogle.common import Utils
from adspygoogle.common.Errors import MissingPackageError
from adspygoogle.common.soappy import MIN_SOAPPY_VERSION
from adspygoogle.common.soappy.HTTPTransportHandler import HTTPTransportHandler
try:
  import SOAPpy
except ImportError:
  msg = 'SOAPpy v%s or newer is required.' % MIN_SOAPPY_VERSION
  raise MissingPackageError(msg)
else:
  if (map(eval, SOAPpy.version.__version__.split('.')) <
      (list(map(eval, MIN_SOAPPY_VERSION.split('.'))))):
    msg = 'SOAPpy v%s or newer is required.' % MIN_SOAPPY_VERSION
    raise MissingPackageError(msg)


def GetServiceConnection(headers, config, url, http_proxy, is_jaxb_api):
  """Get SOAP service connection.

  Args:
    headers: dict Dictionary object with populated authentication
             credentials.
    config: dict Dictionary object with populated configuration values.
    url: str URL of the web service to call.
    http_proxy: str HTTP proxy to use.
    is_jaxb_api: bool Whether API uses JAXB.

  Returns:
    instance SOAPpy.SOAPProxy with set headers.
  """
  # Catch empty SOAP header elements and exclude them from request.
  full_headers = {}
  for key in headers:
    if headers[key]: full_headers[key] = headers[key]

  if is_jaxb_api or Utils.BoolTypeConvert(config['wsse']):
    headers = SOAPpy.Types.headerType({config['ns_target'][1]: full_headers})
    headers._setAttr('xmlns', config['ns_target'][0])
    service = SOAPpy.SOAPProxy(url, http_proxy=http_proxy, header=headers,
                               transport=HTTPTransportHandler)
    service.transport.data_injects = config['data_injects']
  elif Utils.BoolTypeConvert(config['force_data_inject']):
    service = SOAPpy.SOAPProxy(url, http_proxy=http_proxy, header=headers,
                               transport=HTTPTransportHandler)
    service.transport.data_injects = config['data_injects']
  else:
    headers = SOAPpy.Types.headerType(full_headers)
    service = SOAPpy.SOAPProxy(url, http_proxy=http_proxy, header=headers)
  service.config.dumpHeadersIn = 1
  service.config.dumpHeadersOut = 1
  service.config.dumpSOAPIn = 1
  service.config.dumpSOAPOut = 1

  # Turn off type information, since SOAPpy usually gets the types wrong.
  service.config.typed = 0

  # Turn on noroot, to skip including "SOAP-ENC:root" as part of the request.
  service.noroot = 1

  # Explicitly set the style of the namespace, otherwise will default to 1999.
  service.config.namespaceStyle = '2001'

  # Set up OAuth, if applicable.
  if 'oauth_enabled' in config and config['oauth_enabled']:
    service.transport.oauth_enabled = True
    service.transport.oauth_handler = config['oauth_handler']
    service.transport.oauth_credentials = config['oauth_credentials']

  return service


# TODO(api.jdilallo): Remove this function once all products use PackVarAsXml.
def PackDictAsXml(obj, key='', key_map=[], order=[], wrap_list=False):
  """Pack a Python dictionary object into an XML string.

  DEPRECATED. As of version 2.0.0, use PackVarAsXml instead.

  For example, an input in a form of "dct = {'ids': [12345, 67890]}", where
  "dct" is key and "{'ids': ['12345', '67890']}" is obj, the output will be
  "<dct><ids>12345</ids><ids>67890</ids></dct>".

  Args:
    obj: dict Python dictionary to pack.
    [optional]
    key: str Key that maps to this Python dictionary.
    key_map: dict Object key order map.
    order: list Order of sub keys for this Python dictionary.
    wrap_list: bool If True, wraps list into an extra layer (e.g.,
               "'ids': ['12345']"  becomes "<ids><ids>12345</ids></ids>"). If
               False, "'ids': ['12345']" becomes "<ids>12345</ids>".

  Returns:
    str XML snippet.
  """
  buf = xsi_type = ''
  has_native_type = False
  tmp_xsi_type, local_order, tmp_key_type_obj = ('', [], {})
  if isinstance(obj, dict):
    # Determine if the object is typed.
    for item in obj:
      if (item == 'xsi_type' or item == 'type' or item.find('.Type') > -1 or
          item.find('_Type') > -1):
        xsi_type = obj[item]
        if key not in key_map: continue
        for key_map_item in key_map[key]:
          if key_map_item['type'] != xsi_type and 'native_type' in key_map_item:
            xsi_type = key_map_item['type']
            has_native_type = True
    if key == 'operations' and xsi_type.find('Operation') < 0: xsi_type = ''
    # Step through each key/value pair in the dictionary and pack it.
    for sub_key in obj:
      if (not has_native_type and
          (sub_key == 'xsi_type' or sub_key == 'type' or
           sub_key.find('.Type') > -1 or sub_key.find('_Type') > -1) and
          not (sub_key == 'type' and 'xsi_type' in obj)):
        continue
      tmp_xsi_type, local_order, tmp_key_type_obj = ('', [], {})
      if key in key_map:
        if 'xsi_type' not in obj and 'type' not in obj:
          if not has_native_type:
            for key_type_obj in key_map[key]:
              if not key_type_obj['type']:
                tmp_xsi_type = ''
                local_order = key_type_obj['order']
        else:
          for key_type_obj in key_map[key]:
            if key_type_obj['type'] and xsi_type == key_type_obj['type']:
              tmp_xsi_type = key_type_obj['type']
              local_order = key_type_obj['order']
              break
            elif not key_type_obj['type']:
              tmp_key_type_obj = key_type_obj
        if tmp_key_type_obj:
          if tmp_key_type_obj['type'] is None:
            tmp_xsi_type = xsi_type
          else:
            tmp_xsi_type = tmp_key_type_obj['type']
          local_order = tmp_key_type_obj['order']
        else:
          if len(key_map[key]) == 1:
            tmp_xsi_type = key_map[key][0]['type']
            local_order = key_map[key][0]['order']
      else:
        local_order = ()
      buf += PackDictAsXml(obj[sub_key], sub_key, key_map, local_order,
                           wrap_list)
      if local_order and buf:
        pre_tags = re.split('(<.*?>)', buf)[1:-1]
        if not pre_tags: return '<%s/>' % key
        tag_name = pre_tags[0][1:-1]
        post_tags = []
        tag_buf = ''
        counter = 0
        for pre_tag in pre_tags:
          if not pre_tag: continue
          tag = ''
          if pre_tag[0] == '<' and pre_tag[-1] == '>':
            tag = re.findall('<(?:/|)(\w+).*(?:/|)>', pre_tag)
            if tag: tag = tag[0]
          if counter == 0: tag_name = tag
          tag_buf += pre_tag
          if tag and tag_name == tag:
            counter += 1
            if counter == 2 or pre_tag[-2] == '/':
              post_tags.append(tag_buf)
              tag_buf = ''
              counter = 0
        xml_elems = post_tags
        if (len(xml_elems) > 1 and len(local_order) > 1 and
            xml_elems[0][1:] != xml_elems[-1][1:-1]):
          tmp_buf = ''
          pre_tags = []
          for pre_tag in xml_elems:
            tags = re.findall('<(?:/|)(\w+).*(?:/|)>', pre_tag)
            if tags: pre_tags.append(tags[0])
          sub_local_order = []
          for tag_name in local_order:
            if tag_name in pre_tags: sub_local_order.append(tag_name)
          for tag_name in sub_local_order:
            for xml_elem in xml_elems:
              if xml_elem[0] != '<': xml_elem = '<%s' % xml_elem
              if xml_elem[-1] != '>': xml_elem = '%s>' % xml_elem
              if (xml_elem.find(tag_name, 1, len(tag_name) + 1) > -1 and
                  (xml_elem[len(tag_name) + 1] == ' ' or
                   xml_elem[len(tag_name) + 1] == '>')):
                tmp_buf += xml_elem
          if tmp_buf and len(tmp_buf) >= len(buf): buf = tmp_buf
    if xsi_type and len(obj.keys()) == 1:
      data = '<%s xsi3:type="%s"/>' % (key, xsi_type)
    elif xsi_type:
      data = '<%s xsi3:type="%s">%s</%s>' % (key, xsi_type, buf, key)
    else:
      if tmp_xsi_type: tmp_xsi_type = ' xsi3:type="%s"' % (tmp_xsi_type)
      if key:
        data = '<%s%s>%s</%s>' % (key, tmp_xsi_type, buf, key)
      else:
        data = buf
  elif isinstance(obj, list):
    for item in obj:
      buf += PackDictAsXml(item, key, key_map, order, wrap_list)
    if wrap_list:
      data = '<%s>%s</%s>' % (key, buf, key)
    else:
      data = buf
  else:
    if obj is None:
      data = '<%s xsi3:nil="true" />' % (key)
    else:
      obj = Utils.HtmlEscape(obj)
      if key:
        data = '<%s>%s</%s>' % (key, obj, key)
      else:
        data = obj
  return data


def _PackDictionaryAsXml(obj, xml_tag_name, wsdl_type_map, wrap_list, xsi_type):
  """Pack a Python dictionary object into an XML string.

  Args:
    obj: dict Python dictionary to pack.
    xml_tag_name: str The name of the XML tag that will house this dict.
    wsdl_type_map: dict Information on all WSDL-defined types.
    wrap_list: bool If true, wraps lists in an extra layer (e.g.,
               "'ids': ['12345']"  becomes "<ids><ids>12345</ids></ids>"). If
               False, "'ids': ['12345']" becomes "<ids>12345</ids>".
    xsi_type: str The WSDL-defined type of this object, if applicable.

  Returns:
    str An XML element representing the given dictionary.
  """
  buf = ''
  obj_copy = obj.copy()
  # See if this object specifies its xsi_type and, if so, override the xsi_type
  # given. This has to occur before the main packing loop to ensure that
  # elements which exist only in a specified subtype can be handled correctly.
  obj_contained_type, xsi_override_key = Utils.GetExplicitType(wsdl_type_map,
                                                               obj, xsi_type)
  if obj_contained_type:
    xsi_type = obj_contained_type
    del obj_copy[xsi_override_key]

  param_order = []
  if xsi_type in wsdl_type_map:
    param_order = Utils.GenParamOrder(wsdl_type_map, xsi_type)

  # Recursively pack this dictionary's elements. If there is a specified param
  # order, pack things in this order. After going through the parameters with
  # an ordering, pack anything that remains in no particular order.
  for parameter, param_type in param_order:
    if parameter in obj_copy:
      buf += PackVarAsXml(obj[parameter], parameter, wsdl_type_map, wrap_list,
                          param_type)
      del obj_copy[parameter]

  for key in obj_copy:
    buf += PackVarAsXml(obj[key], key, wsdl_type_map, wrap_list)

  if xsi_type:
    if obj_contained_type and len(obj.keys()) == 1:
      return '<%s xsi3:type="%s"/>' % (xml_tag_name, xsi_type)
    else:
      return '<%s xsi3:type="%s">%s</%s>' % (xml_tag_name, xsi_type, buf,
                                             xml_tag_name)
  else:
    return '<%s>%s</%s>' % (xml_tag_name, buf, xml_tag_name)


def _PackListAsXml(obj, xml_tag_name, wsdl_type_map, wrap_list, xsi_type):
  """Pack a Python list object into an XML string.

  For compatibility reasons, this does not pack an empty list into XML at all.

  Args:
    obj: list Python list to pack.
    xml_tag_name: str The name of the XML tag that will house this list.
    wsdl_type_map: dict Information on all WSDL-defined types.
    wrap_list: bool If true, wraps lists in an extra layer (e.g.,
               "'ids': ['12345']"  becomes "<ids><ids>12345</ids></ids>"). If
               False, "'ids': ['12345']" becomes "<ids>12345</ids>".
    xsi_type: str The WSDL-defined type of this object, if applicable.

  Returns:
    str An XML element representing the given list.
  """
  buf = ''
  base_xsi_type = xsi_type
  if not obj or all(value is None for value in obj):
    return buf
  if (xsi_type in wsdl_type_map and
      wsdl_type_map[xsi_type]['soap_type'] == 'array'):
    base_xsi_type = wsdl_type_map[xsi_type]['base_type']
  for item in obj:
    buf += PackVarAsXml(item, xml_tag_name, wsdl_type_map, wrap_list,
                        base_xsi_type)
  if wrap_list:
    if (xsi_type in wsdl_type_map and
        wsdl_type_map[xsi_type]['soap_type'] == 'array'):
      return '<%s xsi3:type="%s">%s</%s>' % (xml_tag_name, xsi_type, buf,
                                             xml_tag_name)
    else:
      return '<%s>%s</%s>' % (xml_tag_name, buf, xml_tag_name)
  else:
    return buf


def _PackStringAsXml(obj, xml_tag_name):
  """Pack a Python string into an XML string.

  Args:
    obj: str Python string to pack.
    xml_tag_name: str The name of the XML tag that will house this string.

  Returns:
    str An XML element representing the given string.
  """
  if obj is None:
    return '<%s xsi3:nil="true" />' % (xml_tag_name)
  else:
    obj = Utils.HtmlEscape(obj)
    if xml_tag_name:
      return '<%s>%s</%s>' % (xml_tag_name, obj, xml_tag_name)
    else:
      return obj


def PackVarAsXml(obj, xml_tag_name='', wsdl_type_map={}, wrap_list=False,
                 xsi_type=''):
  """Pack a Python object into an XML string.

  For example, an input in a form of "dct = {'ids': [12345, 67890]}", where
  "dct" is xml_tag_name and "{'ids': ['12345', '67890']}" is obj, the output
  will be "<dct><ids>12345</ids><ids>67890</ids></dct>".

  Args:
    obj: object Python object to pack.
    [optional]
    xml_tag_name: str Key that maps to this Python dictionary.
    wsdl_type_map: dict Object key order map.
    wrap_list: bool If True, wraps lists into an extra layer (e.g.,
               "'ids': ['12345']"  becomes "<ids><ids>12345</ids></ids>"). If
               False, "'ids': ['12345']" becomes "<ids>12345</ids>".
    xsi_type: str The WSDL-defined type of this object, if applicable.

  Returns:
    str An XML element representing the given object.
  """
  if isinstance(obj, dict):
    return _PackDictionaryAsXml(obj, xml_tag_name, wsdl_type_map, wrap_list,
                                xsi_type)
  elif isinstance(obj, list):
    return _PackListAsXml(obj, xml_tag_name, wsdl_type_map, wrap_list, xsi_type)
  else:
    return _PackStringAsXml(obj, xml_tag_name)


def SetRequestParams(config, method_name, params):
  """Set SOAP request parameters.

  Args:
    config: dict Dictionary object with populated configuration values.
    method_name: str API method name.
    params: list List of parameters to send to the API method.

  Returns:
    instance SOAPpy.Types.bodyType with set parameters.
  """
  # Set namespace at method's level.
  params = SOAPpy.Types.untypedType(Utils.MakeTextXMLReady(params))
  params._setAttr('xmlns', config['ns_target'][0])

  # Set namespace at body's level.
  body = SOAPpy.Types.bodyType({method_name: params})
  body._setAttr('xmlns', config['ns_target'][0])
  return body


def UnpackResponseAsDict(response):
  """Unpack (recursively) SOAP data holder into a Python dict object.

  Args:
    response: instance SOAP data holder object.

  Returns:
    dict Unpacked SOAP data holder.
  """
  if (isinstance(response, types.InstanceType) and
      response.__dict__['_type'] == 'struct'):
    if not response.__dict__.keys(): return (response.__dict__,)
    dct = {}
    for key in response.__dict__:
      if key[0] == '_': continue
      value = response.__dict__.get(key)
      if key.find('.') > -1: key = key.replace('.', '_')
      if (key == 'entries') and not isinstance(value, list):
        value = [value]
      data = UnpackResponseAsDict(value)
      if (key == 'results' or key == 'sizes') and isinstance(data, dict):
        data = [data]
      dct[str(key)] = data
    return dct
  elif (isinstance(response, list) or
        (isinstance(response, types.InstanceType) and
         isinstance(response.__dict__['_type'], tuple)) or
        isinstance(response, SOAPpy.Types.typedArrayType)):
    lst = []
    for item in response:
      if item is None: continue
      lst.append(UnpackResponseAsDict(item))
    return lst
  else:
    if isinstance(response, int) or isinstance(response, long):
      return str(response)
    return response


def RestoreListType(response, key_triggers=()):
  """Restores a response object's list types which were overwritten by SOAPpy.

  Lists with only one element are converted by SOAPpy into a dictionary. This
  handler function restores the proper type.

  Args:
    response: dict Response data object.
    key_triggers: tuple Names of the parameters which should contain list types
                  in the response object.

  Returns:
    dict Restored data object.
  """
  if not key_triggers: return response

  if isinstance(response, dict):
    if not response: return response
    dct = {}
    for key in response:
      value = response.get(key)
      if key in key_triggers and not isinstance(value, list):
        value = [value]
      data = RestoreListType(value, key_triggers)
      dct[str(key)] = data
    return dct
  elif isinstance(response, list):
    lst = []
    for item in response:
      lst.append(RestoreListType(item, key_triggers))
    return lst
  else:
    return response


def RestoreListTypeWithWsdl(response, service_type_map, operation_return_types):
  """Restores list types within given response which were overwritten by SOAPpy.

  Args:
    response: tuple Response data object.
    service_type_map: dict Information on WSDL-defined types in one service.
    operation_return_types: list Data types this operation returns, in order.

  Returns:
    tuple Responses, each with list types restored.
  """
  holder = []
  if (len(operation_return_types) == 1 and
      not Utils.IsXsdOrSoapenc(operation_return_types[0]) and
      service_type_map[operation_return_types[0]]['soap_type'] == 'array'):
    holder.extend(_RestoreListTypesForResponse(
        list(response), operation_return_types[0], service_type_map))
  else:
    for i in range(len(response)):
      holder.append(_RestoreListTypesForResponse(
          response[i], operation_return_types[i], service_type_map))
  return tuple(holder)


def _RestoreListTypesForResponse(response, xsi_type, service_type_map):
  """Restores list types for an individual response object.

  Args:
    response: obj An individual object returned by the webservice. May be a
              dictionary, list, or string depending on what it represents.
    xsi_type: str The WSDL-defined type of this response.
    service_type_map: dict Information on WSDL-defined types in one service.

  Returns:
    obj The response in its proper format. May be a dictionary, list, or string
    depending on what was input. Not guaranteed to output the same data type
    that was input - may output a list instead.
  """
  if isinstance(response, dict):
    if not response: return response
    for param, param_type in Utils.GenParamOrder(service_type_map, xsi_type):
      if not param in response or Utils.IsXsdOrSoapenc(param_type):
        continue
      value = response[param]
      if (service_type_map[param_type]['soap_type'] == 'array' and not
          isinstance(response[param], list)):
        value = [value]
      response[param] = _RestoreListTypesForResponse(
          value, param_type, service_type_map)
    return response
  elif isinstance(response, list):
    lst = []
    for item in response:
      if item is None: continue
      lst.append(_RestoreListTypesForResponse(
          item, service_type_map[xsi_type]['base_type'], service_type_map))
    return lst
  else:
    return response
