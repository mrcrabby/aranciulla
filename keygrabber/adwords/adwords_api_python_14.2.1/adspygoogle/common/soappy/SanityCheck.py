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

import cgi
import re

from adspygoogle.common import SanityCheck
from adspygoogle.common.Errors import MissingPackageError
from adspygoogle.common.soappy import MIN_SOAPPY_VERSION
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


def UnType(item):
  """Convert given string into untyped type.

  Args:
    item: str String to untype.

  Returns:
    untypedType String converted into untypedType.
  """
  SanityCheck.ValidateTypes(((item, (str, unicode)),))

  # HTML encode non-complex strings. Complex strings would be XML snippets,
  # like <networkTypes>GoogleSearch</networkTypes>.
  pattern = re.compile('<.*>|</.*>')
  if pattern.search(item) is None:
    pattern = re.compile('&#(x\w{2,4}|\d{3});')
    result = pattern.findall(item)
    # Escape only ASCII characters.
    if not result: item = cgi.escape(item)
  return SOAPpy.Types.untypedType(item)


def IsUnTypedClass(obj):
  """Return True if a given object is of type SOAPpy.Types.untypedType, False
  otherwise.

  Args:
    obj: object Object to check.

  Returns:
    bool True if a given object is untyped, False otherwise.
  """
  return isinstance(obj, SOAPpy.Types.untypedType)
