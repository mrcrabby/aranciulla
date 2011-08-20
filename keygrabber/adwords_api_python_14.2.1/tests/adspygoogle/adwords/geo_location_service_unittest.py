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

"""Unit tests to cover GeoLocationService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V200909
from tests.adspygoogle.adwords import SERVER_V201003
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import VERSION_V200909
from tests.adspygoogle.adwords import VERSION_V201003
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import client


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


class GeoLocationServiceTestV201008(unittest.TestCase):

  """Unittest suite for GeoLocationService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetGeoLocationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetGeoLocationInfo(self):
    """Test whether we can fetch geo location information for the address."""
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


class GeoLocationServiceTestV201101(unittest.TestCase):

  """Unittest suite for GeoLocationService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetGeoLocationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetGeoLocationInfo(self):
    """Test whether we can fetch geo location information for the address."""
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


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GeoLocationServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(GeoLocationServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  suite_v201008 = makeTestSuiteV201008()
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003, suite_v201008,
                                 suite_v201101])
  unittest.main(defaultTest='alltests')
