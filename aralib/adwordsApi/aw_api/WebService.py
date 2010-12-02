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

"""Methods for sending and recieving SOAP XML requests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import httplib
import sys
import time

from aw_api import AUTH_TOKEN_EXPIRE
from aw_api import LIB_SHORT_NAME
from aw_api import LIB_URL
from aw_api import LIB_VERSION
from aw_api import SOAPPY
from aw_api import ZSI
from aw_api import SanityCheck
from aw_api import Utils
from aw_api.Errors import ERRORS
from aw_api.Errors import ApiError
from aw_api.Errors import AuthTokenError
from aw_api.Errors import Error
from aw_api.Errors import ValidationError
from aw_api.Logger import Logger
from aw_api.SoapBuffer import SoapBuffer


class WebService(object):

  """Implements WebService.

  Responsible for sending and recieving SOAP XML requests.
  """

  def __init__(self, headers, config, op_config, url, lock, logger=None):
    """Inits WebService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      url: str url of the web service to call.
      lock: thread.lock the thread lock.
      logger: Logger the instance of Logger
    """
    self.__headers = headers
    self.__config = config
    self.__op_config = op_config
    self.__url = url
    self.__lock = lock
    self.__logger = logger

    if self.__logger is None:
      self.__logger = Logger(self.__config['log_home'])

    if (self.__config['soap_lib'] == SOAPPY and
        self.__headers.values().count(None) < 2 and
        (len(self.__headers.values()) > len(set(self.__headers.values())) and
         not self.__headers.has_key('useragent'))):
      if self.__headers.values().count('') < 2:
        msg = ('Two (or more) values in \'headers\' dict can not be the same. '
               'See, %s/issues/detail?id=27.' % LIB_URL)
        raise ValidationError(msg)
      else:
        self.__headers = {}
        for key in headers:
          if headers[key]: self.__headers[key] = headers[key]

  def __ManageSoap(self, buf, start_time, stop_time, error={}):
    """Manage SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      start_time: str time before service call was invoked.
      stop_time: str time after service call was invoked.
      [optional]
      error: dict error, if any.
    """
    # Update the number of units and operations consumed by API call.
    if buf.GetCallUnits() and buf.GetCallOperations():
      self.__config['units'][0] += int(buf.GetCallUnits())
      self.__config['operations'][0] += int(buf.GetCallOperations())
      self.__config['last_units'][0] = int(buf.GetCallUnits())
      self.__config['last_operations'][0] = int(buf.GetCallOperations())

    # Load trace errors, if any.
    if error and 'trace' in error:
      error_msg = error['trace']
    else:
      error_msg = ''

    # Check if response was successful or not.
    if error and 'data' in error:
      is_fault = True
    else:
      is_fault = False

    # Forward SOAP XML, errors, and other debugging data to console, external
    # file, both, or ignore. Each handler supports the following elements,
    #   tag: Config value for this handler. If left empty, will never write
    #        data to file.
    #   target: Target/destination represented by this handler (i.e. FILE,
    #           CONSOLE, etc.). Initially, it should be set to Logger.NONE.
    #   name: Name of the log file to use.
    #   data: Data to write.
    handlers = [
        {'tag': 'xml_log',
         'target': Logger.NONE,
         'name': 'soap_xml',
         'data': str('StartTime: %s\n%s\n%s\n%s\n%s\nEndTime: %s'
                     % (start_time, buf.GetHeadersOut(), buf.GetSOAPOut(),
                        buf.GetHeadersIn(), buf.GetSOAPIn(), stop_time))},
        {'tag': 'request_log',
         'target': Logger.NONE,
         'name': 'request_info',
         'data': str('host=%s service=%s method=%s operator=%s responseTime=%s '
                     'operations=%s units=%s requestId=%s isFault=%s'
                     % (Utils.GetNetLocFromUrl(self.__url),
                        buf.GetServiceName(), buf.GetCallName(),
                        buf.GetOperatorName(), buf.GetCallResponseTime(),
                        buf.GetCallOperations(), buf.GetCallUnits(),
                        buf.GetCallRequestId(), is_fault))},
        {'tag': '',
         'target': Logger.NONE,
         'name': 'aw_api_lib',
         'data': 'DEBUG: %s' % error_msg}
    ]
    for handler in handlers:
      if (handler['tag'] and
          Utils.BoolTypeConvert(self.__config[handler['tag']])):
        handler['target'] = Logger.FILE
      # If debugging is On, raise handler's target two levels,
      #   NONE -> CONSOLE
      #   FILE -> FILE_AND_CONSOLE.
      if Utils.BoolTypeConvert(self.__config['debug']):
        handler['target'] += 2

      if (handler['target'] != Logger.NONE and handler['data'] and
          handler['data'] != 'None' and handler['data'] != 'DEBUG: '):
        self.__logger.Log(handler['name'], handler['data'],
                          log_level=Logger.DEBUG, log_handler=handler['target'])

    # If raw response is requested, no need to validate and throw appropriate
    # error. Up to the end user to handle successful or failed request.
    if Utils.BoolTypeConvert(self.__config['raw_response']):
      return

    # Report SOAP fault.
    if is_fault:
      try:
        fault = buf.GetFaultAsDict()
        if not fault:
          msg = error['data']
      except:
        fault = None
        # An error is not a SOAP fault, but check if some other error.
        if error_msg:
          msg = error_msg
        else:
          msg = ('Unable to parse incoming SOAP XML. Please, file '
                 'a bug at %s/issues/list.' % LIB_URL)
      # Release thread lock.
      if self.__lock.locked():
        self.__lock.release()
      if not fault and msg:
        raise Error(msg)

      # Raise a specific error, subclass of ApiError.
      if 'detail' in fault:
        if 'code' in fault['detail']:
          code = int(fault['detail']['code'])
          if code in ERRORS:
            raise ERRORS[code](fault)
        elif 'errors' in fault['detail']:
          type = fault['detail']['errors'][0]['type']
          if type in ERRORS:
            raise ERRORS[str(type)](fault)
      raise ApiError(fault)

  def CallMethod(self, method_name, params, service_name=None, loc=None,
                 request=None):
    """Make an API call to specified method.

    Args:
      method_name: str API method name.
      params: list list of parameters to send to the API method.
      [optional]
      service_name: str API service name.
      loc: service locator.
      request: instance holder of the SOAP request.

    Returns:
      tuple/str response from the API method. If 'raw_response' flag enabled a
                string is returned, tuple otherwise.
    """
    # Acquire thread lock.
    self.__lock.acquire()

    try:
      headers = self.__headers
      config = self.__config

      # Temporarily redirect HTTP headers and SOAP from STDOUT into a buffer.
      buf = SoapBuffer(
          xml_parser=config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(config['use_pretty_xml']))
      old_stdout = sys.stdout
      sys.stdout = buf

      start_time = time.strftime('%Y-%m-%d %H:%M:%S')
      response = ()
      raw_response = ''
      error = {}
      try:
        if Utils.BoolTypeConvert(config['use_strict']):
          SanityCheck.ValidateHeadersForServer(headers,
                                               self.__op_config['server'])

        # Load/unload version specific authentication and configuration data.
        if SanityCheck.IsNewApi(self.__op_config['version']):
          # Set boolean to the format expected by the server, True => true.
          if 'validateOnly' in headers:
            headers['validateOnly'] = headers['validateOnly'].lower()

          # Load/set authentication token. If authentication token has expired,
          # regenerate it.
          now = time.time()
          if (Utils.BoolTypeConvert(config['use_auth_token']) and
              (('authToken' not in headers and
                'auth_token_epoch' not in config) or
               int(now - config['auth_token_epoch']) >= AUTH_TOKEN_EXPIRE)):
            if ('email' not in headers or not headers['email'] or
                'password' not in headers or not headers['password']):
              msg = ('Required authentication headers, \'email\' and '
                     '\'password\', are missing. Unable to regenerate '
                     'authentication token.')
              raise ValidationError(msg)
            headers['authToken'] = Utils.GetAuthToken(headers['email'],
                                                      headers['password'])
            config['auth_token_epoch'] = time.time()
            self.__headers = headers
            self.__config = config
          elif not Utils.BoolTypeConvert(config['use_auth_token']):
            msg = ('Requests via %s require use of authentication token.'
                   % self.__op_config['version'])
            raise ValidationError(msg)

          headers = Utils.UnLoadDictKeys(Utils.CleanUpDict(headers),
                                         ['email', 'password'])
          name_space = '/'.join(['https://adwords.google.com/api/adwords',
                                 self.__op_config['group'],
                                 self.__op_config['version']])
          config['ns_target'] = (name_space, 'RequestHeader')
        else:
          headers['useragent'] = headers['userAgent']
          headers = Utils.UnLoadDictKeys(headers, ['authToken', 'userAgent'])
          config = Utils.UnLoadDictKeys(config, ['ns_target',
                                                 'auth_token_epoch'])

        # Fire off API request and handle the response.
        if config['soap_lib'] == SOAPPY:
          from aw_api.soappy_toolkit import MessageHandler
          service = MessageHandler.GetServiceConnection(
              headers, config, self.__url, self.__op_config['http_proxy'],
              self.__op_config['version'])

          if not SanityCheck.IsNewApi(self.__op_config['version']):
            response = MessageHandler.UnpackResponseAsDict(
                service.invoke(method_name, params))
          else:
            response = MessageHandler.UnpackResponseAsDict(
                service._callWithBody(MessageHandler.SetRequestParams(
                    config, method_name, params)))
        elif config['soap_lib'] == ZSI:
          from aw_api.zsi_toolkit import MessageHandler
          service = MessageHandler.GetServiceConnection(
              headers, config, self.__url, self.__op_config['http_proxy'],
              service_name, loc)
          request = MessageHandler.SetRequestParams(self.__op_config, request,
                                                    params)

          response = MessageHandler.UnpackResponseAsTuple(
              eval('service.%s(request)' % method_name))

          # The response should always be tuple. If it's not, there must be
          # something wrong with MessageHandler.UnpackResponseAsTuple().
          if len(response) == 1 and isinstance(response[0], list):
            response = tuple(response[0])

        if isinstance(response, list):
          response = tuple(response)
        elif isinstance(response, tuple):
          pass
        else:
          if response:
            response = (response,)
          else:
            response = ()
      except Exception, e:
        error['data'] = e
      stop_time = time.strftime('%Y-%m-%d %H:%M:%S')

      # Restore STDOUT.
      sys.stdout = old_stdout

      # When debugging mode is ON, fetch last traceback.
      if Utils.BoolTypeConvert(self.__config['debug']):
        error['trace'] = Utils.LastStackTrace()

      # Catch local errors prior to going down to the SOAP layer, which may not
      # exist for this error instance.
      if 'data' in error and not buf.IsHandshakeComplete():
        # Check if buffer contains non-XML data, most likely an HTML page. This
        # happens in the case of 502 errors (and similar). Otherwise, this is a
        # local error and API request was never made.
        html_error = Utils.GetErrorFromHtml(buf.GetBufferAsStr())
        if html_error:
          msg = '%s' % html_error
        else:
          msg = str(error['data'])
          if Utils.BoolTypeConvert(self.__config['debug']):
            msg += '\n%s' % error['trace']

        # When debugging mode is ON, store the raw content of the buffer.
        if Utils.BoolTypeConvert(self.__config['debug']):
          error['raw_data'] = buf.GetBufferAsStr()

        # Catch errors from AuthToken and ValidationError levels, raised during
        # try/except above.
        if isinstance(error['data'], AuthTokenError):
          raise AuthTokenError(msg)
        elif isinstance(error['data'], ValidationError):
          raise ValidationError(error['data'])
        if 'raw_data' in error:
          msg = '%s [RAW DATA: %s]' % (msg, error['raw_data'])
        raise Error(msg)

      if Utils.BoolTypeConvert(self.__config['raw_response']):
        raw_response = buf.GetRawSOAPIn()

      self.__ManageSoap(buf, start_time, stop_time, error)
    finally:
      # Release thread lock.
      if self.__lock.locked():
        self.__lock.release()

    if Utils.BoolTypeConvert(self.__config['raw_response']):
      return raw_response

    return response

  def CallRawMethod(self, soap_message):
    """Make an API call by posting raw SOAP XML message.

    Args:
      soap_message: str SOAP XML message.

    Returns:
      tuple response from the API method.
    """
    # Acquire thread lock.
    self.__lock.acquire()

    try:
      buf = SoapBuffer(
          xml_parser=self.__config['xml_parser'],
          pretty_xml=Utils.BoolTypeConvert(self.__config['use_pretty_xml']))
      http_header = {
          'post': '%s' % self.__url,
          'host': 'sandbox.google.com',
          'user_agent': '%s v%s; WebService.py' % (LIB_SHORT_NAME, LIB_VERSION),
          'content_type': 'text/xml; charset=\"UTF-8\"',
          'content_length': '%d' % len(soap_message),
          'soap_action': ''
      }

      version = self.__url.split('/')[-2]
      if SanityCheck.IsNewApi(version):
        http_header['host'] = 'adwords-%s' % http_header['host']

      index = self.__url.find('adwords.google.com')
      if index > -1:
        http_header['host'] = 'adwords.google.com'

      self.__url = ''.join(['https://', http_header['host'], self.__url])

      start_time = time.strftime('%Y-%m-%d %H:%M:%S')
      buf.write(
          ('%s Outgoing HTTP headers %s\nPOST %s\nHost: %s\nUser-Agent: '
           '%s\nContent-type: %s\nContent-length: %s\nSOAPAction: %s\n%s\n%s '
           'Outgoing SOAP %s\n%s\n%s\n' % ('*'*3, '*'*46, http_header['post'],
                                           http_header['host'],
                                           http_header['user_agent'],
                                           http_header['content_type'],
                                           http_header['content_length'],
                                           http_header['soap_action'], '*'*72,
                                           '*'*3, '*'*54, soap_message,
                                           '*'*72)))

      # Construct header and send SOAP message.
      web_service = httplib.HTTPS(http_header['host'])
      web_service.putrequest('POST', http_header['post'])
      web_service.putheader('Host', http_header['host'])
      web_service.putheader('User-Agent', http_header['user_agent'])
      web_service.putheader('Content-type', http_header['content_type'])
      web_service.putheader('Content-length', http_header['content_length'])
      web_service.putheader('SOAPAction', http_header['soap_action'])
      web_service.endheaders()
      web_service.send(soap_message)

      # Get response.
      status_code, status_message, header = web_service.getreply()
      response = web_service.getfile().read()

      header = str(header).replace('\r', '')
      buf.write(('%s Incoming HTTP headers %s\n%s %s\n%s\n%s\n%s Incoming SOAP'
                 ' %s\n%s\n%s\n' % ('*'*3, '*'*46, status_code, status_message,
                                    header, '*'*72, '*'*3, '*'*54, response,
                                    '*'*72)))
      stop_time = time.strftime('%Y-%m-%d %H:%M:%S')

      # Catch local errors prior to going down to the SOAP layer, which may not
      # exist for this error instance.
      if not buf.IsHandshakeComplete() or not buf.IsSoap():
        # The buffer contains non-XML data, most likely an HTML page. This
        # happens in the case of 502 errors.
        html_error = Utils.GetErrorFromHtml(buf.GetBufferAsStr())
        if html_error:
          msg = '%s' % html_error
        else:
          msg = 'Unknown error.'
        raise Error(msg)

      self.__ManageSoap(buf, start_time, stop_time,
                        {'data': buf.GetBufferAsStr()})
    finally:
      # Release thread lock.
      if self.__lock.locked():
        self.__lock.release()

    return (response,)
