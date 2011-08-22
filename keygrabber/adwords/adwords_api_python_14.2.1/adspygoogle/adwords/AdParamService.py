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

"""Methods to access AdParamService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.ApiService import ApiService


class AdParamService(ApiService):

  """Wrapper for AdParamService.

  The AdParamService service provides operations for accessing, creating,
  modifying, and removing ad parameters.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits AdParamService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['group'],
           op_config['version'], self.__class__.__name__]
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(AdParamService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def Get(self, selector):
    """Return a list of ad params.

    List of ad params specified by the selector from the customer's account.

    Args:
      selector: dict Filter to run ad params through.

    Returns:
      tuple List of ad params meeting all the criteria of the selector.
    """
    method_name = 'getAdParam'
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, selector, 'AdParamSelector')

    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'selector', self._wsdl_types_map, False, 'AdParamSelector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'AdParamSelector', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'AdParam', self._loc, request)

  def Mutate(self, ops):
    """Create, update, or remove ad params.

    Args:
      ops: list Unique operations.

    Returns:
      tuple Mutated ad params.
    """
    method_name = 'mutateAdParam'
    SanityCheck.ValidateTypes(((ops, list),))
    for op in ops:
      SanityCheck.NewSanityCheck(self._wsdl_types_map, op, 'AdParamOperation')

    if self._config['soap_lib'] == SOAPPY:
      new_ops = []
      for op in ops:
        new_ops.append(self._message_handler.PackVarAsXml(
            op, 'operations', self._wsdl_types_map, False, 'AdParamOperation'))
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (''.join(new_ops)))
    elif self._config['soap_lib'] == ZSI:
      new_ops = []
      for op in ops:
        new_ops.append(self._transformation.MakeZsiCompatible(
            op, 'AdParamOperation', self._wsdl_types_map,
            self._web_services))
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'operations': new_ops},)),
                                       'AdParam', self._loc, request)
