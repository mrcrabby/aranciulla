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

"""Validation functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.adwords import API_VERSIONS_MAP
from adspygoogle.common.Errors import ValidationError


def ValidateServer(server, version):
  """Sanity check for API server.

  Args:
    server: str API server to access for this API call.
    version: str API version being used to access the server.
  """
  # Map of supported API servers and versions.
  prod = {'v13': 'https://adwords.google.com',
          'v200909': 'https://adwords.google.com',
          'v201003': 'https://adwords.google.com',
          'v201008': 'https://adwords.google.com',
          'v201101': 'https://adwords.google.com'}
  sandbox = {'v13': 'https://sandbox.google.com',
             'v200909': 'https://adwords-sandbox.google.com',
             'v201003': 'https://adwords-sandbox.google.com',
             'v201008': 'https://adwords-sandbox.google.com',
             'v201101': 'https://adwords-sandbox.google.com'}

  if server not in prod.values() and server not in sandbox.values():
    msg = ('Given API server, \'%s\', is not valid. Expecting one of %s.'
           % (server, sorted(prod.values() + sandbox.values())[1:]))
    raise ValidationError(msg)

  if version not in prod.keys() and version not in sandbox.keys():
    msg = ('Given API version, \'%s\', is not valid. Expecting one of %s.'
           % (version, sorted(set(prod.keys() + sandbox.keys()))))
    raise ValidationError(msg)

  if server != prod[version] and server != sandbox[version]:
    msg = ('Given API version, \'%s\', is not compatible with given server, '
           '\'%s\'.' % (version, server))
    raise ValidationError(msg)


def IsJaxbApi(version):
  """Check if request is being made against API that used JAXB.

  Args:
    version: str Version of the API being used.

  Returns:
    bool True if request is made against an API that used JAXB, False otherwise.
  """
  valid_versions = []
  for api_version, is_jaxb in API_VERSIONS_MAP:
    valid_versions.append(api_version)
    if api_version == version:
      return is_jaxb
  msg = ('Given API version, \'%s\' is not valid. Expecting one of %s.'
         % (version, valid_versions))
  raise ValidationError(msg)


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
      msg = ('Invalid credentials for \'%s\', see http://code.google.com/apis/adwords/docs/developer/adwords_api_sandbox.html#requestheaders.'
             % server)
      raise ValidationError(msg)
  elif server.find('sandbox') < 0:
    if fits_sandbox:
      msg = ('Invalid credentials for \'%s\', see http://code.google.com/apis/adwords/docs/developer/index.html#adwords_api_intro_request.'
             % server)
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
