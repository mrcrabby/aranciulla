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

"""Unit tests to cover Errors."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from aw_api.Client import Client
from aw_api.Errors import ApiError
from aw_api.Errors import ApiAsStrError
from aw_api.Errors import Error
from aw_api.Errors import MalformedBufferError
from aw_api.Errors import RequestError
from aw_api.SoapBuffer import SoapBuffer
from tests import HTTP_PROXY
from tests import SERVER_V13
from tests import SERVER_V200909
from tests import SERVER_V201003
from tests import VERSION_V13
from tests import VERSION_V200909
from tests import VERSION_V201003
from tests import client


class ErrorsTest(unittest.TestCase):

  """Unittest suite for Errors."""

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
      self.assertEqual(e.msg, self.__class__.TRIGGER_MSG1)
      self.assertEqual(int(e.code), self.__class__.TRIGGER_CODE1)

  def testStacktraceElement(self):
    """Tests whether we can handle a fault's stacktrace element."""
    try:
      buf = SoapBuffer()
      buf.InjectXml(self.__class__.XML_RESPONSE_FAULT1)
      raise ApiError(buf.GetFaultAsDict())
    except ApiError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG2)
      self.assertEqual(int(e.code), self.__class__.TRIGGER_CODE2)

  def testProcessingFault(self):
    """Tests whether we can handle a processing fault."""
    try:
      buf = SoapBuffer()
      buf.InjectXml(self.__class__.XML_RESPONSE_FAULT2)
      raise ApiError(buf.GetFaultAsDict())
    except ApiError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG3)

  def testErrorsFault(self):
    """Tests whether we can handle a fault with errors elements."""
    try:
      buf = SoapBuffer()
      buf.InjectXml(self.__class__.XML_RESPONSE_FAULT3)
      raise ApiError(buf.GetFaultAsDict())
    except ApiError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG4)
      self.assertEqual(int(e.code), self.__class__.TRIGGER_CODE4)

  def testMalformedBuffer(self):
    """Tests whether we can handle a malformed SOAP buffer."""
    buf = SoapBuffer()
    buf.write('JUNK')
    self.assertRaises(MalformedBufferError, buf.GetCallResponseTime)


class ErrorsTestV13(unittest.TestCase):

  """Unittest suite for Errors using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  TRIGGER_MSG1 = 'The developer token is invalid.'
  TRIGGER_CODE1 = 42
  TRIGGER_MSG2 = 'Login with this username/password failed.'
  TRIGGER_CODE2 = 9
  dummy_client = Client(path='..',
                        headers={'email': 'xxxxxx',
                                 'password': 'none',
                                 'useragent': 'ErrorsTest',
                                 'developerToken': 'xxxxxx++USD'})
  dummy_client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    self.__class__.dummy_client.use_mcc = True

  def tearDown(self):
    """Finalize unittest."""
    self.__class__.dummy_client.use_mcc = False

  def testApiError(self):
    """Tests whether we can catch an Errors.ApiError exception."""
    try:
      self.__class__.dummy_client.GetAccountService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetAccountInfo()
    except ApiError, e:
      try:
        self.assertEqual(e.message, self.__class__.TRIGGER_MSG1)
        self.assertEqual(e.code, self.__class__.TRIGGER_CODE1)
      except:
        self.assertEqual(e.message, self.__class__.TRIGGER_MSG2)
        self.assertEqual(e.code, self.__class__.TRIGGER_CODE2)

  def testError(self):
    """Tests whether we can catch an Errors.Error exception."""
    try:
      try:
        self.__class__.dummy_client.GetAccountService(
            self.__class__.SERVER, self.__class__.VERSION,
            HTTP_PROXY).GetAccountInfo()
      except ApiError, e:
        raise Error(e.message)
    except Error, e:
      try:
        self.assertEqual(str(e), self.__class__.TRIGGER_MSG1)
      except:
        self.assertEqual(str(e), self.__class__.TRIGGER_MSG2)

  def testRequestError(self):
    """Tests whether we can catch an Errors.RequestError exception."""
    try:
      self.__class__.dummy_client.GetAccountService(
          self.__class__.SERVER, self.__class__.VERSION,
          HTTP_PROXY).GetAccountInfo()
    except RequestError, e:
      self.assertEqual(e.message, self.__class__.TRIGGER_MSG2)


class ErrorsTestV200909(unittest.TestCase):

  """Unittest suite for Errors using v200909."""

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
    except RequestError, e:
      self.assertEqual(e.errors[0].type, self.__class__.TRIGGER_TYPE1)
      self.assertEqual(e.errors[0].field_path, self.__class__.TRIGGER_MSG1)


class ErrorsTestV201003(unittest.TestCase):

  """Unittest suite for Errors using v201003."""

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
    except RequestError, e:
      self.assertEqual(e.errors[0].type, self.__class__.TRIGGER_TYPE1)
      self.assertEqual(e.errors[0].field_path, self.__class__.TRIGGER_MSG1)


def makeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ErrorsTest))
  return suite


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ErrorsTestV13))
  return suite


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ErrorsTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ErrorsTestV201003))
  return suite


if __name__ == '__main__':
  suite = makeTestSuite()
  suite_v13 = makeTestSuiteV13()
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite, suite_v13, suite_v200909,
                                 suite_v201003])
  unittest.main(defaultTest='alltests')
