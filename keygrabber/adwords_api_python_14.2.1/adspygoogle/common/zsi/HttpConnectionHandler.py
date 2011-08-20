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

"""Creates custom handler for httplib.HTTPConnection."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import StringIO
import gzip
import httplib

from adspygoogle.common import Utils


class HttpConnectionHandler(httplib.HTTPConnection):

  """Implements HttpConnectionHandler.

  Responsible for creating custom HTTP connection object to intercept ZSI's
  implementation. Provides support for HTTP proxy connection. Provides support
  for sending and recieving compressed data.

  Overwrites httplib's putrequest().
  """

  # Connection states from httplib.py.
  _CS_IDLE = 'Idle'
  _CS_REQ_STARTED = 'Request-started'
  _CS_REQ_SENT = 'Request-sent'

  _UNKNOWN = 'UNKNOWN'

  http_proxy = ''
  debug =  False
  compress = False

  def __init__(self, host, port=None, strict=None):
    """Inits HttpConnectionHandler with host and port.

    Args:
      host: str Proxy's HTTP host or combined form of host:port.
      [optional]
      port: int Proxy's HTTP port number.
      strict: bool if True, causes BadStatusLine to be raised if the status
              line can't be parsed as a valid HTTP/1.0 or 1.1 status line.
    """
    self.__host = host
    self.__port = port
    self.__http_proxy = HttpConnectionHandler.http_proxy or host
    httplib.HTTPConnection.__init__(self, host=self.__http_proxy,
                                    port=self.__port, strict=strict)
    if HttpConnectionHandler.debug: self.set_debuglevel(1)

  def send(self, data):
    """Send data to the server.

    Args:
      data: str Data to send to the server.
    """
    # If compression is enabled, compress request prior to sending it, unless
    # data is a header string.
    if (not HttpConnectionHandler.compress or
        (data.find('Host:') > -1 and data.find('Accept-Encoding:') > -1 and
         data.find('Content-Type:') > -1 and data.find('SOAPAction:') > -1 and
         data.find('User-Agent:') > -1)):
      httplib.HTTPConnection.send(self, data)
    else:
      if self.sock is None:
        if self.auto_open:
          self.connect()
        else:
          raise self.NotConnected()


      stream = StringIO.StringIO()
      zdata = gzip.GzipFile(mode='wb', fileobj=stream, compresslevel=1)
      zdata.write(data)
      zdata.close()
      data = stream.getvalue()

      # Set re calculated content's length and encoding type.
      self.putheader('Content-length', len(data))
      self.putheader('Content-encoding', 'gzip')

      httplib.HTTPConnection.endheaders(self)
      httplib.HTTPConnection.send(self, data)

  def putrequest(self, method, url, skip_host=False,
                 skip_accept_encoding=False):
    """Send a request to the server.

    Args:
      method: str Specifies an HTTP request method.
      url: str Specifies the object being requested.
      [optional]
      skip_host: bool If True does not add automatically a 'Host:' header.
      skip_accept_encoding: bool If True does not add automatically an
                            'Accept-Encoding:' header.
    """
    if HttpConnectionHandler.compress: skip_accept_encoding = True
    if self.__http_proxy != self.__host:
      scheme = Utils.GetSchemeFromUrl(url) or 'http'
      netloc = Utils.GetNetLocFromUrl(url) or self.__host
      path = Utils.GetPathFromUrl(url)
      uri = '%s://%s%s' % (scheme, netloc, path)
    else:
      uri = url
    httplib.HTTPConnection.putrequest(self, method=method, url=uri,
                                      skip_host=skip_host,
                                      skip_accept_encoding=skip_accept_encoding)

  def putheader(self, header, value):
    """Send a request header line to the server.

    For example: h.putheader('Accept', 'text/html')

    Args:
      header: str Header to send.
      value: str Value for a given header to send.
    """
    # Compressed content is of a different length than original content, thus
    # don't set the content's length here.
    if HttpConnectionHandler.compress and header == 'Content-Length': return
    str_in = '%s: %s' % (header, value)
    self._output(str_in)

  def endheaders(self):
    """Indicate that the last header line has been sent to the server."""
    if HttpConnectionHandler.compress:
      self.putheader('Accept-Encoding', 'gzip, deflate')
    else:
      self._send_output()

  def getresponse(self):
    """Get the response from the server."

    Returns:
      instance Response from the server.
    """
    if self.debuglevel > 0:
      response = self.response_class(self.sock, self.debuglevel,
                                     strict=self.strict,
                                     method=self._method)
    else:
      response = self.response_class(self.sock, strict=self.strict,
                                     method=self._method)

    response.begin()
    assert response.will_close != HttpConnectionHandler._UNKNOWN
    self.__state = HttpConnectionHandler._CS_IDLE

    if response.will_close:
      # This effectively passes the connection to the response.
      self.close()

    # If response was compressed, uncompress it prior to returning.
    if response.getheader('content-encoding') == 'gzip':
      stream = StringIO.StringIO(response.read())
      data = gzip.GzipFile(fileobj=stream).read()
      response.read = lambda: data
    return response
