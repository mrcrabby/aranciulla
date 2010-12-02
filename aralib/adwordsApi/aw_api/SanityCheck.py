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
#

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import re

from aw_api import ETREE
from aw_api import PYXML
from aw_api import SOAPPY
from aw_api import ZSI
from aw_api.Errors import ValidationError


def ValidateRequiredHeaders(headers):
  """Sanity check for required authentication elements.

  All required authentication headers have to be set in order to make
  successful API request.

  Args:
    headers: dict authentication headers.
  """
  req_headers = ('email', 'password', 'userAgent', 'developerToken')
  if 'authToken' in headers and headers['authToken']:
    req_headers = ('authToken', 'userAgent', 'developerToken')
  for key in req_headers:
    if key not in headers or not headers[key]:
      msg = ('Required authentication header \'%s\' is missing.' % key)
      raise ValidationError(msg)


def IsClientIdSet(client_email, client_customer_id):
  """Sanity check for clientEmail/clientCustomerId elements.

  Args:
    client_email: str clientEmail authentication header.
    client_customer_id: str clientCustomerId authentication header.

  Returns:
    bool True if either client_email or client_customer_id is set, False
         otherwise.
  """
  if client_email and client_customer_id:
    return False
  return True


def IsConfigUserInputValid(user_input, valid_el):
  """Sanity check for user input.

  Args:
    user_input: str user input.
    valid_el: list of valid elements.

  Returns:
    bool True if user input is valid, False otherwise.
  """
  if not user_input:
    return False

  try:
    valid_el.index(str(user_input))
  except ValueError:
    return False
  return True


def ValidateServer(server, version):
  """Sanity check for API server.

  Args:
    server: str API server to access for this API call.
    version: str API version being used to access the server.
  """
  # Map of supported API servers and versions.
  prod = {'v13': 'https://adwords.google.com',
          'v200909': 'https://adwords.google.com',
          'v201003': 'https://adwords.google.com'}
  sandbox = {'v13': 'https://sandbox.google.com',
             'v200909': 'https://adwords-sandbox.google.com',
             'v201003': 'https://adwords-sandbox.google.com'}

  if server not in prod.values() and server not in sandbox.values():
    msg = ('Given API server, \'%s\', is not valid. Expecting one of %s.'
           % (server, sorted(prod.values() + sandbox.values())[1:]))
    raise ValidationError(msg)

  if version not in prod.keys() and version not in sandbox.keys():
    msg = ('Geven API version, \'%s\', is not valid. Expecting one of %s.'
           % (version, sorted(set(prod.keys() + sandbox.keys()))))
    raise ValidationError(msg)

  if server != prod[version] and server != sandbox[version]:
    msg = ('Given API version, \'%s\', is not compatible with given server, '
           '\'%s\'.' % (version, server))
    raise ValidationError(msg)


def ValidateConfigSoapLib(soap_lib):
  """Sanity check for SOAP library.

  Args:
    soap_lib: str SOAP library to use.
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
  """
  if (not isinstance(xml_parser, str) or
      not IsConfigUserInputValid(xml_parser, [PYXML, ETREE])):
    msg = ('Invalid input for %s \'%s\', expecting %s or %s of type <str>.'
           % (type(xml_parser), xml_parser, PYXML, ETREE))
    raise ValidationError(msg)


def IsType(param, param_type):
  """Check if parameter is of the right type.

  Args:
    param: parameter to check.
    param_type: type of the parameter to check against.

  Returns:
    bool True if the parameter is of right type, False otherwise.
  """
  if not isinstance(param, param_type):
    return False
  return True


def ValidateTypes(vars_tpl):
  """Check types for a set of variables.

  Args:
    vars_tpl: tuple set of variables to check.
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


def IsNewApi(version):
  """Check if request is being made against new version of API (i.e. old=v13,
  new=v200909).

  Args:
    version: str version of the API being used.

  Returns:
    bool True if request is made against new version of API, False otherwise.
  """
  vmatch = re.search('v\d{2}$', version)
  if vmatch:
    return False
  return True


def ValidateHeadersForServer(headers, server):
  """Check if provided headers match the ones expected on the provided server.

  The SOAP headers on Sandbox server are different from production.  See
  http://code.google.com/apis/adwords/docs/developer/adwords_api_sandbox.html.
  """
  fits_sandbox = False

  # The clientEmail SOAP header in Sandbox has to be of specific format, with
  # "client_" prepended (e.g., client_1+joe.shmoe@gmail.com).
  if ('clientEmail' in headers and headers['clientEmail'] and
      headers['clientEmail'].find('client_', 0, 7) > -1):
    fits_sandbox = True

  # The developerToken SOAP header in Sandbox has to be same as email SOAP
  # header with appended "++" and the currency code.
  if ('email' in headers and headers['email'] and
      headers['developerToken'].find('%s++' % headers['email'], 0,
                                     len(headers['email']) + 2) > -1):
    fits_sandbox = True
  elif ('authToken' in headers and headers['authToken'] and
        headers['developerToken'].find('++') ==
        len(headers['developerToken']) - 5):
    fits_sandbox = True
  else:
    fits_sandbox = False

  # Sandbox server is identifying by the "sandbox" part in the URL (e.g.,
  # https://sandbox.google.com or https://adwords-sandbox.google.com).
  if server.find('sandbox') > -1:
    if not fits_sandbox:
      msg = ('Invalid headers for \'%s\', see http://code.google.com/apis/adwords/docs/developer/adwords_api_sandbox.html#requestheaders.'
             % server)
      raise ValidationError(msg)
  elif server.find('sandbox') < 0:
    if fits_sandbox:
      msg = ('Invalid headers for \'%s\', see http://code.google.com/apis/adwords/docs/developer/index.html#adwords_api_intro_request.'
             % server)
      raise ValidationError(msg)
