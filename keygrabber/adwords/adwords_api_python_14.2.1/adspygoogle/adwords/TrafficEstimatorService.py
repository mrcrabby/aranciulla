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

"""Methods to access TrafficEstimatorService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.adwords import AdWordsSanityCheck
from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService


class TrafficEstimatorService(ApiService):

  """Wrapper for TrafficEstimatorService.

  The TrafficEstimatorService service provides operations for estimating
  campaign, ad group, and keyword traffic.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits TrafficEstimatorService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['version'],
           self.__class__.__name__]
    if AdWordsSanityCheck.IsJaxbApi(op_config['version']): url.insert(2, 'o')
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__name_space = 'https://adwords.google.com/api/adwords'
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(TrafficEstimatorService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def CheckKeywordTraffic(self, requests):
    """Check a batch of keywords to see whether they will get any traffic.

    Args:
      requests: list Requests for keyword traffic checks.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((requests, list),))
    for item in requests:
      self._sanity_check.ValidateKeywordTrafficRequestV13(item)

    method_name = 'checkKeywordTraffic'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, (requests))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'requests': requests},)),
                                       'TrafficEstimator', self._loc, request)

  def EstimateAdGroupList(self, requests):
    """Return traffic estimates for the requested set.

    Set is of new or existing ad groups.

    Args:
      requests: list Set of ad groups to estimate.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((requests, list),))

    method_name = 'estimateAdGroupList'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck
      items = []
      for item in requests:
        items.append(self._sanity_check.ValidateAdGroupRequestV13(item))
      requests = SoappySanityCheck.UnType(''.join(items))
      name_space = '/'.join([self.__name_space, self._op_config['version'],
                             self._config['access']]).strip('/')
      requests._setAttr('xmlns:impl', name_space)
      requests._setAttr('xsi3:type', 'AdGroupRequests')
      return self.__service.CallMethod(method_name, (requests))
    elif self._config['soap_lib'] == ZSI:
      for item in requests:
        self._sanity_check.ValidateAdGroupRequestV13(item)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'adGroupRequests': requests},)),
                                       'TrafficEstimator', self._loc, request)

  def EstimateCampaignList(self, requests):
    """Return traffic estimates for the requested set of campaigns.

    Args:
      requests: list Set of campaigns to estimate.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((requests, list),))

    method_name = 'estimateCampaignList'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck
      items = []
      for item in requests:
        items.append(self._sanity_check.ValidateCampaignRequestV13(item))
      requests = SoappySanityCheck.UnType(''.join(items))
      name_space = '/'.join([self.__name_space, self._op_config['version'],
                             self._config['access']]).strip('/')
      requests._setAttr('xmlns:impl', name_space)
      requests._setAttr('xsi3:type', 'CampaignRequests')
      return self.__service.CallMethod(method_name, (requests))
    elif self._config['soap_lib'] == ZSI:
      for item in requests:
        self._sanity_check.ValidateCampaignRequestV13(item)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'campaignRequests': requests},)),
                                       'TrafficEstimator', self._loc, request)

  def EstimateKeywordList(self, requests):
    """Return traffic estimates for the requested set of new keywords.

    Args:
      requests: list Set of keywords to estimate.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((requests, list),))

    method_name = 'estimateKeywordList'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck
      new_data = []
      for item in requests:
        new_data.append(SoappySanityCheck.UnType(
            self._sanity_check.ValidateKeywordRequestV13(item)))
      return self.__service.CallMethod(method_name, (new_data))
    elif self._config['soap_lib'] == ZSI:
      for item in requests:
        self._sanity_check.ValidateKeywordRequestV13(item)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'keywordRequests': requests},)),
                                       'TrafficEstimator', self._loc, request)

  def Get(self, selector):
    """Return a list of traffic estimates.

    Args:
      selector: dict Filter to run traffic estimate requests through.

    Returns:
      tuple List of traffic estimates meeting all the criteria of the selector.
    """
    SanityCheck.NewSanityCheck(
          self._wsdl_types_map, selector, 'TrafficEstimatorSelector')

    method_name = 'getTrafficEstimator'
    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'selector', self._wsdl_types_map, False,
          'TrafficEstimatorSelector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'TrafficEstimatorSelector', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'TrafficEstimator', self._loc, request)
