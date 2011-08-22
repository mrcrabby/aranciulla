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

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import ETREE
from adspygoogle.common import PYXML
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI
from adspygoogle.common.Errors import ValidationError


def ValidateRequiredHeaders(headers, required_headers):
  """Sanity check for required authentication elements.

  All required authentication headers have to be set in order to make
  successful API request.

  Args:
    headers: dict Authentication headers.
    required_headers: tuple Valid combinations of headers.

  Raises:
    ValidationError: The given authentication headers are not sufficient to make
                     requests agaisnt this API.
  """
  is_valid = True
  for headers_set in required_headers:
    is_valid_set = True
    for key in headers_set:
      if key not in headers or not headers[key]: is_valid_set = False
    if not is_valid_set:
      is_valid = False
    else:
      is_valid = True
      break

  if not is_valid:
    msg = ('Required authentication header is missing. Valid options for '
           'headers are %s.' % str(required_headers))
    raise ValidationError(msg)


def IsConfigUserInputValid(user_input, valid_el):
  """Sanity check for user input.

  Args:
    user_input: str User input.
    valid_el: list List of valid elements.

  Returns:
    bool True if user input is valid, False otherwise.
  """
  if not user_input: return False

  try:
    valid_el.index(str(user_input))
  except ValueError:
    return False
  return True


def ValidateConfigSoapLib(soap_lib):
  """Sanity check for SOAP library.

  Args:
    soap_lib: str SOAP library to use.

  Raises:
    ValidationError: The given SOAP toolkit is not supported by this library.
  """
  if (not isinstance(soap_lib, str) or
      not IsConfigUserInputValid(soap_lib, [SOAPPY, ZSI])):
    msg = ('Invalid input for %s \'%s\', expecting %s or %s of type <str>.'
           % (type(soap_lib), soap_lib, SOAPPY, ZSI))
    raise ValidationError(msg)


def ValidateConfigXmlParser(xml_parser):
  """Sanity check for XML parser.

  Args:
    xml_parser: str XML parser to use.

  Raises:
    ValidationError: The given XML parser is not supported by this library.
  """
  if (not isinstance(xml_parser, str) or
      not IsConfigUserInputValid(xml_parser, [PYXML, ETREE])):
    msg = ('Invalid input for %s \'%s\', expecting %s or %s of type <str>.'
           % (type(xml_parser), xml_parser, PYXML, ETREE))
    raise ValidationError(msg)


def IsType(param, param_type):
  """Check if parameter is of the right type.

  Args:
    param: obj Parameter to check.
    param_type: type Type of the parameter to check against.

  Returns:
    bool True if the parameter is of right type, False otherwise.
  """
  if not isinstance(param, param_type):
    return False
  return True


def ValidateTypes(vars_tpl):
  """Check types for a set of variables.

  Args:
    vars_tpl: tuple Set of variables to check.

  Raises:
    ValidationError: The given object was not one of the given accepted types.
  """
  for var, var_types in vars_tpl:
    if not isinstance(var_types, tuple):
      var_types = (var_types,)
    for var_type in var_types:
      if IsType(var, var_type):
        return
    msg = ('The \'%s\' is of type %s, expecting one of %s.'
           % (var, type(var), var_types))
    raise ValidationError(msg)


def ValidateOneLevelObject(obj):
  """Validate object with one level of complexity.

  Args:
    obj: dict Object to validate.
  """
  ValidateTypes(((obj, dict),))
  for key in obj:
    if obj[key] != 'None': ValidateTypes(((obj[key], (str, unicode)),))


def ValidateOneLevelList(lst):
  """Validate list with one level of complexity.

  Args:
    lst: list List to validate.
  """
  ValidateTypes(((lst, list),))
  for item in lst:
    if item != 'None': ValidateTypes(((item, (str, unicode)),))


def IsSuperType(wsdl_types, sub_type, super_type):
  """Checks to see if one type is a supertype of another type.

  Any case where the sub_type cannot be traced through to super_type is
  considered to be an invalid supertype. For example, if the WSDL definitions
  dictionary is empty or if one type's entry in the definitions does not include
  the required field (base_type), these are not valid supertypes.

  Args:
    wsdl_types: dict WSDL-defined types in the same service as the given type.
    sub_type: str Type that may be extending super_type.
    super_type: str Type that may be extended by sub_type.

  Returns:
    bool Whether super_type is really a supertype of sub_type.
  """
  if not wsdl_types or sub_type not in wsdl_types:
    return False
  while (sub_type != super_type and 'base_type' in wsdl_types[sub_type] and
         wsdl_types[sub_type]['base_type']):
    sub_type = wsdl_types[sub_type]['base_type']
  return sub_type == super_type


