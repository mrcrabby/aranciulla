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

"""Unit tests to cover WebService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append('..')
import thread
import threading
import unittest

from aw_api import SOAPPY
from aw_api import ZSI
from aw_api import Utils
from aw_api.Errors import ApiError
from aw_api.WebService import WebService
from tests import HTTP_PROXY
from tests import SERVER_V13
from tests import SERVER_V200909
from tests import SERVER_V201003
from tests import VERSION_V13
from tests import VERSION_V200909
from tests import VERSION_V201003
from tests import client


class WebServiceTestV13(unittest.TestCase):

  """Unittest suite for WebService using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  client.debug = False
  info_res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    service = client.GetAccountService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    self.assert_(isinstance(service.GetAccountInfo(), tuple))

  def testCallMethodDirect(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = 'https://sandbox.google.com/api/adwords/v13/AccountService'
    op_config = {
        'server': self.__class__.SERVER,
        'version': self.__class__.VERSION,
        'http_proxy': None
    }

    lock = thread.allocate_lock()
    service = WebService(headers, config, op_config, url, lock)
    soap_lib = config['soap_lib']
    method_name = 'getAccountInfo'
    if soap_lib == SOAPPY:
      self.assert_(isinstance(service.CallMethod(method_name, ()), tuple))
    elif soap_lib == ZSI:
      web_services = __import__(
          'aw_api.zsi_toolkit.v13.AccountService_services',
          globals(), locals(), [''])
      loc = web_services.AccountServiceLocator()
      request = eval('web_services.%sRequest()' % method_name)
      self.assert_(isinstance(service.CallMethod(method_name, (), 'Account',
                                                 loc, request), tuple))

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getaccountinfo.xml'))
    url = '/api/adwords/v13/AccountService'
    http_proxy = None

    self.failUnlessRaises(ApiError, client.CallRawMethod,
                          soap_message, url, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for i in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV13()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.info_res), self.__class__.MAX_THREADS)


class TestThreadV13(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v13.
  """

  def run(self):
    """Represent thread's activity."""
    WebServiceTestV13.info_res.append(
        client.GetAccountService(WebServiceTestV13.SERVER,
            WebServiceTestV13.VERSION).GetAccountInfo())


class WebServiceTestV200909(unittest.TestCase):

  """Unittest suite for WebService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  info_res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v200909/CampaignService'
    http_proxy = None

    self.failUnlessRaises(ApiError, client.CallRawMethod, soap_message, url,
                          http_proxy)


class WebServiceTestV201003(unittest.TestCase):

  """Unittest suite for WebService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  info_res = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v201003/CampaignService'
    http_proxy = None

    self.failUnlessRaises(ApiError, client.CallRawMethod, soap_message, url,
                          http_proxy)


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(WebServiceTestV13))
  return suite


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(WebServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(WebServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v13 = makeTestSuiteV13()
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v13, suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
