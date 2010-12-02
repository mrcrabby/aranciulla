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

"""Methods to access AdGroupCriterionService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from aw_api import SanityCheck as glob_sanity_check
from aw_api import SOAPPY
from aw_api import ZSI
from aw_api.Errors import ValidationError
from aw_api.WebService import WebService


class AdGroupCriterionService(object):

  """Wrapper for AdGroupCriterionService.

  The AdGroupCriterion Service provides operations for accessing, modifying,
  and creating criteria (Keywords and Websites) at AdGroup level.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits AdGroupCriterionService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock the thread lock.
      logger: Logger the instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['group'],
           op_config['version'], self.__class__.__name__]
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

  def Get(self, selector):
    """Return a list of ad group criteria.

    List of ad group criteria specified by the selector from the customer's
    account.

    Args:
      selector: dict filter to run ad group criteria through.

    Returns:
      tuple list of ad group criteria meeting all the criteria of the selector.
    """
    method_name = 'getAdGroupCriterion'
    if self.__config['soap_lib'] == SOAPPY:
      self.__sanity_check.ValidateSelector(selector)
      selector = self.__message_handler.PackDictAsXml(
          selector, 'selector',
          ['idFilters', 'criterionUse', 'userStatuses', 'statsSelector',
           'paging'])
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      self.__sanity_check.ValidateSelector(selector, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'AdGroupCriterion', self.__loc, request)

  def Mutate(self, ops):
    """Add, update, or remove ad group criteria.

    Args:
      ops: list unique operations.

    Returns:
      tuple mutated ad group criteria.
    """
    method_name = 'mutateAdGroupCriterion'
    if self.__config['soap_lib'] == SOAPPY:
      glob_sanity_check.ValidateTypes(((ops, list),))
      new_ops = []
      for op in ops:
        self.__sanity_check.ValidateOperation(op)
        new_ops.append(self.__message_handler.PackDictAsXml(
            op, 'operations', ['operator', 'operand','exemptionRequests']))
      ops = ''.join(new_ops)
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (ops))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      glob_sanity_check.ValidateTypes(((ops, list),))
      for op in ops:
        op = self.__sanity_check.ValidateOperation(op, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'operations': ops},)),
                                       'AdGroupCriterion', self.__loc, request)