def _SanityCheckComplexType(wsdl_types, obj, xsi_type):
  """Validates a dict representing a complex type against its WSDL definition.

  Args:
    wsdl_types: dict WSDL-defined types in the same service as the given type.
    obj: dict Object that should represent an instance of the given type.
    xsi_type: str The complex type name defined in the WSDL.

  Raises:
    ValidationError: The given object is not an acceptable representation of the
                     given WSDL-defined complex type.
  """
  ValidateTypes(((obj, dict),))
  obj_contained_type, contained_type_key = Utils.GetExplicitType(wsdl_types,
                                                                 obj, xsi_type)

  if obj_contained_type and not obj_contained_type == xsi_type:
    if not IsSuperType(wsdl_types, obj_contained_type, xsi_type):
      raise ValidationError('Expecting type of \'%s\' but given type of class '
                            '\'%s\'.' % (xsi_type, obj_contained_type))
    xsi_type = obj_contained_type

  parameters = Utils.GenParamOrder(wsdl_types, xsi_type)
  for key in obj:
    if obj[key] is None or (obj_contained_type and key == contained_type_key):
      continue
    found = False
    for parameter, param_type in parameters:
      if parameter == key:
        found = True
        if Utils.IsXsdOrSoapenc(param_type):
          ValidateTypes(((obj[key], (str, unicode)),))
        else:
          NewSanityCheck(wsdl_types, obj[key], param_type)
        break
    if not found:
      raise ValidationError('Field \'%s\' is not in type \'%s\'.'
                            % (key, xsi_type))


def _SanityCheckSimpleType(wsdl_types, obj, xsi_type):
  """Validates a string representing a simple type against its WSDL definition.

  Args:
    wsdl_types: dict WSDL-defined types in the same service as the given type.
    obj: str String representing the given simple type.
    xsi_type: str The simple type name defined in the WSDL.

  Raises:
    ValidationError: The given object is not an acceptable representation of the
                     given WSDL-defined simple type.
  """
  ValidateTypes(((obj, (str, unicode)),))
  if obj not in wsdl_types[xsi_type]['allowed_values']:
    raise ValidationError('Value \'%s\' is not listed as an acceptable value '
                          'for type \'%s\'. Allowed values are: %s.' %
                          (obj, xsi_type,
                           wsdl_types[xsi_type]['allowed_values']))


def _SanityCheckArray(wsdl_types, obj, xsi_type):
  """Validates a list representing an array type against its WSDL definition.

  Args:
    wsdl_types: dict WSDL-defined types in the same service as the given type.
    obj: list List representing the given array type.
    xsi_type: str The array type name defined in the WSDL.
  """
  ValidateTypes(((obj, list),))
  if Utils.IsXsdOrSoapenc(wsdl_types[xsi_type]['base_type']):
    for item in obj:
      if item is None: continue
      ValidateTypes(((item, (str, unicode)),))
  else:
    for item in obj:
      if item is None: continue
      NewSanityCheck(wsdl_types, item, wsdl_types[xsi_type]['base_type'])


def NewSanityCheck(wsdl_types, obj, xsi_type):
  """Validates any given object against its WSDL definition.

  This method considers None and the empty string to be a valid representation
  of any type.

  Args:
    wsdl_types: dict WSDL-defined types in the same service as the given type.
    obj: object Object to be validated. Depending on the WSDL-defined type this
         is representing, the data type will vary. It should always be either a
         dictionary, list, or string no matter what WSDL-defined type it is.
    xsi_type: str The type name defined in the WSDL.

  Raises:
    ValidationError: The given WSDL-defined type has no definition in the WSDL
                     types map.
  """
  if obj in (None, ''):
    return
  if not xsi_type in wsdl_types:
    raise ValidationError('This type is not defined in the WSDL: %s.'
                          % xsi_type)
  if wsdl_types[xsi_type]['soap_type'] == 'simple':
    _SanityCheckSimpleType(wsdl_types, obj, xsi_type)
  elif wsdl_types[xsi_type]['soap_type'] == 'complex':
    _SanityCheckComplexType(wsdl_types, obj, xsi_type)
  elif wsdl_types[xsi_type]['soap_type'] == 'array':
    _SanityCheckArray(wsdl_types, obj, xsi_type)
  else:
    raise ValidationError('Error in autogenerated WSDL definitions - Unknown '
                          'parameter type: %s'
                          % wsdl_types[xsi_type]['soap_type'])
