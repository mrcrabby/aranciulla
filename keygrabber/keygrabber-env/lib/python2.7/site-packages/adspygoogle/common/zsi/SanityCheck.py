#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
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

"""Validation and type conversion functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import MAX_TARGET_NAMESPACE
from adspygoogle.common.Errors import ValidationError


def GetPyClass(name, web_services):
  """Return Python class for a given class name.

  Args:
    name: str Name of the Python class to return.
    web_services: Module for web service.

  Returns:
    Python class.
  """
  for index in xrange(MAX_TARGET_NAMESPACE):
    try:
      pyclass = eval('web_services.ns%s.%s_Def(\'%s\').pyclass' % (index, name,
                                                                   name))
      break
    except AttributeError:
      if index == MAX_TARGET_NAMESPACE - 1:
        version = web_services.__dict__['__name__'].split('.')[2]
        msg = ('Given API version, %s, is not compatible with \'%s\' class.' %
               (version, name))
        raise ValidationError(msg)
  return pyclass


def IsPyClass(obj):
  """Return True if a given object is a Python class, False otherwise.

  Args:
    obj: object Object to check.

  Returns:
    bool True if a given object is a Python class, False otherwise.
  """
  if (hasattr(obj, 'typecode') and
      str(obj.typecode.pyclass).find('_Holder') > -1):
    return True
  return False
