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

"""Interface for fetching authentication token to access Google Account."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import urllib

from aw_api import AUTH_TOKEN_SERVICE
from aw_api import LIB_SHORT_NAME
from aw_api import LIB_VERSION
from aw_api.Errors import AuthTokenError


class AuthToken(object):

  """Fetches authentication token.

  Responsible for fetching authentication token to access Google Account,
  https://www.google.com/accounts/NewAccount. The token is fetched via the
  Account Authentication API, http://code.google.com/apis/accounts/.
  """

  def __init__(self, email, password):
    """Inits AuthToken."""
    self.__email = email
    self.__password = password
    self.__account_type = 'GOOGLE'
    self.__service = AUTH_TOKEN_SERVICE
    self.__source = 'Google-%s-%s' % (LIB_SHORT_NAME, LIB_VERSION)
    self.__sid = ''
    self.__lsid = ''
    self.__auth = ''

    self.__Login()

  def __Login(self):
    """Fetch Auth token and SID, LSID cookies from Google Account auth."""
    url = 'https://www.google.com/accounts/ClientLogin'
    data = [('Email', self.__email),
            ('Passwd', self.__password),
            ('accountType', self.__account_type),
            ('service', self.__service),
            ('source', self.__source)]
    try:
      fh = urllib.urlopen(url, urllib.urlencode(data))
      try:
        tag, msg = fh.readline().split('=')
        if tag in ('SID', 'LSID', 'Auth'):
          self.__sid = msg.strip()
          self.__lsid = fh.readline().split('=')[1].strip()
          self.__auth = fh.readline().split('=')[1].strip()
        elif tag in ('Error',):
          raise AuthTokenError(msg.strip())
        elif tag in ('CaptchaToken',):
          raise AuthTokenError('Captcha token is %s' % msg.strip())
        else:
          raise AuthTokenError(msg.strip())
      finally:
        fh.close()
    except IOError, e:
      raise AuthTokenError(e)

  def GetSidToken(self):
    """Return SID cookie.

    Returns:
      str an SID cookie.
    """
    return self.__sid

  def GetLsidToken(self):
    """Return LSID cookie.

    Returns:
      str an LSDI cookie.
    """
    return self.__lsid

  def GetAuthToken(self):
    """Return Auth authentication token.

    Returns:
      str an Auth authentication token.
    """
    return self.__auth
