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

"""Creates XML Signature handler to support SOAP headers."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from aw_api import Utils


class SigHandler(object):

  """Implements SigHandler.

  Rosponsible for creating XML Signature handler to support SOAP headers
  for the outgoing SOAP message. Overwrites XML Signature handler, must sign
  and verify.
  """

  def __init__(self, headers, config):
    """Inits SigHandler with authentication headers.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
    """
    self.__headers = headers
    self.__config = config

  def sign(self, soap_writer):
    """Sign signature handler.

    Args:
      soap_writer: SoapWriter instance.
    """
    keys = []
    for key in self.__headers:
      keys.append((key, self.__headers[key]))
    keys = tuple(keys)

    header = soap_writer._header
    body = soap_writer.body
    # Set RequestHeader element, if appropriate.
    if 'ns_target' in self.__config:
      name_space, target = self.__config['ns_target']
      header = header.createAppendElement('', target)
      header.setNamespaceAttribute('', name_space)

      # Explicitly set namespace at the request method's level. For services
      # with multiple namespaces, this has to be done prior to checking where
      # RequestHeader elements point.
      if body._getElements():
        body._getElements()[0].setAttributeNS('', 'xmlns:ns1', name_space)

      # Make sure that the namespace for RequestHeader elements is pointing
      # at cm/.
      if 'cm' not in Utils.GetPathFromUrl(name_space).split('/'):
        parts = name_space.split('/')
        parts[-2] = 'cm'
        name_space = '/'.join(parts)
    else:
      name_space = ''
    for key, value in keys:
      if value:
        header.createAppendElement(name_space, key).createAppendTextNode(value)

  def verify(self, soap_writer):
    """Veirfy if signature handler is signed.

    Args:
      soap_writer: SoapWriter instance.

    Raises:
      VerifyError to indicate invalid signature.
    """
    pass
