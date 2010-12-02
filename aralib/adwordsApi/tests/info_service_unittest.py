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

"""Unit tests to cover InfoService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V200909
from tests import SERVER_V201003
from tests import VERSION_V200909
from tests import VERSION_V201003
from tests import client


class InfoServiceTestV200909(unittest.TestCase):

  """Unittest suite for InfoService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    client.use_mcc = True
    if not self.__class__.service:
      self.__class__.service = client.GetInfoService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def tearDown(self):
    """Finalize unittest."""
    client.use_mcc = False

  def testGetFreeUsageUnitsPerMonth(self):
    """Test whether we can get free usage units per month."""
    selector = {
        'apiUsageType': 'FREE_USAGE_API_UNITS_PER_MONTH'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetTotalUsageUnitsPerMonth(self):
    """Test whether we can get total usage units per month."""
    selector = {
        'apiUsageType': 'TOTAL_USAGE_API_UNITS_PER_MONTH'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetOperationCount(self):
    """Test whether we can get operation count."""
    selector = {
        'dateRange': {
            'min': '20090101',
            'max': '20090131'
        },
        'apiUsageType': 'OPERATION_COUNT'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetUnitCount(self):
    """Test whether we can get unit count."""
    selector = {
        'dateRange': {
            'min': '20090901',
            'max': '20090930'
        },
        'apiUsageType': 'UNIT_COUNT'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetUnitCountForMethod(self):
    """Test whether we can get unit count for method."""
    selector = {
        'serviceName': 'AdGroupService',
        'methodName': 'mutate',
        'dateRange': {
            'min': '20090901',
            'max': '20091014'
        },
        'apiUsageType': 'UNIT_COUNT'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetUnitCountForClients(self):
    """Test whether we can get unit count for clients."""
    selector = {
        'dateRange': {
            'min': '20090801',
            'max': '20090831'
        },
        'apiUsageType': 'UNIT_COUNT_FOR_CLIENTS'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetMethodCost(self):
    """Test whether we can get method cost."""
    selector = {
        'serviceName': 'AdGroupService',
        'methodName': 'mutate',
        'operator': 'SET',
        'dateRange': {
            'min': '20090801',
            'max': '20090801'
        },
        'apiUsageType': 'METHOD_COST'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


class InfoServiceTestV201003(unittest.TestCase):

  """Unittest suite for InfoService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    client.use_mcc = True
    if not self.__class__.service:
      self.__class__.service = client.GetInfoService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def tearDown(self):
    """Finalize unittest."""
    client.use_mcc = False

  def testGetFreeUsageUnitsPerMonth(self):
    """Test whether we can get free usage units per month."""
    selector = {
        'apiUsageType': 'FREE_USAGE_API_UNITS_PER_MONTH'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetTotalUsageUnitsPerMonth(self):
    """Test whether we can get total usage units per month."""
    selector = {
        'apiUsageType': 'TOTAL_USAGE_API_UNITS_PER_MONTH'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetOperationCount(self):
    """Test whether we can get operation count."""
    selector = {
        'dateRange': {
            'min': '20090101',
            'max': '20090131'
        },
        'apiUsageType': 'OPERATION_COUNT'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetUnitCount(self):
    """Test whether we can get unit count."""
    selector = {
        'dateRange': {
            'min': '20090901',
            'max': '20090930'
        },
        'apiUsageType': 'UNIT_COUNT'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetUnitCountForMethod(self):
    """Test whether we can get unit count for method."""
    selector = {
        'serviceName': 'AdGroupService',
        'methodName': 'mutate',
        'dateRange': {
            'min': '20090901',
            'max': '20091014'
        },
        'apiUsageType': 'UNIT_COUNT'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetUnitCountForClients(self):
    """Test whether we can get unit count for clients."""
    selector = {
        'dateRange': {
            'min': '20090801',
            'max': '20090831'
        },
        'apiUsageType': 'UNIT_COUNT_FOR_CLIENTS'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetMethodCost(self):
    """Test whether we can get method cost."""
    selector = {
        'serviceName': 'AdGroupService',
        'methodName': 'mutate',
        'operator': 'SET',
        'dateRange': {
            'min': '20090801',
            'max': '20090801'
        },
        'apiUsageType': 'METHOD_COST'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(InfoServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(InfoServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
