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

"""Unit tests to cover AdWordsWebService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import thread
import threading
import unittest

from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.adwords.AdWordsErrors import AdWordsApiError
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import Utils
from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V13
from tests.adspygoogle.adwords import SERVER_V200909
from tests.adspygoogle.adwords import SERVER_V201003
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import VERSION_V13
from tests.adspygoogle.adwords import VERSION_V200909
from tests.adspygoogle.adwords import VERSION_V201003
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import client


class AdWordsWebServiceTestV13(unittest.TestCase):

  """Unittest suite for AdWordsWebService using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallMethod(self):
    """Test whether we can call an API method indirectly."""
    self.assert_(isinstance(client.GetAccountService(
        self.__class__.SERVER, self.__class__.VERSION,
        HTTP_PROXY).GetAccountInfo(), tuple))

  def testCallMethodDirect(self):
    """Test whether we can call an API method directly."""
    headers = client.GetAuthCredentials()
    config = client.GetConfigValues()
    url = '/'.join([AdWordsWebServiceTestV13.SERVER,
                    'api/adwords/v13', 'AccountService'])
    op_config = {
        'server': self.__class__.SERVER,
        'version': self.__class__.VERSION,
        'http_proxy': HTTP_PROXY
    }

    lock = thread.allocate_lock()
    service = AdWordsWebService(headers, config, op_config, url, lock)
    method_name = 'getAccountInfo'
    if config['soap_lib'] == SOAPPY:
      self.assert_(isinstance(service.CallMethod(method_name, (),
                                                 'AccountService'), tuple))
    elif config['soap_lib'] == ZSI:
      web_services = __import__(
          'adspygoogle.adwords.zsi.v13.AccountService_services',
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
    http_proxy = HTTP_PROXY

    self.failUnlessRaises(AdWordsApiError, client.CallRawMethod, soap_message,
                          url, self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV13()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV13(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v13.
  """

  def run(self):
    """Represent thread's activity."""
    AdWordsWebServiceTestV13.responses.append(
        client.GetAccountService(AdWordsWebServiceTestV13.SERVER,
            AdWordsWebServiceTestV13.VERSION, HTTP_PROXY).GetAccountInfo())


class AdWordsWebServiceTestV200909(unittest.TestCase):

  """Unittest suite for AdWordsWebService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  responses = []
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

    self.failUnlessRaises(AdWordsApiError, client.CallRawMethod, soap_message,
                          url, self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV200909()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV200909(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v200909.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {'ids': []}
    AdWordsWebServiceTestV200909.responses.append(
        client.GetCampaignService(AdWordsWebServiceTestV200909.SERVER,
            AdWordsWebServiceTestV200909.VERSION, HTTP_PROXY).Get(selector))


class AdWordsWebServiceTestV201003(unittest.TestCase):

  """Unittest suite for AdWordsWebService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v201003/CampaignService'
    http_proxy = HTTP_PROXY

    self.failUnlessRaises(AdWordsApiError, client.CallRawMethod, soap_message,
                          url, self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201003()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV201003(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v201003.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {'ids': []}
    AdWordsWebServiceTestV201003.responses.append(
        client.GetCampaignService(AdWordsWebServiceTestV201003.SERVER,
            AdWordsWebServiceTestV201003.VERSION, HTTP_PROXY).Get(selector))


class AdWordsWebServiceTestV201008(unittest.TestCase):

  """Unittest suite for AdWordsWebService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  responses = []
  MAX_THREADS = 3

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCallRawMethod(self):
    """Test whether we can call an API method by posting SOAP XML message."""
    soap_message = Utils.ReadFile(os.path.join('data',
                                               'request_getallcampaigns.xml'))
    url = '/api/adwords/cm/v201008/CampaignService'
    http_proxy = None

    self.failUnlessRaises(AdWordsApiError, client.CallRawMethod, soap_message,
                          url, self.__class__.SERVER, http_proxy)

  def testMultiThreads(self):
    """Test whether we can safely execute multiple threads."""
    all_threads = []
    for index in xrange(self.__class__.MAX_THREADS):
      t = TestThreadV201008()
      all_threads.append(t)
      t.start()

    for t in all_threads:
      t.join()

    self.assertEqual(len(self.responses), self.__class__.MAX_THREADS)


class TestThreadV201008(threading.Thread):

  """Creates TestThread.

  Responsible for defining an action for a single thread using v201008.
  """

  def run(self):
    """Represent thread's activity."""
    selector = {'ids': []}
    AdWordsWebServiceTestV201008.responses.append(
        client.GetCampaignService(AdWordsWebServiceTestV201008.SERVER,
            AdWordsWebServiceTestV201008.VERSION, HTTP_PROXY).Get(selector))


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsWebServiceTestV13))
  return suite


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsWebServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsWebServiceTestV201003))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsWebServiceTestV201008))
  return suite


if __name__ == '__main__':
  suite_v13 = makeTestSuiteV13()
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  suite_v201008 = makeTestSuiteV201008()
  alltests = unittest.TestSuite([suite_v13, suite_v200909, suite_v201003,
                                 suite_v201008])
  unittest.main(defaultTest='alltests')
