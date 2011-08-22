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

"""Unit tests to cover AdWordsErrors."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.adwords.AdWordsSoapBuffer import AdWordsSoapBuffer
from adspygoogle.adwords.AdWordsErrors import AdWordsApiError
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.AdWordsErrors import AdWordsRequestError
from adspygoogle.common import Utils
from adspygoogle.common.Errors import ApiAsStrError
from adspygoogle.common.Errors import MalformedBufferError
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


class AdWordsErrorsTest(unittest.TestCase):

  """Unittest suite for AdWordsErrors."""

  TRIGGER_MSG1 = 'The developer token is invalid.'
  TRIGGER_CODE1 = 42
  TRIGGER_STR = """faultcode: soapenv:Server.userException
faultstring: The developer token is invalid.

trigger: xxxxxx++USD
message: The developer token is invalid.
code: 42"""
  TRIGGER_MSG2 = 'An internal error has occurred.  Please retry your request.'
  TRIGGER_CODE2 = 0
  TRIGGER_MSG3 = 'Fault occurred while processing.'
  TRIGGER_MSG4 = 'One or more input elements failed validation.'
  TRIGGER_CODE4 = 122
  XML_RESPONSE_FAULT1 = Utils.ReadFile(
      os.path.join('data', 'response_fault_stacktrace.xml'))
  XML_RESPONSE_FAULT2 = Utils.ReadFile(
      os.path.join('data', 'response_fault.xml'))
  XML_RESPONSE_FAULT3 = Utils.ReadFile(
      os.path.join('data', 'response_fault_errors.xml'))

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testApiAsStrError(self):
    """Tests whether we can catch an Errors.ApiAsStrError exception."""
    try:
      raise ApiAsStrError(self.__class__.TRIGGER_STR)
    except ApiAsStrError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG1)
      self.assertEqual(int(e.code), self.__class__.TRIGGER_CODE1)

  def testStacktraceElement(self):
    """Tests whether we can handle a fault's stacktrace element."""
    try:
      buf = AdWordsSoapBuffer()
      buf.InjectXml(self.__class__.XML_RESPONSE_FAULT1)
      raise AdWordsApiError(buf.GetFaultAsDict())
    except AdWordsApiError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG2)
      self.assertEqual(int(e.code), self.__class__.TRIGGER_CODE2)

  def testProcessingFault(self):
    """Tests whether we can handle a processing fault."""
    try:
      buf = AdWordsSoapBuffer()
      buf.InjectXml(self.__class__.XML_RESPONSE_FAULT2)
      raise AdWordsApiError(buf.GetFaultAsDict())
    except AdWordsApiError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG3)

  def testErrorsFault(self):
    """Tests whether we can handle a fault with errors elements."""
    try:
      buf = AdWordsSoapBuffer()
      buf.InjectXml(self.__class__.XML_RESPONSE_FAULT3)
      raise AdWordsApiError(buf.GetFaultAsDict())
    except AdWordsApiError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG4)
      self.assertEqual(int(e.code), self.__class__.TRIGGER_CODE4)

  def testMalformedBuffer(self):
    """Tests whether we can handle a malformed SOAP buffer."""
    buf = AdWordsSoapBuffer()
    buf.write('JUNK')
    self.assertRaises(MalformedBufferError, buf.GetCallResponseTime)


