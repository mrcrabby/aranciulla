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

"""Methods to access AccountService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService


class AccountService(ApiService):

  """Wrapper for AccountService.

  The AccountService service allows you to modify AdWords accounts, such as
  changing targeting, business category, and email preferences for existing
  accounts.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits AccountService.

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
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(AccountService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def GetAccountInfo(self):
    """Return the AdWords account specified by the client account header.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAccountInfo'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self._loc,
                                       request)

  def GetClientAccountInfos(self):
    """Get the client account info for managed clients of effective user.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getClientAccountInfos'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self._loc,
                                       request)

  def GetClientAccounts(self):
    """Get the primary login for each account managed by the effective user.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getClientAccounts'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self._loc,
                                       request)

  def GetMccAlerts(self):
    """Retrieve the MCC alerts.

    The alerts are associated with any of the accounts beneath the current
    account.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getMccAlerts'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Account', self._loc,
                                       request)

  def UpdateAccountInfo(self, acct_info):
    """Update the account to reflect the changes in the account object.

    Args:
      acct_info: dict AccountInfo object with updated values.
    """
    self._sanity_check.ValidateAccountInfoV13(acct_info)

    method_name = 'updateAccountInfo'
    if self._config['soap_lib'] == SOAPPY:
      self.__service.CallMethod(method_name, (acct_info))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      self.__service.CallMethod(method_name, (({'accountInfo': acct_info},)),
                                'Account', self._loc, request)
