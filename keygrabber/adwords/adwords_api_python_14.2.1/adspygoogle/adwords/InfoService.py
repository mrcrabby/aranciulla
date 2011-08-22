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

"""Methods to access InfoService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import datetime

from adspygoogle.adwords import AdWordsSanityCheck
from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService


class InfoService(ApiService):

  """Wrapper for InfoService.

  The InfoService service allows you to obtain some basic information about your
  API usage.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits InfoService.

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
    if AdWordsSanityCheck.IsJaxbApi(op_config['version']): url.insert(2, 'info')
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(InfoService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def GetUnitSummary(self):
    """Retrieve the current status of API units.

    The results are similar to the numbers shown in API Center.

    Returns:
      tuple Collection of API units stats.
    """
    selector = {
        'apiUsageType': 'TOTAL_USAGE_API_UNITS_PER_MONTH'
    }
    total_units = self.Get(selector)[0]['cost']

    selector = {
        'apiUsageType': 'FREE_USAGE_API_UNITS_PER_MONTH'
    }
    free_units_limit = self.Get(selector)[0]['cost']

    selector = {
        'dateRange': {
            'min': datetime.datetime.now().strftime('%Y%m01'),
            'max': datetime.datetime.now().strftime('%Y%m%d')
        },
        'apiUsageType': 'UNIT_COUNT'
    }
    units_count = self.Get(selector)[0]['cost']

    if long(units_count) > long(free_units_limit):
      free_units_used = free_units_limit
    else:
      free_units_used = units_count

    stats = {
        'free_units_used': free_units_used,
        'total_units_used': units_count,
        'free_units_remaining': long(free_units_limit) - long(free_units_used),
        'total_units': total_units
    }
    return (stats,)

  def GetTotalUnitUsed(self):
    """Retrieve the total number of API units used.

    Units used from beggining of time to now.

    Returns:
      tuple Total number of API units used.
    """
    start_date = '20040101'
    end_date = datetime.datetime.now().strftime('%Y%m%d')
    selector = {
        'dateRange': {
            'min': start_date,
            'max': end_date
        },
        'apiUsageType': 'UNIT_COUNT'
    }
    return (self.Get(selector)[0]['cost'],)

  def Get(self, selector):
    """Return the API usage information.

    Usage information is based on the selection criteria of the selector.

    Args:
      selector: dict Filter to run API usage through.

    Returns:
      tuple API usage information.
    """
    method_name = 'getInfo'

    SanityCheck.NewSanityCheck(self._wsdl_types_map, selector, 'InfoSelector')

    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'selector', self._wsdl_types_map, False, 'InfoSelector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'InfoSelector', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'selector': selector},)),
                                       'Info', self._loc, request)
