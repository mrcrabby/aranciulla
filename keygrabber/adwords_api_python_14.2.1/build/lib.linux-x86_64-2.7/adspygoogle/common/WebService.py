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

"""Methods for sending and recieving SOAP XML requests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import httplib
import sys
import time

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import Utils
from adspygoogle.common.Logger import Logger
from adspygoogle.common.Errors import AuthTokenError
from adspygoogle.common.Errors import Error
from adspygoogle.common.Errors import ValidationError


class WebService(object):

  """Implements WebService.

  Responsible for sending and recieving SOAP XML requests.
  """

  def __init__(self, lib_sig, headers, config, op_config, url, lock,
               logger=None):
    """Inits WebService.

    Args:
      lib_sig: str Client library signature.
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values
                 for this operation.
      url: str URL of the web service to call.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger.
    """
    self._lib_sig = lib_sig
    self._headers = headers
    self._config = config
    self._op_config = op_config
    self._url = url
    self._lock = lock
    self._logger = logger
    self._start_time = 0
    self._stop_time = 0
    self._response = None

    if self._logger is None:
      self._logger = Logger(lib_sig, self._config['log_home'])

  def _ManageSoap(self, buf, log_handlers, lib_url, errors, start_time,
                  stop_time, error={}):
    """Manage SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      log_handlers: list Log handlers.
      lib_url: str URL of the project's home.
      errors: dict Map of errors available for the API.
      start_time: str Time before service call was invoked.
      stop_time: str Time after service call was invoked.
      [optional]
      error: dict Error, if any.
    """
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
    for handler in log_handlers:
      if handler['tag'] == 'xml_log':
        handler['target'] = Logger.NONE
        handler['data'] += str(
            'StartTime: %s\n%s\n%s\n%s\n%s\nEndTime: %s'
            % (start_time, buf.GetHeadersOut(), buf.GetSoapOut(),
               buf.GetHeadersIn(), buf.GetSoapIn(), stop_time))
      elif handler['tag'] == 'request_log':
        handler['target'] = Logger.NONE
        handler['data'] += ' isFault=%s' % is_fault
      elif handler['tag'] == '':
        handler['target'] = Logger.NONE
        handler['data'] += 'DEBUG: %s' % error_msg
    for handler in log_handlers:
      if (handler['tag'] and
          Utils.BoolTypeConvert(self._config[handler['tag']])):
        handler['target'] = Logger.FILE
      # If debugging is On, raise handler's target two levels,
      #   NONE -> CONSOLE
      #   FILE -> FILE_AND_CONSOLE.
      if Utils.BoolTypeConvert(self._config['debug']):
        handler['target'] += 2

      if (handler['target'] != Logger.NONE and handler['data'] and
          handler['data'] != 'None' and handler['data'] != 'DEBUG: '):
        self._logger.Log(handler['name'], handler['data'],
                         log_level=Logger.DEBUG, log_handler=handler['target'])

    # If raw response is requested, no need to validate and throw appropriate
    # error. Up to the end user to handle successful or failed request.
    if Utils.BoolTypeConvert(self._config['raw_response']): return

    # Report SOAP fault.
    if is_fault:
      try:
        fault = buf.GetFaultAsDict()
        if not fault: msg = error['data']
      except:
        fault = None
        # An error is not a SOAP fault, but check if some other error.
        if error_msg:
          msg = error_msg
        else:
          msg = ('Unable to parse incoming SOAP XML. Please, file '
                 'a bug at %s/issues/list.' % lib_url)
      # Release thread lock.
      if self._lock.locked(): self._lock.release()
      if not fault and msg: return msg
      return fault
    return None

  def CallMethod(self, headers, config, method_name, params, buf, is_jaxb_api,
                 lib_sig, lib_url, service_name=None, loc=None, request=None):
    """Make an API call to specified method.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      method_name: str API method name.
      params: list List of parameters to send to the API method.
      buf: SoapBuffer SOAP buffer.
      is_jaxb_api: str Whether API uses JAXB.
      lib_sig: str Signature of the client library.
      lib_url: str URL of the project's home.
      [optional]
      service_name: str API service name.
      loc: Service locator.
      request: instance Holder of the SOAP request.

    Returns:
      tuple/str Response from the API method. If 'raw_response' flag enabled a
                string is returned, tuple otherwise.
    """
    # Temporarily redirect HTTP headers and SOAP from STDOUT into a buffer.
    if not Utils.BoolTypeConvert(self._config['raw_debug']):
      old_stdout = sys.stdout
      sys.stdout = buf

    response = ()
    error = {}
    try:
      # Fire off API request and handle the response.
      if config['soap_lib'] == SOAPPY:
        from adspygoogle.common.soappy import MessageHandler
        service = MessageHandler.GetServiceConnection(
            headers, config, self._url, self._op_config['http_proxy'],
            is_jaxb_api)

        if not is_jaxb_api:
          response = MessageHandler.UnpackResponseAsDict(
              service.invoke(method_name, params))
        else:
          if not params: params = ('')
          response = MessageHandler.UnpackResponseAsDict(
              service._callWithBody(MessageHandler.SetRequestParams(
                  config, method_name, params)))
      elif config['soap_lib'] == ZSI:
        from adspygoogle.common.zsi import MessageHandler
        service = MessageHandler.GetServiceConnection(
            headers, config, self._op_config, self._url, service_name, loc)
        request = MessageHandler.SetRequestParams(request, params, is_jaxb_api)

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

    # Restore STDOUT.
    if not Utils.BoolTypeConvert(self._config['raw_debug']):
      sys.stdout = old_stdout

    # When debugging mode is ON, fetch last traceback.
    if Utils.BoolTypeConvert(self._config['debug']):
      if Utils.LastStackTrace() and Utils.LastStackTrace() != 'None':
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
        if Utils.BoolTypeConvert(self._config['debug']):
          msg += '\n%s' % error['trace']

      # When debugging mode is ON, store the raw content of the buffer.
      if Utils.BoolTypeConvert(self._config['debug']):
        error['raw_data'] = buf.GetBufferAsStr()

      # Catch errors from AuthToken and ValidationError levels, raised during
      # try/except above.
      if isinstance(error['data'], AuthTokenError):
        raise AuthTokenError(msg)
      elif isinstance(error['data'], ValidationError):
        raise ValidationError(error['data'])
      if 'raw_data' in error:
        msg = '%s [RAW DATA: %s]' % (msg, error['raw_data'])
      return Error(msg)

    if Utils.BoolTypeConvert(self._config['raw_response']):
      response = buf.GetRawSOAPIn()
    if error: response = error
    return response

  def CallRawMethod(self, buf, host, soap_message):
    """Make an API call by posting raw SOAP XML message.

    Args:
      buf: SoapBuffer SOAP buffer.
      host: str Host against which to make API request.
      soap_message: str SOAP XML message.

    Returns:
      tuple Response from the API method.
    """
    http_header = {
        'post': '%s' % self._url,
        'host': host,
        'user_agent': '%s; WebService.py' % self._lib_sig,
        'content_type': 'text/xml; charset=\"UTF-8\"',
        'content_length': '%d' % len(soap_message),
        'soap_action': ''
    }

    self._start_time = time.strftime('%Y-%m-%d %H:%M:%S')
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
    self._response = web_service.getfile().read()

    header = str(header).replace('\r', '')
    buf.write(('%s Incoming HTTP headers %s\n%s %s\n%s\n%s\n%s Incoming SOAP'
               ' %s\n%s\n%s\n' % ('*'*3, '*'*46, status_code, status_message,
                                  header, '*'*72, '*'*3, '*'*54, self._response,
                                  '*'*72)))
    self._stop_time = time.strftime('%Y-%m-%d %H:%M:%S')

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
