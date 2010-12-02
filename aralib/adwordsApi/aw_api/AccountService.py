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

"""Methods to access AccountService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from aw_api import SOAPPY
from aw_api import ZSI
from aw_api import SanityCheck as glob_sanity_check
from aw_api.Errors import ValidationError
from aw_api.WebService import WebService


class AccountService(object):

  """Wrapper for AccountService.

  The Account Service allows you to modify AdWords accounts, such as
  changing targeting, business category, and email preferences for existing
  accounts.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits AccountService.

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
    if glob_sanity_check.IsNewApi(op_config['version']):
      url.insert(2, 'account')
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = WebService(headers, config, op_config, '/'.join(url), lock,
                                logger)
    self.__config = config
    self.__op_config = op_config
    if self.__config['soap_lib'] == SOAPPY:
      from aw_api.soappy_toolkit import MessageHandler
      from aw_api.soappy_toolkit import SanityCheck
      self.__web_services = None
      self.__message_handler = MessageHandler
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

  def GetAccountInfo(self):
    """Return the AdWords account specified by the client account header.

    Returns:
      tuple response from the API method.
    """
    method_name = 'getAccountInfo'
    if self.__config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self.__loc,
                                       request)

  def GetClientAccountInfos(self):
    """Get the client account info for managed clients of effective user.

    Returns:
      tuple response from the API method.
    """
    method_name = 'getClientAccountInfos'
    if self.__config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self.__loc,
                                       request)

  def GetClientAccounts(self):
    """Get the primary login for each account managed by the effective user.

    Returns:
      tuple response from the API method.
    """
    method_name = 'getClientAccounts'
    if self.__config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self.__loc,
                                       request)

  def GetMccAlerts(self):
    """Retrieve the MCC alerts.

    The alerts are associated with any of the accounts beneath the current
    account.

    Returns:
      tuple response from the API method.
    """
    method_name = 'getMccAlerts'
    if self.__config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self.__loc,
                                       request)

  def UpdateAccountInfo(self, acct_info):
    """Update the account to reflect the changes in the account object.

    Args:
      acct_info: dict AccountInfo object with updated values.

        Ex:
          acct_info = {
              'defaultNetworkTargeting': ['GoogleSearch'],
              'descriptiveName': 'My Test Account',
              'emailPromotionsPreferences': {
                  'accountPerformanceEnabled': 'True',
                  'disapprovedAdsEnabled': 'True',
                  'marketResearchEnabled': 'True',
                  'newsletterEnabled': 'True',
                  'promotionsEnabled': 'True'
              },
              'languagePreference': 'en_US',
              'primaryBusinessCategory': 'Technology: Commerce',
          }
    """
    self.__sanity_check.ValidateAccountInfoV13(acct_info)

    method_name = 'updateAccountInfo'
    if self.__config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name, (acct_info))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      self.__service.CallMethod(method_name, (({'accountInfo': acct_info},)),
                                'Account', self.__loc, request)
