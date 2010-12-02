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

"""Unit tests to cover AccountService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V13
from tests import VERSION_V13
from tests import client


class AccountServiceTestV13(unittest.TestCase):

  """Unittest suite for AccountService using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      client.use_mcc = True
      self.__class__.service = client.GetAccountService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      # Make sure that Sandbox accounts exist.
      self.__class__.service.GetAccountInfo()
      client.use_mcc = False

  def testGetAccountInfo(self):
    """Test whether we can fetch information for account."""
    self.assert_(isinstance(self.__class__.service.GetAccountInfo(), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getAccountInfo',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetClientAccountInfos(self):
    """Test whether we can fetch all client account information."""
    self.assert_(isinstance(self.__class__.service.GetClientAccountInfos(),
                            tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getClientAccountInfos',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetClientAccounts(self):
    """Test whether we can fetch all client accounts."""
    self.assert_(isinstance(self.__class__.service.GetClientAccounts(), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getClientAccounts',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetMccAlerts(self):
    """Test whether we can retrieve MCC alerts."""
    self.assert_(isinstance(self.__class__.service.GetMccAlerts(), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getMccAlerts',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUpdateAccountInfo(self):
    """Test whether we can update email promotions preferences in account."""
    acct_info = {
        'emailPromotionsPreferences': {
            'accountPerformanceEnabled': 'True',
            'disapprovedAdsEnabled': 'True',
            'marketResearchEnabled': 'False',
            'newsletterEnabled': 'False',
            'promotionsEnabled': 'False'
        }
    }
    self.assertEqual(self.__class__.service.UpdateAccountInfo(acct_info), None)
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'updateAccountInfo',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AccountServiceTestV13))
  return suite


if __name__ == '__main__':
  suite_v13 = makeTestSuiteV13()
  alltests = unittest.TestSuite([suite_v13])
  unittest.main(defaultTest='alltests')