class AdWordsErrorsTestV13(unittest.TestCase):

  """Unittest suite for AdWordsErrors using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  TRIGGER_MSG1 = 'The developer token is invalid.'
  TRIGGER_CODE1 = 42
  TRIGGER_MSG2 = 'Login with this username/password failed.'
  TRIGGER_CODE2 = 9
  dummy_client = AdWordsClient(path=os.path.join('..', '..', '..'),
                               headers={'email': 'xxxxxx',
                                        'password': 'none',
                                        'useragent': 'ErrorsTest',
                                        'developerToken': 'xxxxxx++USD'})
  dummy_client.debug = False
  dummy_client.soap_lib = client.soap_lib

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    self.__class__.dummy_client.use_mcc = True

  def tearDown(self):
    """Finalize unittest."""
    self.__class__.dummy_client.use_mcc = False

  def testApiError(self):
    """Tests whether we can catch an AdWordsErrors.AdWordsApiError exception."""
    try:
      self.__class__.dummy_client.GetAccountService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetAccountInfo()
    except AdWordsApiError, e:
      try:
        self.assertEqual(e.message, self.__class__.TRIGGER_MSG1)
        self.assertEqual(e.code, self.__class__.TRIGGER_CODE1)
      except:
        self.assertEqual(e.message, self.__class__.TRIGGER_MSG2)
        self.assertEqual(e.code, self.__class__.TRIGGER_CODE2)

  def testError(self):
    """Tests whether we can catch an AdWordsErrors.AdWordsError exception."""
    try:
      try:
        self.__class__.dummy_client.GetAccountService(
            self.__class__.SERVER, self.__class__.VERSION,
            HTTP_PROXY).GetAccountInfo()
      except AdWordsError, e:
        raise AdWordsError(e.message)
    except AdWordsError, e:
      try:
        self.assertEqual(str(e), self.__class__.TRIGGER_MSG1)
      except:
        self.assertEqual(str(e), self.__class__.TRIGGER_MSG2)

  def testRequestError(self):
    """Tests whether we can catch an AdWordsErrors.AdWordsRequestError
    exception."""
    try:
      self.__class__.dummy_client.GetAccountService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetAccountInfo()
    except AdWordsRequestError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG2)


class AdWordsErrorsTestV200909(unittest.TestCase):

  """Unittest suite for AdWordsErrors using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  TRIGGER_TYPE1 = 'RequiredError'
  TRIGGER_MSG1 = 'operations[0].operand.biddingStrategy'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    client.use_mcc = True

  def tearDown(self):
    """Finalize unittest."""
    client.use_mcc = False

  def testMissingBiddingStrategy(self):
    """Tests whether we can catch missing bidding strategy exception."""
    try:
      operations = [
          {
              'operator': 'ADD',
              'operand': {
                  'status': 'PAUSED',
                  'budget': {
                      'period': 'DAILY',
                      'amount': {
                          'microAmount': '1000000'
                      },
                      'deliveryMethod': 'STANDARD'
                  }
              }
          }
      ]
      client.GetCampaignService(self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).Mutate(operations)
    except AdWordsRequestError, e:
      self.assertEqual(e.errors[0].type, self.__class__.TRIGGER_TYPE1)
      self.assertEqual(e.errors[0].fieldPath, self.__class__.TRIGGER_MSG1)


class AdWordsErrorsTestV201003(unittest.TestCase):

  """Unittest suite for AdWordsErrors using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  TRIGGER_TYPE1 = 'RequiredError'
  TRIGGER_MSG1 = 'operations[0].operand.biddingStrategy'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    client.use_mcc = True

  def tearDown(self):
    """Finalize unittest."""
    client.use_mcc = False

  def testMissingBiddingStrategy(self):
    """Tests whether we can catch missing bidding strategy exception."""
    try:
      operations = [
          {
              'operator': 'ADD',
              'operand': {
                  'status': 'PAUSED',
                  'budget': {
                      'period': 'DAILY',
                      'amount': {
                          'microAmount': '1000000'
                      },
                      'deliveryMethod': 'STANDARD'
                  }
              }
          }
      ]
      client.GetCampaignService(self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).Mutate(operations)
    except AdWordsRequestError, e:
      self.assertEqual(e.errors[0].type, self.__class__.TRIGGER_TYPE1)
      self.assertEqual(e.errors[0].fieldPath, self.__class__.TRIGGER_MSG1)


class AdWordsErrorsTestV201008(unittest.TestCase):

  """Unittest suite for AdWordsErrors using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  TRIGGER_TYPE1 = 'RequiredError'
  TRIGGER_MSG1 = 'operations[0].operand.biddingStrategy'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    client.use_mcc = True

  def tearDown(self):
    """Finalize unittest."""
    client.use_mcc = False

  def testMissingBiddingStrategy(self):
    """Tests whether we can catch missing bidding strategy exception."""
    try:
      operations = [
          {
              'operator': 'ADD',
              'operand': {
                  'status': 'PAUSED',
                  'budget': {
                      'period': 'DAILY',
                      'amount': {
                          'microAmount': '1000000'
                      },
                      'deliveryMethod': 'STANDARD'
                  }
              }
          }
      ]
      client.GetCampaignService(self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).Mutate(operations)
    except AdWordsRequestError, e:
      self.assertEqual(e.errors[0].type, self.__class__.TRIGGER_TYPE1)
      self.assertEqual(e.errors[0].fieldPath, self.__class__.TRIGGER_MSG1)


def makeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsErrorsTest))
  return suite


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsErrorsTestV13))
  return suite


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsErrorsTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsErrorsTestV201003))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdWordsErrorsTestV201008))
  return suite


if __name__ == '__main__':
  suite = makeTestSuite()
  suite_v13 = makeTestSuiteV13()
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  suite_v201008 = makeTestSuiteV201008()
  alltests = unittest.TestSuite([suite, suite_v13, suite_v200909,
                                 suite_v201003, suite_v201008])
  unittest.main(defaultTest='alltests')
