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

"""Unit tests to cover AdExtensionOverrideService."""

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


class AdExtensionOverrideServiceTestV200909(unittest.TestCase):

  """Unittest suite for AdExtensionOverrideService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  campaign_id = '0'
  ad_id = '0'
  ad_extension_id = '0'
  geo_location = None
  address = {
      'streetAddress': '1600 Amphitheatre Parkway',
      'cityName': 'Mountain View',
      'provinceCode': 'US-CA',
      'provinceName': 'California',
      'postalCode': '94043',
      'countryCode': 'US'
  }

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdExtensionOverrideService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign_id is '0':
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'name': 'Campaign #%s' % Utils.GetUniqueName(),
              'status': 'PAUSED',
              'biddingStrategy': {
                'type': 'ManualCPC'
              },
              'budget': {
                  'period': 'DAILY',
                  'amount': {
                      'microAmount': '1000000'
                  },
                  'deliveryMethod': 'STANDARD'
              }
          }
      }]
      self.__class__.campaign_id = \
          campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': self.__class__.campaign_id,
              'name': 'AdGroup #%s' % Utils.GetUniqueName(),
              'status': 'ENABLED',
              'bids': {
                  'type': 'ManualCPCAdGroupBids',
                  'keywordMaxCpc': {
                      'amount': {
                          'microAmount': '1000000'
                      }
                  }
              }
          }
      }]
      ad_group_id = ad_group_service.Mutate(operations)[0]['value'][0]['id']
      ad_service = client.GetAdGroupAdService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'AdGroupAd',
              'adGroupId': ad_group_id,
              'ad': {
                  'type': 'TextAd',
                  'url': 'http://www.example.com',
                  'displayUrl': 'example.com',
                  'status': 'ENABLED',
                  'description1': 'Visit the Red Planet in style.',
                  'description2': 'Low-gravity fun for everyone!',
                  'headline': 'Luxury Cruise to Mars'

              }
          }
      }]
      self.__class__.ad_id = \
          ad_service.Mutate(operations)[0]['value'][0]['ad']['id']

    if not self.__class__.geo_location:
      geo_location_service = client.GetGeoLocationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      selector = {
        'addresses': [self.__class__.address]
      }
      self.__class__.geo_location = \
          geo_location_service.Get(selector)[0]

    if self.__class__.ad_extension_id is '0':
      campaign_ad_extension_service = client.GetCampaignAdExtensionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'CampaignAdExtension',
              'campaignId': self.__class__.campaign_id,
              'adExtension': {
                  'type': 'LocationExtension',
                  'address': self.__class__.geo_location['address'],
                  'geoPoint': self.__class__.geo_location['geoPoint'],
                  'encodedLocation':
                      self.__class__.geo_location['encodedLocation'],
                  'source': 'ADWORDS_FRONTEND'
              }
          }
      }]
      self.__class__.ad_extension_id = \
          campaign_ad_extension_service.Mutate(
              operations)[0]['value'][0]['adExtension']['id']


  def testGetAdExtenstionOverrides(self):
    """Test whether we can fetch existing ad extension overrides for a given
    campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id],
        'statuses': ['ACTIVE']
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddAdExtentionOverride(self):
    """Test whether we can add ad extension override to a given campaign."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'adId': self.__class__.ad_id,
            'adExtension': {
                'type': 'AdExtension',
                'id': self.__class__.ad_extension_id,
            }
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


class AdExtensionOverrideServiceTestV201003(unittest.TestCase):

  """Unittest suite for AdExtensionOverrideService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  campaign_id = '0'
  ad_id = '0'
  ad_extension_id = '0'
  geo_location = None
  address = {
      'streetAddress': '1600 Amphitheatre Parkway',
      'cityName': 'Mountain View',
      'provinceCode': 'US-CA',
      'provinceName': 'California',
      'postalCode': '94043',
      'countryCode': 'US'
  }

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdExtensionOverrideService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign_id is '0':
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'name': 'Campaign #%s' % Utils.GetUniqueName(),
              'status': 'PAUSED',
              'biddingStrategy': {
                'type': 'ManualCPC'
              },
              'budget': {
                  'period': 'DAILY',
                  'amount': {
                      'microAmount': '1000000'
                  },
                  'deliveryMethod': 'STANDARD'
              }
          }
      }]
      self.__class__.campaign_id = \
          campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': self.__class__.campaign_id,
              'name': 'AdGroup #%s' % Utils.GetUniqueName(),
              'status': 'ENABLED',
              'bids': {
                  'type': 'ManualCPCAdGroupBids',
                  'keywordMaxCpc': {
                      'amount': {
                          'microAmount': '1000000'
                      }
                  }
              }
          }
      }]
      ad_group_id = ad_group_service.Mutate(operations)[0]['value'][0]['id']
      ad_service = client.GetAdGroupAdService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'AdGroupAd',
              'adGroupId': ad_group_id,
              'ad': {
                  'type': 'TextAd',
                  'url': 'http://www.example.com',
                  'displayUrl': 'example.com',
                  'status': 'ENABLED',
                  'description1': 'Visit the Red Planet in style.',
                  'description2': 'Low-gravity fun for everyone!',
                  'headline': 'Luxury Cruise to Mars'

              }
          }
      }]
      self.__class__.ad_id = \
          ad_service.Mutate(operations)[0]['value'][0]['ad']['id']

    if not self.__class__.geo_location:
      geo_location_service = client.GetGeoLocationService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      selector = {
        'addresses': [self.__class__.address]
      }
      self.__class__.geo_location = \
          geo_location_service.Get(selector)[0]

    if self.__class__.ad_extension_id is '0':
      campaign_ad_extension_service = client.GetCampaignAdExtensionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'CampaignAdExtension',
              'campaignId': self.__class__.campaign_id,
              'adExtension': {
                  'type': 'LocationExtension',
                  'address': self.__class__.geo_location['address'],
                  'geoPoint': self.__class__.geo_location['geoPoint'],
                  'encodedLocation':
                      self.__class__.geo_location['encodedLocation'],
                  'source': 'ADWORDS_FRONTEND'
              }
          }
      }]
      self.__class__.ad_extension_id = \
          campaign_ad_extension_service.Mutate(
              operations)[0]['value'][0]['adExtension']['id']


  def testGetAdExtenstionOverrides(self):
    """Test whether we can fetch existing ad extension overrides for a given
    campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id],
        'statuses': ['ACTIVE']
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddAdExtentionOverride(self):
    """Test whether we can add ad extension override to a given campaign."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'adId': self.__class__.ad_id,
            'adExtension': {
                'type': 'AdExtension',
                'id': self.__class__.ad_extension_id,
            }
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdExtensionOverrideServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdExtensionOverrideServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
