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

"""Methods to access BulkOpportunity service."""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

from adspygoogle.adwords import AdWordsSanityCheck
from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService


class BulkOpportunityService(ApiService):

  """Wrapper for BulkOpportunityService.

  The BulkOpportunityService service lets you research opportunities for your
  AdWords account in bulk.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits BulkOpportunityService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['version'],
           self.__class__.__name__]
    if AdWordsSanityCheck.IsJaxbApi(op_config['version']): url.insert(2, 'o')
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(BulkOpportunityService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def Get(self, selector):
    """Return a page of opportunities.

    Args:
      selector: dict Filter to run opportunities through.

    Returns:
      tuple List of user lists meeting all the criteria of the selector.
    """
    method_name = 'getBulkOpportunity'
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, selector, 'BulkOpportunitySelector')

    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'selector', self._wsdl_types_map, False,
          'BulkOpportunitySelector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'BulkOpportunitySelector', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'BulkOpportunity', self._loc, request)
