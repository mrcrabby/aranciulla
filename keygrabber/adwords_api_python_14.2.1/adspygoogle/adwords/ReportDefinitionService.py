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

"""Methods to access ReportDefinitionService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import httplib
import re
import time
import urllib2
import xml.dom.minidom as minidom

from adspygoogle.adwords import AUTH_TOKEN_EXPIRE
from adspygoogle.adwords import AUTH_TOKEN_SERVICE
from adspygoogle.adwords import LIB_SIG
from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsErrors import AdWordsApiError
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils
from adspygoogle.common import ZSI

from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import ValidationError


REPORT_DOWNLOAD_URL = '/api/adwords/reportdownload?__rd=%s'
OLD_ERROR_REGEX = r'^!!!(\d+)\|\|\|(\d+)\|\|\|(.*)\?\?\?'
BUF_SIZE = 4096


class ReportDefinitionService(ApiService):

  """Wrapper for ReportDefinitionService.

  The ReportDefinitionService service provides operations for accessing,
  modifying, and creating report definitions.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits ReportDefinitionService.

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
    super(ReportDefinitionService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def Get(self, selector):
    """Return a list of report definitions.

    Args:
      selector: dict Filter to run report definitions through.

    Returns:
      tuple List of report definitions meeting all the criteria of the selector.
    """
    method_name = 'getReportDefinition'
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, selector, 'ReportDefinitionSelector')

    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'selector', self._wsdl_types_map, False,
          'ReportDefinitionSelector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'ReportDefinitionSelector', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'ReportDefinition', self._loc, request)

  def GetReportFields(self, report_type):
    """Return a list of supported report fields.

    Args:
      report_type: str Type of the report.

    Returns:
      tuple List of report fields.
    """
    SanityCheck.ValidateTypes(((report_type, str),))

    method_name = 'getReportFields'
    if self._config['soap_lib'] == SOAPPY:
      report_type = self._message_handler.PackVarAsXml(report_type,
                                                       'reportType')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (report_type))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportType': report_type},)),
                                       'ReportDefinition', self._loc, request)

  def Mutate(self, ops):
    """Create, update, or remove a report.

    Args:
      ops: list Unique operations.

    Returns:
      tuple Mutated reports.
    """
    method_name = 'mutateReportDefinition'
    SanityCheck.ValidateTypes(((ops, list),))
    for op in ops:
      SanityCheck.NewSanityCheck(
          self._wsdl_types_map, op, 'ReportDefinitionOperation')

    if self._config['soap_lib'] == SOAPPY:
      new_ops = []
      for op in ops:
        new_ops.append(self._message_handler.PackVarAsXml(
            op, 'operations', self._wsdl_types_map, False,
            'ReportDefinitionOperation'))
      ops = ''.join(new_ops)
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (ops))
    elif self._config['soap_lib'] == ZSI:
      for op in ops:
        op = self._transformation.MakeZsiCompatible(
            op, 'ReportDefinitionOperation', self._wsdl_types_map,
            self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'operations': ops},)),
                                       'ReportDefinition', self._loc, request)

  def DownloadReport(self, report_definition_id, return_micros=False):
    """Download report and return raw data.

    Args:
      report_definition_id: str Id of the report definition to download.
      return_micros: bool Whether to return currency in micros.

    Returns:
      str Report data.
    """
    self.__ReloadAuthToken()
    selector = self.__GenerateUrl(report_definition_id)
    headers = self.__GenerateHeaders(return_micros)
    response = self.__MakeRequest(selector, headers)
    return response['body']

  def __GenerateUrl(self, report_definition_id, query_token=None):
    """Generates the URL to get a report from.

    Args:
      report_definition_id: int ID of the report to download.
      query_token: str query token (if one is needed/exists).

    Returns:
      str url to request
    """
    url = REPORT_DOWNLOAD_URL % report_definition_id
    if query_token:
      url += ('&qt=%s' % query_token)
    return url

  def __GenerateHeaders(self, return_micros):
    """Generates the headers to use for the report download.

    Args:
      return_micros: bool whether or not to use micros for money.

    Returns:
      dict Dictionary containing all the headers for the request
    """
    headers = {}
    if ('clientEmail' in self.__service._headers and
        self.__service._headers['clientEmail']):
      headers['clientEmail'] = self.__service._headers['clientEmail']
    elif 'clientCustomerId' in self.__service._headers:
      headers['clientCustomerId'] = self.__service._headers['clientCustomerId']

    headers['Authorization'] = ('GoogleLogin auth=%s' %
                                self.__service._headers['authToken'].strip())
    headers['returnMoneyInMicros'] = str(return_micros).lower()
    return headers

  def __MakeRequest(self, url, headers=None, file_path=None):
    """Performs an HTTPS request and slightly processes the response.

    If file_path is provided, saves the body to file instead of including it
    in the return value.

    Args:
      url: str Resource for the request line.
      headers: dict Headers to send along with the request.
      file_path: str File to save to (optional).

    Returns:
      dict process response with the following structure {'body':
      'body of response', 'status': 'http status code', 'headers':
      'headers that came back with the response'}
    """
    headers = headers or {}
    # Download report.
    conn = httplib.HTTPSConnection(
        Utils.GetNetLocFromUrl(self._op_config['server']))
    conn.connect()
    conn.putrequest('GET', url)
    for key in headers:
      conn.putheader(key, headers[key])
    conn.endheaders()
    response = conn.getresponse()
    response_headers = {}
    for key, value in response.getheaders():
      response_headers[key] = value
    body = None
    if file_path:
      self.__DumpToFile(response, file_path)
    else:
      body = response.read()
    return {
        'body': body,
        'status': response.status,
        'headers': response_headers,
        'reason': response.reason
    }

  def __ReloadAuthToken(self):
    """Ensures we have a valid auth_token in our headers."""
    # Load/set authentication token. If authentication token has expired,
    # regenerate it.
    now = time.time()
    if (('authToken' not in self.__service._headers and
         'auth_token_epoch' not in self._config) or
        int(now - self._config['auth_token_epoch']) >= AUTH_TOKEN_EXPIRE):
      if ('email' not in self.__service._headers or
          not self._headers['email'] or
          'password' not in self.__service._headers or
          not self.__service._headers['password']):
        msg = ('Required authentication headers, \'email\' and \'password\', '
               'are missing. Unable to regenerate authentication token.')
        raise ValidationError(msg)
      self._headers['authToken'] = Utils.GetAuthToken(
          self.__service._headers['email'], self.__service._headers['password'],
          AUTH_TOKEN_SERVICE, LIB_SIG, self._config['proxy'])
      self._config['auth_token_epoch'] = time.time()

  def DownloadMCCReport(self, report_definition_id, file_path=None,
                        return_micros=False, tries=50, sleep=30):
    """Blocking call to download a MCC report.

    This method will try to successfully download the report to the specified
    file_path, throwing an AdWordsApiError.  If file_path is None or not
    provided, will return as a string the downloaded report.

    Args:
      report_definition_id: str Id of the report definition to download.
      file_path: str File path to download to. Optional, returns string if None.
      return_micros: bool Whether to return currency in micros.
      tries: int Optional number of times to retry.
      sleep: int Optional number of seconds to sleep between retries.

    Returns:
      str Report data or a tuple of filename and bytes written if file_path is
      not None.

    Raises:
      AdWordsApiError: When we encounter a server error
    """
    response = self.GetMCCReportStatus(report_definition_id, return_micros,
                                       'new')
    while response['httpStatus'] != 301 and tries > 0:
      if response['httpStatus'] != 200:
        msg = []
        if 'state' in response: msg.append(response['state'])
        if 'failureReason' in response: msg.append(response['failureReason'])
        raise AdWordsApiError({
            'faultcode': '500',
            'faultstring': ' '.join(msg)})
      # Otherwise, it should be status == 200 which means try again later.
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Sleeping with %i tries left' % tries
      tries -= 1
      time.sleep(sleep)
      response = self.GetMCCReportStatus(report_definition_id, return_micros,
                                         response['queryToken'])
    if tries <= 0:
      raise AdWordsApiError({'faultstring': 'No more retries left.'})
    # On success, get the download URL from the Location header
    url = None
    if 'Location' in response['headers']:
      url = response['headers']['Location']
    else:
      url = response['headers']['location']
    headers = self.__GenerateHeaders(return_micros)
    return self.__DownloadFile(url, headers, file_path)

  def GetMCCReportStatus(self, report_definition_id, return_micros=False,
                         query_token='new'):
    """Tries to download report and return raw data. Does not poll.

    Args:
      report_definition_id: str Id of the report definition to download.
      return_micros: bool Whether to return currency in micros.
      query_token: str Query token to use, defaults to 'new'.

    Returns:
      str Report data.
    """
    self.__ReloadAuthToken()
    selector = self.__GenerateUrl(report_definition_id, query_token)
    headers = self.__GenerateHeaders(return_micros)
    parsed_response = self.__ParseMCCResponse(self.__MakeRequest(
        selector, headers))
    return parsed_response

  def __ParseMCCResponse(self, http_response):
    """Parses the raw MCC response xml into a dict.

    Args:
      http_response: dict The slightly processed response from the server.

    Returns:
      dict Dictionary interpretation of the response.  Format is ret[tagName] =
      'value' for all tags in the xml response, except for the failed account
      ids which reside in 'failedIds'.  We also store httpStatus, headers (as
      a dict), and the raw xml itself in the tags 'httpStatus', 'headers' and
      'raw'
    """
    self.__CheckOldError(http_response['body'])
    doc = minidom.parseString(http_response['body'])
    ret = {}
    for tag in ['queryToken', 'state', 'total', 'success', 'fail',
                'failureReason']:
      ret[tag] = self.__GetText(doc, tag)
    ret['failedIds'] = self.__GetText(doc, 'id')
    ret['httpStatus'] = http_response['status']
    ret['headers'] = http_response['headers']
    ret['raw'] = http_response['body']
    return ret

  def __GetText(self, doc, tag):
    """Extracts text from elements matching tag name.

    Args:
      doc: DOM DOM model of the xml.
      tag: str Name of the tag to get text for.
    Returns:
      str String value of a single result node.
      list List of string nodes if more than one tag matches.
    """
    nodelist = doc.getElementsByTagName(tag)
    ret = []
    for node in nodelist:
      text_nodes = []
      for text_node in node.childNodes:
        if text_node.nodeType == text_node.TEXT_NODE:
          text_nodes.append(text_node.data)
      if text_nodes:
        ret.append(''.join(text_nodes))
    # return empty string if we have no text
    if not ret:
      return ''
    # if only one, return just the single element
    if len(ret) == 1:
      return ret[0]
    return ret

  def __CheckOldError(self, response_text):
    """Checks for the old-style error messages.

    Args:
      response_text: str Raw text the server returns.

    Raises:
      AdWordsApiError: When we see an old-style error.
    """
    error_message_regex = OLD_ERROR_REGEX
    matches = re.search(error_message_regex, response_text)
    if matches:
      message = response_text
      if matches.group(3):
        message = matches.group(3)
      raise AdWordsApiError({'faultstring': message})

  def __DownloadFile(self, url, headers, file_path=None):
    """Downloads the specified url.

    Args:
      url: str Full URL to download.
      headers: dict Headers to use with the request.
      file_path: str Optional path to download to.  If None, text is returned.

    Returns:
      str File contents if file_path is None or else a tuple with filename and
      bytes written.
    """
    req = urllib2.Request(url, None, headers)
    r = urllib2.urlopen(req)
    # if we have a file, write to it, otherwise return the text
    if file_path:
      return self.__DumpToFile(r, file_path)
    else:
      return r.read()

  def __DumpToFile(self, response, file_path):
    """Reads from response.read() and writes to file_path.

    Args:
      response: file Some object that supports read().
      file_path: str File name to write to.

    Returns:
      tuple Filename and number of bytes written.
    """
    byteswritten = 0
    f = open(file_path, 'w+')
    while True:
      buf = response.read(BUF_SIZE)
      if buf:
        f.write(buf)
        byteswritten += len(buf)
      else: break
    return (file_path, byteswritten)
