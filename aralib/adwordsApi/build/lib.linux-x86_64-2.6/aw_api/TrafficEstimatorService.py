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

"""Methods to access TrafficEstimatorService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from aw_api import SanityCheck as glob_sanity_check
from aw_api import SOAPPY
from aw_api import ZSI
from aw_api.Errors import ValidationError
from aw_api.WebService import WebService


class TrafficEstimatorService(object):

  """Wrapper for TrafficEstimatorService.

  The Traffic Estimator Service provides operations for estimating keyword
  traffic, campaign traffic, and ad group traffic.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits TrafficEstimatorService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock the thread lock
      logger: Logger the instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['version'],
           self.__class__.__name__]
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = WebService(headers, config, op_config, '/'.join(url), lock,
                                logger)
    self.__config = config
    self.__op_config = op_config
    self.__name_space = 'https://adwords.google.com/api/adwords'
    if self.__config['soap_lib'] == SOAPPY:
      from aw_api.soappy_toolkit import SanityCheck
      self.__web_services = None
    elif self.__config['soap_lib'] == ZSI:
      from aw_api import API_VERSIONS
      from aw_api.zsi_toolkit import SanityCheck
      if op_config['version'] in API_VERSIONS:
        module = '%s_services' % self.__class__.__name__
        try:
          web_services = __import__('aw_api.zsi_toolkit.%s.%s'
                                    % (op_config['version'], module), globals(),
                                    locals(), [''])
        except ImportError, e:
          # If one of library's required modules is missing, re raise exception.
          if str(e).find(module) < 0:
            raise ImportError(e)
          msg = ('The version \'%s\' is not compatible with \'%s\'.'
                 % (op_config['version'], self.__class__.__name__))
          raise ValidationError(msg)
      else:
        msg = 'Invalid API version, not one of %s.' % str(list(API_VERSIONS))
        raise ValidationError(msg)
      self.__web_services = web_services
      self.__loc = eval('web_services.%sLocator()' % self.__class__.__name__)
    self.__sanity_check = SanityCheck

  def CheckKeywordTraffic(self, requests):
    """Check a batch of keywords to see whether they will get any traffic.

    Args:
      requests: list requests for keyword traffic checks.

        Ex:
          requests = [
            {
              'keywordText': 'Flowers',
              'keywordType': 'Broad',
              'language': 'en'
            }
          ]

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((requests, list),))
    for item in requests:
      self.__sanity_check.ValidateKeywordTrafficRequestV13(item)

    method_name = 'checkKeywordTraffic'
    if self.__config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, (requests))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'requests': requests},)),
                                       'TrafficEstimator', self.__loc, request)

  def EstimateAdGroupList(self, requests):
    """Return traffic estimates for the requested set.

    Set is of new or existing ad groups.

    Args:
      requests: list set of ad groups to estimate.

        Ex:
          requests = [
            {
              'id': '1234567890',
              'keywordRequests': [
                {
                  'id': '1234567890',
                  'maxCpc': '1000000',
                  'negative': 'False',
                  'text': 'Flowers',
                  'type': 'Broad'
                }
              ],
              'maxCpc': '1000000'
            }
          ]

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((requests, list),))

    method_name = 'estimateAdGroupList'
    if self.__config['soap_lib'] == SOAPPY:
      items = []
      for item in requests:
        items.append(self.__sanity_check.ValidateAdGroupRequestV13(item))
      requests = self.__sanity_check.UnType(''.join(items))
      name_space = '/'.join([self.__name_space, self.__op_config['version'],
                             self.__config['access']]).strip('/')
      requests._setAttr('xmlns:impl', name_space)
      requests._setAttr('xsi3:type', 'AdGroupRequests')
      return self.__service.CallMethod(method_name, (requests))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      for item in requests:
        self.__sanity_check.ValidateAdGroupRequestV13(item)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'adGroupRequests': requests},)),
                                       'TrafficEstimator', self.__loc, request)

  def EstimateCampaignList(self, requests):
    """Return traffic estimates for the requested set of campaigns.

    Args:
      requests: list set of campaigns to estimate.

        Ex:
          requests = [
            {
              'adGroupRequests': [
                {
                  'id': '1234567890',
                  'keywordRequests': [
                    {
                      'id': '1234567890',
                      'maxCpc': '1000000',
                      'negative': 'False',
                      'text': 'Flowers',
                      'type': 'Broad'
                    }
                  ],
                  'maxCpc': '1000000'
                }
              ],
              'geoTargeting': {
                'cityTargets': ['New York, NY US'],
                'countryTargets': ['US'],
                'metroTargets': ['501'],
                'proximityTargets': [
                  {
                    'latitudeMicroDegrees': '12345',
                    'longitudeMicroDegrees': '12345',
                    'radiusMeters': '5'
                  }
                ],
                'regionsTargets': ['US-NY'],
                'targetAll': 'False'
              },
              'id': '1234567890',
              'languageTargeting': ['en'],
              'networkTargeting': ['GoogleSearch', 'SearchNetwork']
            }
          ]

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((requests, list),))

    method_name = 'estimateCampaignList'
    if self.__config['soap_lib'] == SOAPPY:
      items = []
      for item in requests:
        items.append(self.__sanity_check.ValidateCampaignRequestV13(item))
      requests = self.__sanity_check.UnType(''.join(items))
      name_space = '/'.join([self.__name_space, self.__op_config['version'],
                             self.__config['access']]).strip('/')
      requests._setAttr('xmlns:impl', name_space)
      requests._setAttr('xsi3:type', 'CampaignRequests')
      return self.__service.CallMethod(method_name, (requests))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      for item in requests:
        self.__sanity_check.ValidateCampaignRequestV13(item)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'campaignRequests': requests},)),
                                       'TrafficEstimator', self.__loc, request)

  def EstimateKeywordList(self, requests):
    """Return traffic estimates for the requested set of new keywords.

    Args:
      requests: list set of keywords to estimate.

        Ex:
          requests = [
            {
              'id': '1234567890',
              'maxCpc': '1000000',
              'negative': 'False',
              'text': 'Flowers',
              'type': 'Broad'
            }
          ]

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((requests, list),))

    method_name = 'estimateKeywordList'
    if self.__config['soap_lib'] == SOAPPY:
      new_data = []
      for item in requests:
        new_data.append(self.__sanity_check.UnType(
            self.__sanity_check.ValidateKeywordRequestV13(item)))
      return self.__service.CallMethod(method_name, (new_data))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      for item in requests:
        self.__sanity_check.ValidateKeywordRequestV13(item)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'keywordRequests': requests},)),
                                       'TrafficEstimator', self.__loc, request)
