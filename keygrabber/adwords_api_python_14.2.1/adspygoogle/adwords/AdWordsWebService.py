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

"""Methods for sending and recieving SOAP XML requests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import re
import time

from adspygoogle.adwords import AdWordsSanityCheck
from adspygoogle.adwords import AUTH_TOKEN_EXPIRE
from adspygoogle.adwords import AUTH_TOKEN_SERVICE
from adspygoogle.adwords import LIB_SIG
from adspygoogle.adwords import LIB_URL
from adspygoogle.adwords import OPERATIONS_MAP
from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsErrors import ERRORS
from adspygoogle.adwords.AdWordsErrors import AdWordsApiError
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.AdWordsSoapBuffer import AdWordsSoapBuffer
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common.Errors import Error
from adspygoogle.common.Errors import ValidationError
from adspygoogle.common.WebService import WebService


class AdWordsWebService(WebService):

  """Implements AdWordsWebService.

  Responsible for sending and recieving SOAP XML requests.
  """

  def __init__(self, headers, config, op_config, url, lock, logger=None):
    """Inits AdWordsWebService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      url: str URL of the web service to call.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger
    """
    self.__config = config
    self.__service = url.split('/')[-1]
    super(AdWordsWebService, self).__init__(LIB_SIG, headers, config, op_config,
                                            url, lock, logger)

  def __ManageSoap(self, buf, start_time, stop_time, error={}):
    """Manage SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      start_time: str Time before service call was invoked.
      stop_time: str Time after service call was invoked.
      [optional]
      error: dict Error, if any.
    """
    try:
      # Update the number of units and operations consumed by API call.
      if buf.GetCallUnits() and buf.GetCallOperations():
        self._config['units'][0] += int(buf.GetCallUnits())
        self._config['operations'][0] += int(buf.GetCallOperations())
        self._config['last_units'][0] = int(buf.GetCallUnits())
        self._config['last_operations'][0] = int(buf.GetCallOperations())

      # Set up log handlers.
      handlers = [
          {
              'tag': 'xml_log',
              'name': 'soap_xml',
              'data': ''
          },
          {
              'tag': 'request_log',
              'name': 'request_info',
              'data': str('host=%s service=%s method=%s operator=%s '
                          'responseTime=%s operations=%s units=%s requestId=%s'
                          % (Utils.GetNetLocFromUrl(self._url),
                             buf.GetServiceName(), buf.GetCallName(),
                             buf.GetOperatorName(), buf.GetCallResponseTime(),
                             buf.GetCallOperations(), buf.GetCallUnits(),
                             buf.GetCallRequestId()))
          },
          {
              'tag': '',
              'name': 'adwords_api_lib',
              'data': ''
          }
      ]

      fault = super(AdWordsWebService, self)._ManageSoap(
          buf, handlers, LIB_URL, ERRORS, start_time, stop_time, error)
      if fault:
        # Raise a specific error, subclass of AdWordsApiError.
        if 'detail' in fault:
          if 'code' in fault['detail']:
            code = int(fault['detail']['code'])
            if code in ERRORS: raise ERRORS[code](fault)
          elif 'errors' in fault['detail']:
            type = fault['detail']['errors'][0]['type']
            if type in ERRORS: raise ERRORS[str(type)](fault)

        if isinstance(fault, str):
          raise AdWordsError(fault)
        elif isinstance(fault, dict):
          raise AdWordsApiError(fault)
    except AdWordsApiError, e:
      raise e
    except AdWordsError, e:
      raise e
    except Error, e:
      if error: e = error
      raise Error(e)

  def _GetServiceName(self):
    return self.__service

  def CallMethod(self, method_name, params, service_name=None, loc=None,
                 request=None):
    """Make an API call to specified method.

    Args:
      method_name: str API method name.
      params: list List of parameters to send to the API method.
      [optional]
      service_name: str API service name.
      loc: service Locator.
      request: instance Holder of the SOAP request.

    Returns:
      tuple/str Response from the API method. If 'raw_response' flag enabled a
                string is returned, tuple otherwise.
    """
    # Acquire thread lock.
    self._lock.acquire()

    try:
      if not service_name and self.__service:
        service_name = self.__service
      headers = self._headers
      config = self._config
      config['data_injects'] = ()
      error = {}

      # Load/unload version specific authentication and configuration data.
      if AdWordsSanityCheck.IsJaxbApi(self._op_config['version']):
        # Set boolean to the format expected by the server, True => true.
        for key in ['validateOnly', 'partialFailure']:
          if key in self._headers:
            self._headers[key] = self._headers[key].lower()

        # Load/set authentication token. If authentication token has expired,
        # regenerate it.
        now = time.time()
        if ((('authToken' not in headers and
              'auth_token_epoch' not in config) or
             int(now - config['auth_token_epoch']) >= AUTH_TOKEN_EXPIRE) and
            not 'oauth_enabled' in config):
          if ('email' not in headers or not headers['email'] or
              'password' not in headers or not headers['password']):
            msg = ('Required authentication headers, \'email\' and '
                   '\'password\', are missing. Unable to regenerate '
                   'authentication token.')
            raise ValidationError(msg)
          headers['authToken'] = Utils.GetAuthToken(
              headers['email'], headers['password'], AUTH_TOKEN_SERVICE,
              LIB_SIG, config['proxy'])
          config['auth_token_epoch'] = time.time()
          self._headers = headers
          self._config = config
        headers = Utils.UnLoadDictKeys(headers,
                                       ['email', 'password', 'useragent'])
        ns = '/'.join(['https://adwords.google.com/api/adwords',
                       self._op_config['group'], self._op_config['version']])
        default_ns = '/'.join(['https://adwords.google.com/api/adwords',
                               self._op_config['default_group'],
                               self._op_config['version']])
        config['ns_target'] = (ns, 'RequestHeader')

        if (config['soap_lib'] == SOAPPY and
            (self._op_config['default_group'] != self._op_config['group'] or
             self.__service == 'BulkMutateJobService')):
          from adspygoogle.adwords.soappy import SERVICE_TYPES
          data_injects = []
          for header in headers:
            if headers[header]: data_injects.append((header, 'ns1:%s' % header))
          data_injects.append(
              ('<RequestHeader>', '<RequestHeader xmlns="%s" xmlns:ns1="%s">'
               % (ns, default_ns)))
          data_injects.append(
              ('<SOAP-ENV:Body xmlns="%s">' % ns,
               '<SOAP-ENV:Body xmlns="%s" xmlns:ns1="%s">' % (ns, default_ns)))
          for item in SERVICE_TYPES:
            if (item['group'] == self._op_config['default_group'] and
                re.compile('<%s>|<%s ' % (item['attr'],
                                          item['attr'])).findall(params)):
              # TODO(api.sgrinberg): Find a more elegant solution that doesn't
              # involve manual triggering for attributes that show up in both
              # groups.
              if ((self._op_config['group'] == 'o' and
                   item['attr'] == 'urls') or
                  (self.__service == 'TrafficEstimatorService' and
                   item['attr'] == 'maxCpc')
                  or item['attr'] == 'selector' or item['attr'] == 'operator'):
                continue
              if self.__service != 'BulkMutateJobService':
                data_injects.append((' xsi3:type="%s">' % item['type'], '>'))
              data_injects.append(('<%s>' % item['attr'],
                                   '<ns1:%s>' % item['attr']))
              data_injects.append(('<%s ' % item['attr'],
                                   '<ns1:%s ' % item['attr']))
              data_injects.append(('</%s>' % item['attr'],
                                   '</ns1:%s>' % item['attr']))
          config['data_injects'] = tuple(data_injects)
      else:
        headers['useragent'] = headers['userAgent']
        headers = Utils.UnLoadDictKeys(headers, ['authToken', 'userAgent'])
        config = Utils.UnLoadDictKeys(config, ['ns_target',
                                               'auth_token_epoch'])

      buf = AdWordsSoapBuffer(
          xml_parser=self._config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(self._config['pretty_xml']))

      start_time = time.strftime('%Y-%m-%d %H:%M:%S')
      response = super(AdWordsWebService, self).CallMethod(
          headers, config, method_name, params, buf,
          AdWordsSanityCheck.IsJaxbApi(self._op_config['version']), LIB_SIG,
          LIB_URL, service_name, loc, request)
      stop_time = time.strftime('%Y-%m-%d %H:%M:%S')

      # Restore list type which was overwritten by SOAPpy.
      if config['soap_lib'] == SOAPPY and isinstance(response, tuple):
        from adspygoogle.common.soappy import MessageHandler
        holder = []
        for element in response:
          holder.append(MessageHandler.RestoreListType(
              element, ('value', 'partialFailureErrors', 'conversionTypes')))
        response = tuple(holder)

      if isinstance(response, dict) or isinstance(response, Error):
        error = response

      if not Utils.BoolTypeConvert(self.__config['raw_debug']):
        self.__ManageSoap(buf, start_time, stop_time, error)
    finally:
      # Release thread lock.
      if self._lock.locked():
        self._lock.release()

    if Utils.BoolTypeConvert(self._config['raw_response']):
      return response
    return response

  def CallRawMethod(self, soap_message):
    """Make an API call by posting raw SOAP XML message.

    Args:
      soap_message: str SOAP XML message.

    Returns:
      tuple Response from the API method.
    """
    # Acquire thread lock.
    self._lock.acquire()

    try:
      buf = AdWordsSoapBuffer(
          xml_parser=self._config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(self._config['pretty_xml']))

      super(AdWordsWebService, self).CallRawMethod(
          buf, Utils.GetNetLocFromUrl(self._op_config['server']), soap_message)

      self.__ManageSoap(buf, self._start_time, self._stop_time,
                        {'data': buf.GetBufferAsStr()})
    finally:
      # Release thread lock.
      if self._lock.locked():
        self._lock.release()
    return (self._response,)
