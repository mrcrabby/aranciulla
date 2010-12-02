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

"""Methods to access ReportDefinitionService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import httplib
import os

from aw_api import SOAPPY
from aw_api import ZSI
from aw_api import SanityCheck as glob_sanity_check
from aw_api import Utils
from aw_api.Errors import ValidationError
from aw_api.WebService import WebService


class ReportDefinitionService(object):

  """Wrapper for ReportDefinitionService.

  The ReportDefinition Service provides operations for accessing, modifying,
  and creating report definitions.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits ReportDefinitionService.

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
    self.__headers = headers
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
    """Return a list of report definitions.

    Args:
      selector: dict filter to run report definitions through.

    Returns:
      tuple list of report definitions meeting all the criteria of the selector.
    """
    method_name = 'getReportDefinition'
    if self.__config['soap_lib'] == SOAPPY:
      self.__sanity_check.ValidateSelector(selector)
      selector = self.__message_handler.PackDictAsXml(
          selector, 'selector', [])
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      self.__sanity_check.ValidateSelector(selector, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'ReportDefinition', self.__loc, request)

  def GetReportFields(self, report_type):
    """Return a list of supported report fields.

    Args:
      report_type: str type of the report.

    Returns:
      tuple list of report fields.
    """
    glob_sanity_check.ValidateTypes(((report_type, str),))

    method_name = 'getReportFields'
    if self.__config['soap_lib'] == SOAPPY:
      report_type = self.__message_handler.PackDictAsXml(
          report_type, 'reportType', [])
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (report_type))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportType': report_type},)),
                                       'ReportDefinition', self.__loc, request)

  def Mutate(self, ops):
    """Create, update, or remove a report.

    Args:
      ops: list unique operations.

    Returns:
      tuple mutated reports.
    """
    method_name = 'mutateReportDefinition'
    if self.__config['soap_lib'] == SOAPPY:
      glob_sanity_check.ValidateTypes(((ops, list),))
      new_ops = []
      for op in ops:
        self.__sanity_check.ValidateOperation(op)
        new_ops.append(self.__message_handler.PackDictAsXml(
            op, 'operations', ['operator', 'operand']))
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
                                       'ReportDefinition', self.__loc, request)

  def DownloadReport(self, report_definition_id, path=None):
    """Download report and either return raw data or save it into a file.

    Args:
      report_definition_id: str Id of the report definition to download.
      path: str Path of the file to save the report data into.

    Returns:
      str Report data, if path was not specified.
    """
    selector = '/api/adwords/reportdownload?__rd=%s' % report_definition_id
    clientId = {}
    if 'clientEmail' in self.__headers:
      clientId['clientEmail'] = self.__headers['clientEmail']
    elif 'clientCustomerId' in self.__headers:
      clientId['clientCustomerId'] = self.__headers['clientCustomerId']

    # Download report data.
    conn = httplib.HTTPSConnection(
        Utils.GetNetLocFromUrl(self.__op_config['server']))
    conn.connect()
    conn.putrequest('GET', selector)
    conn.putheader('Authorization',
                   'GoogleLogin auth=%s' % self.__headers['authToken'])
    conn.putheader(clientId.keys()[0], clientId[clientId.keys()[0]])
    conn.endheaders()
    data = conn.getresponse().read()

    if not path: return data

    # Write data to a file.
    fh = open(path, 'w')
    try:
      fh.write(data)
    finally:
      fh.close()
