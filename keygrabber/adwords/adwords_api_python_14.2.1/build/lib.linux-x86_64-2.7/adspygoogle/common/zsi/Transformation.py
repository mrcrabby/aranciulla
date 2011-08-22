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

"""Transforms python objects into ZSI-compatible form."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

from adspygoogle.common import Utils
from adspygoogle.common.zsi import SanityCheck as ZsiSanityCheck


def MakeZsiCompatible(obj, xsi_type, wsdl_types, web_service):
  """Ensures a given object is compatible with ZSI, possibly by transforming it.

  Dictionaries with valid xsi_types are transformed into ZSI objects. Everything
  else is returned in the same data type as it was given. List and dictionary
  contents will be recursively checked/altered for compatibility.

  Args:
    obj: obj The python object to make ZSI compatible. Should be a dict,
         list, or string depending on the xsi_type. May also already be a ZSI
         object, in which case it is returned unaltered.
    xsi_type: str The WSDL-defined type of the given object.
    wsdl_types: dict A map of all WSDL-defined types in the same service as the
                given type.
    web_service: module The generated web service which uses this object.

  Returns:
    obj The python object passed in, compatible with ZSI.
  """
  if (ZsiSanityCheck.IsPyClass(obj) or not xsi_type in wsdl_types or
      wsdl_types[xsi_type]['soap_type'] == 'simple'):
    return obj
  elif wsdl_types[xsi_type]['soap_type'] == 'complex':
    return ZsiTransfomComplexType(wsdl_types, obj, xsi_type, web_service)
  elif wsdl_types[xsi_type]['soap_type'] == 'array':
    return ZsiTransfomArray(wsdl_types, obj, xsi_type, web_service)


def ZsiTransfomComplexType(wsdl_types, obj, xsi_type, web_service):
  """Transforms a python dictionary into a ZSI object.

  Args:
    wsdl_types: dict WSDL definitions of all types in the same service as the
                given xsi_type.
    obj: dict Dictionary to be made into a ZSI object.
    xsi_type: str The name of the complex type this dictionary represents.
    web_service: module The generated web service which uses this complex type.

  Returns:
    obj A ZSI object representing this complex type.
  """
  obj_contained_type, contained_type_key = Utils.GetExplicitType(wsdl_types,
                                                                 obj, xsi_type)
  if obj_contained_type:
    xsi_type = obj_contained_type

  new_object = ZsiSanityCheck.GetPyClass(xsi_type, web_service)

  parameters = Utils.GenParamOrder(wsdl_types, xsi_type)
  for key in obj:
    if not obj[key] or key == contained_type_key:
      continue
    for parameter, param_type in parameters:
      if parameter == key:
        new_object.__dict__.__setitem__(
            '_%s' % key, MakeZsiCompatible(obj[key], param_type, wsdl_types,
                                           web_service))
        break
  return new_object


def ZsiTransfomArray(wsdl_types, obj, xsi_type, web_service):
  """Ensures a list is compatible with ZSI, possibly by altering its contents.

  Args:
    wsdl_types: dict WSDL definitions of all types in the same service as the
                given xsi_type.
    obj: list List to be made ready for ZSI-transport.
    xsi_type: str The WSDL-defined type name that the given list represents.
    web_service: module The generated web service which uses this list.

  Returns:
    obj A list whose contents have been transformed into ZSI-acceptable form.
  """
  new_array = []
  for item in obj:
    new_array.append(MakeZsiCompatible(item, wsdl_types[xsi_type]['base_type'],
                                       wsdl_types, web_service))
  return new_array
