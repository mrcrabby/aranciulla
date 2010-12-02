#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Unit tests to cover GeoLocationService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V200909
from tests import VERSION_V200909
from tests import SERVER_V201003
from tests import VERSION_V201003
from tests import client


class GeoLocationServiceTestV200909(unittest.TestCase):

  """Unittest suite for GeoLocationService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetGeoLocationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetGeoLocationInfo(self):
    """Test whether we can fetch geo location information for the given
    address."""
    selector = {
        'addresses': [
            {
                'streetAddress': '1600 Amphitheatre Parkway',
                'cityName': 'Mountain View',
                'provinceCode': 'US-CA',
                'provinceName': 'California',
                'postalCode': '94043',
                'countryCode': 'US'
            },
            {
                'streetAddress': '76 Ninth Avenue',
                'cityName': 'New York',
                'provinceCode': 'US-NY',
                'provinceName': 'New York',
                'postalCode': '10011',
                'countryCode': 'US'
            },
            {
                'streetAddress': '五四大街1号, Beijing东城区',
                'countryCode': 'CN'
            }
        ]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


class GeoLocationServiceTestV201003(unittest.TestCase):

  """Unittest suite for GeoLocationService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetGeoLocationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetGeoLocationInfo(self):
    """Test whether we can fetch geo location information for the given
    address."""
    selector = {
        'addresses': [
            {
                'streetAddress': '1600 Amphitheatre Parkway',
                'cityName': 'Mountain View',
                'provinceCode': 'US-CA',
                'provinceName': 'California',
                'postalCode': '94043',
                'countryCode': 'US'
            },
            {
                'streetAddress': '76 Ninth Avenue',
                'cityName': 'New York',
                'provinceCode': 'US-NY',
                'provinceName': 'New York',
                'postalCode': '10011',
                'countryCode': 'US'
            },
            {
                'streetAddress': '五四大街1号, Beijing东城区',
                'countryCode': 'CN'
            }
        ]
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
  suite.addTests(unittest.makeSuite(GeoLocationServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GeoLocationServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
