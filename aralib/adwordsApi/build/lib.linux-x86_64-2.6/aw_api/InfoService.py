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

"""Methods to access InfoService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import datetime

from aw_api import SOAPPY
from aw_api import ZSI
from aw_api import SanityCheck as glob_sanity_check
from aw_api import Utils
from aw_api.Errors import ApiVersionNotSupportedError
from aw_api.Errors import ValidationError
from aw_api.WebService import WebService


class InfoService(object):

  """Wrapper for InfoService.

  The Info Service allows you to obtain some basic information about your
  API usage.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits InfoService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock the thread lock.
      logger: Logger the instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['version'],
           self.__class__.__name__]
    if glob_sanity_check.IsNewApi(op_config['version']): url.insert(2, 'info')
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = WebService(headers, config, op_config, '/'.join(url), lock,
                                logger)
    self.__config = config
    self.__op_config = op_config
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

  def GetUnitSummary(self):
    """Retrieve the current status of API units.

    The results are similar to the numbers shown in API Center.

    Returns:
      tuple collection of API units stats.
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
      tuple total number of API units used.
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

  def GetUnitDetails(self, start_date='%Y%m01', end_date='%Y%m%d'):
    """Retrieve details of the API units usage for given date range.

    Defaults to current month.

    Args:
      [optional]
      start_date: str beginning of the date range, inclusive.
      end_date: str end of the date range, inclusive.

    Returns:
      tuple detailed API usage.
    """
    glob_sanity_check.ValidateTypes(((start_date, (str, unicode)),
                                     (end_date, (str, unicode))))
    date = start_date
    start_date = datetime.datetime.now().strftime(start_date)
    end_date = datetime.datetime.now().strftime(end_date)
    ops_rates = Utils.GetOpsRates()

    usage = []
    for parts in ops_rates:
      (method, operator) = (parts[2], '')
      if len(parts[2].split('.')) > 1:
        (method, operator) = parts[2].split('.')
      selector = {
          'serviceName': parts[1],
          'methodName': method,
          'dateRange': {
              'min': start_date,
              'max': end_date
          },
          'apiUsageType': 'UNIT_COUNT'
      }
      if operator: selector['operator'] = operator
      unit_count = self.Get(selector)[0]['cost']
      if long(unit_count) > 0:
        usage.append({
            'date': date,
            'service': parts[1],
            'method': method,
            'operator': operator,
            'units': unit_count
        })
    return (usage,)

  def GetUnitDetailsDaily(self, date_day=None):
    """Retrieve details of the API units usage per day for current month.

    Args:
      date_day: str number of days to look up.

    Returns:
      tuple detailed API usage per day.
    """
    if date_day is None:
      date_day = datetime.datetime.now().strftime('%d')
    glob_sanity_check.ValidateTypes(((date_day, (str, unicode)),))
    usage = []
    for day in range(1, int(date_day) + 1):
      if day < 10: day = '0%s' % day
      start_date = datetime.datetime.now().strftime('%%Y%%m%s' % day)
      end_date = start_date
      day_usage = self.GetUnitDetails(start_date, end_date)[0]
      if day_usage: usage.append(day_usage)
    return (usage,)

  def Get(self, selector):
    """Return the API usage information.

    Usage information is based on the selection criteria of the selector.

    Args:
      selector: dict filter to run API usage through.

    Returns:
      tuple API usage information.
    """
    method_name = 'getInfo'
    if self.__config['soap_lib'] == SOAPPY:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with SOAPpy toolkit.' % (Utils.GetCurrentFuncName(),
                                           self.__op_config['version']))
      raise ApiVersionNotSupportedError(msg)
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      self.__sanity_check.ValidateSelector(selector, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'selector': selector},)),
                                       'Info', self.__loc, request)

