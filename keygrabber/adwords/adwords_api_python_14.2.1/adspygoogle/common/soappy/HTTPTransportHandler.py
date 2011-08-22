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

"""Creates custom handler for SOAPpy.Client.HTTPTransport."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from SOAPpy import Client
from SOAPpy import SOAPAddress
from SOAPpy import Utilities
from SOAPpy.Config import Config
from SOAPpy.Errors import HTTPError
import base64
import httplib


class HTTPTransportHandler(Client.HTTPTransport):

  """Implements HTTPTransportHandler."""

  def __init__(self):
    # Defaults for OAuth.
    self.oauth_enabled = False
    self.oauth_handler = None
    self.oauth_credentials = None

  def call(self, addr, data, namespace, soapaction=None, encoding=None,
           http_proxy=None, config=Config):
    """Inits HttpConnectionHandler."""
    if not isinstance(addr, SOAPAddress):
      addr = SOAPAddress(addr, config)

    # Build a request.
    if http_proxy:
      real_addr = http_proxy
      real_path = addr.proto + "://" + addr.host + addr.path
    else:
      real_addr = addr.host
      real_path = addr.path

    if addr.proto == 'httpg':
      from pyGlobus.io import GSIHTTP
      r = GSIHTTP(real_addr, tcpAttr = config.tcpAttr)
    elif addr.proto == 'https':
      r = httplib.HTTPS(real_addr)
    else:
      r = httplib.HTTP(real_addr)

    # Intercept outgoing XML message and inject data.
    if self.data_injects:
      for old, new in self.data_injects:
        data = data.replace(old, new)

    r.putrequest('POST', real_path)

    headers = []

    headers.append(('Host', addr.host))
    headers.append(('User-agent', Client.SOAPUserAgent()))
    t = 'text/xml';
    if encoding != None:
      t += '; charset="%s"' % encoding
    headers.append(('Content-type', t))
    headers.append(('Content-length', str(len(data))))

    # If user is not a user:passwd format we'll receive a failure from the
    # server. . .I guess (??)
    if addr.user != None:
      val = base64.encodestring(addr.user)
      headers.append(('Authorization', 'Basic ' + val.replace('\012','')))

    # Handle OAuth (if enabled)
    if self.oauth_enabled:
      signedrequestparams = self.oauth_handler.GetSignedRequestParameters(
          self.oauth_credentials, str(addr))
      headers.append(('Authorization',
                     'OAuth ' + self.oauth_handler.FormatParametersForHeader(
                         signedrequestparams)))

    # This fixes sending either "" or "None".
    if soapaction is None or len(soapaction) == 0:
      headers.append(('SOAPAction', ''))
    else:
      headers.append(('SOAPAction', '"%s"' % soapaction))

    if config.dumpHeadersOut:
      s = 'Outgoing HTTP headers'
      Utilities.debugHeader(s)
      print 'POST %s %s' % (real_path, r._http_vsn_str)
      for header in headers:
        print '%s:%s' % header
      Utilities.debugFooter(s)

    for header in headers:
      r.putheader(header[0], header[1])
    r.endheaders()

    if config.dumpSOAPOut:
      s = 'Outgoing SOAP'
      Utilities.debugHeader(s)
      print data,
      if data[-1] != '\n':
        print
      Utilities.debugFooter(s)

    # Send the payload.
    r.send(data)

    # Read response line.
    code, msg, headers = r.getreply()

    if headers:
      content_type = headers.get('content-type', 'text/xml')
      content_length = headers.get('Content-length')
    else:
      content_type=None
      content_length=None

    # Work around OC4J bug which does '<len>, <len>' for some reaason.
    if content_length:
      comma=content_length.find(',')
      if comma>0:
        content_length = content_length[:comma]

    # attempt to extract integer message size
    try:
      message_len = int(content_length)
    except:
      message_len = -1

    if message_len < 0:
      # Content-Length missing or invalid; just read the whole socket. This
      # won't work with HTTP/1.1 chunked encoding.
      data = r.getfile().read()
      message_len = len(data)
    else:
      data = r.getfile().read(message_len)

    if(config.debug):
      print 'code=', code
      print 'msg=', msg
      print 'headers=', headers
      print 'content-type=', content_type
      print 'data=', data

    if config.dumpHeadersIn:
      s = 'Incoming HTTP headers'
      Utilities.debugHeader(s)
      if headers.headers:
        print 'HTTP/1.? %d %s' % (code, msg)
        print '\n'.join(map (lambda x: x.strip(), headers.headers))
      else:
        print 'HTTP/0.9 %d %s' % (code, msg)
      Utilities.debugFooter(s)

    def startswith(string, val):
      return string[0:len(val)] == val

    if (code == 500 and
        not (startswith(content_type, 'text/xml') and message_len > 0)):
      raise HTTPError(code, msg)

    if config.dumpSOAPIn:
      s = 'Incoming SOAP'
      Utilities.debugHeader(s)
      print data,
      if (len(data)>0) and (data[-1] != '\n'):
          print
      Utilities.debugFooter(s)

    if code not in (200, 500):
      raise HTTPError(code, msg)

    # Get the new namespace.
    if namespace is None:
      new_ns = None
    else:
      new_ns = self.getNS(namespace, data)

    # Return response payload.
    return data, new_ns
