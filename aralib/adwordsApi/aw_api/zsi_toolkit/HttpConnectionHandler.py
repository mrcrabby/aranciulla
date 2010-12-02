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

"""Creates custom HTTPConnection to support HTTP proxy."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import httplib

from aw_api import Utils


class HttpConnectionHandler(httplib.HTTPConnection):

  """Implements HttpConnectionHandler.

  Responsible for creating custom HTTP connection object to support HTTP proxy
  connection. Overwrites HTTPConnection, must putrequest.
  """

  http_proxy = ''

  def __init__(self, host, port=None, strict=None, timeout=None):
    """Inits HttpConnectionHandler with host and port.

    Args:
      host: str proxy's HTTP host or combined form of host:port.
      [optional]
      port: int proxy's HTTP port number.
      strict: bool if True, causes BadStatusLine to be raised if the status
              line can't be parsed as a valid HTTP/1.0 or 1.1 status line. This
              argument is ignored.
      timeout: int blocking operations will timeout after that many seconds.
               This argument is ignored.
    """
    self.__host = host
    self.__port = port
    self.__http_proxy = HttpConnectionHandler.http_proxy or host
    httplib.HTTPConnection.__init__(self, host=self.__http_proxy,
                                    port=self.__port)

  def putrequest(self, method, url, skip_host=False,
                 skip_accept_encoding=False):
    """Send a line to the server consisting of the request string, the selector
    string, and the HTTP version.

    Args:
      method: str HTTP request method.
      url: str selector URL.
      [optional]
      skip_host: bool if True, disable automatic sending of Host header.
      skip_accept_encoding: bool if True, disable automatic sending of
                            Accept-Encoding header.
    """
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
