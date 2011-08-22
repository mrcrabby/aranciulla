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

"""Methods to access DataService service."""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

from adspygoogle.adwords import AdWordsSanityCheck
from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.adwords import AdWordsUtils
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService


class DataService(ApiService):

  """Wrapper for DataService.

  The DataService service lets you retrieve Ads Campaign Management data
  matching a selector.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits DataService.

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
    if AdWordsSanityCheck.IsJaxbApi(op_config['version']): url.insert(2, 'cm')
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(DataService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def GetAdGroupBidLandscape(self, selector):
    """Return a list of bid landscapes for the ad groups in the selector.

    Args:
      selector: dict Filter to run bid landscapes through.

    Returns:
      tuple List of bid landscapes meeting all the criteria of the selector.
    """
    method_name = 'getAdGroupBidLandscape'
    SanityCheck.NewSanityCheck(self._wsdl_types_map, selector, 'Selector')

    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'serviceSelector', self._wsdl_types_map, False, 'Selector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'Selector', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'serviceSelector': selector},)),
                                       'Data', self._loc, request)

  def GetCriterionBidLandscape(self, selector):
    """Return a list of bid landscapes for the criteria in the selector.

    Args:
      selector: dict Filter to run bid landscapes through.

    Returns:
      tuple List of bid landscapes meeting all the criteria of the selector.
    """
    method_name = 'getCriterionBidLandscape'
    SanityCheck.NewSanityCheck(self._wsdl_types_map, selector, 'Selector')

    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'serviceSelector', self._wsdl_types_map, False, 'Selector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'Selector', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'serviceSelector': selector},)),
                                       'Data', self._loc, request)
