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

"""Unit tests to cover AdGroupAdService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import base64
import os
import sys
sys.path.append('..')
import unittest

from aw_api import SOAPPY
from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V200909
from tests import SERVER_V201003
from tests import VERSION_V200909
from tests import VERSION_V201003
from tests import client


class AdGroupAdServiceTestV200909(unittest.TestCase):

  """Unittest suite for AdGroupAdService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  IMAGE_DATA = Utils.ReadFile(os.path.join('data', 'image.jpg'))
  MOBILE_IMAGE_DATA = Utils.ReadFile(os.path.join('data', 'image_192x53.jpg'))
  if client.soap_lib == SOAPPY:
    IMAGE_DATA = base64.encodestring(IMAGE_DATA)
    MOBILE_IMAGE_DATA = base64.encodestring(MOBILE_IMAGE_DATA)
  client.debug = False
  service = None
  campaign_id = '0'
  ad_group_id = '0'
  ad = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdGroupAdService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign_id is '0' or self.__class__.ad_group_id is '0':
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
      self.__class__.ad_group_id = ad_group_service.Mutate(
          operations)[0]['value'][0]['id']

  def testAddTextAd(self):
    """Test whether we can add a text ad."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
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
    ads = self.__class__.service.Mutate(operations)
    self.__class__.ad = ads[0]['value'][0]
    self.assert_(isinstance(ads, tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddTextAdWithExemptionRequests(self):
    """Test whether we can add a text ad with exemption requests."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
            'ad': {
                'type': 'TextAd',
                'url': 'http://www.example.com',
                'displayUrl': 'example.com',
                'status': 'ENABLED',
                'description1': 'Visit the Red Planet in style.',
                'description2': 'Low-gravity fun for everyone!!!',
                'headline': 'Luxury Cruise to Mars'

            }
        },
        'exemptionRequests': [
            {
                'key': {
                    'policyName': 'nonstandard_punctuation',
                    'violatingText': 'everyone!!!'
                }
            },
            {
                'key': {
                    'policyName': 'nonstandard_punctuation',
                    'violatingText': '!!!'
                }
            }
        ]
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddImageAd(self):
    """Test whether we can add an image ad."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
            'ad': {
                'type': 'ImageAd',
                'image': {
                    'dimensions': [{
                        'key': 'FULL',
                        'value': {'width': '300', 'height': '250'}
                    }],
                    'name': 'image.jpg',
                    'data': self.__class__.IMAGE_DATA
                },
                'name': 'Test image',
                'url': 'http://www.example.com',
                'displayUrl': 'www.example.com'
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

  def testAddMobileImageAd(self):
    """Test whether we can add a mobile image ad."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
            'ad': {
                'type': 'MobileImageAd',
                'markupLanguages': ['HTML'],
                'mobileCarriers': ['T-Mobile@US', 'Verizon@US'],
                'image': {
                    'dimensions': [{
                        'key': 'SHRUNKEN',
                        'value': {'width': '192', 'height': '53'}
                    }],
                    'name': 'image_192x53.jpg',
                    'data': self.__class__.MOBILE_IMAGE_DATA
                },
                'url': 'http://www.example.com',
                'displayUrl': 'www.example.com'
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

  def testGetAllAdsFromCampaign(self):
    """Test whether we can fetch all ads from given campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAd(self):
    """Test whether we can fetch an ad."""
    if self.__class__.ad == None:
      self.testAddTextAd()
    selector = {
        'adGroupIds': [self.__class__.ad['adGroupId']],
        'adIds': [self.__class__.ad['ad']['id']]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUpdateAd(self):
    """Test whether we can update an ad."""
    if self.__class__.ad == None:
      self.testAddTextAd()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad['adGroupId'],
            'ad': {
                'id': self.__class__.ad['ad']['id'],
            },
            'status': 'PAUSED'
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.SET',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


class AdGroupAdServiceTestV201003(unittest.TestCase):

  """Unittest suite for AdGroupAdService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  IMAGE_DATA = Utils.ReadFile(os.path.join('data', 'image.jpg'))
  MOBILE_IMAGE_DATA = Utils.ReadFile(os.path.join('data', 'image_192x53.jpg'))
  if client.soap_lib == SOAPPY:
    IMAGE_DATA = base64.encodestring(IMAGE_DATA)
    MOBILE_IMAGE_DATA = base64.encodestring(MOBILE_IMAGE_DATA)
  client.debug = False
  service = None
  campaign_id = '0'
  ad_group_id = '0'
  ad = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdGroupAdService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign_id is '0' or self.__class__.ad_group_id is '0':
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
      self.__class__.ad_group_id = ad_group_service.Mutate(
          operations)[0]['value'][0]['id']

  def testAddTextAd(self):
    """Test whether we can add a text ad."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
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
    ads = self.__class__.service.Mutate(operations)
    self.__class__.ad = ads[0]['value'][0]
    self.assert_(isinstance(ads, tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddTextAdWithExemptionRequests(self):
    """Test whether we can add a text ad with exemption requests."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
            'ad': {
                'type': 'TextAd',
                'url': 'http://www.example.com',
                'displayUrl': 'example.com',
                'status': 'ENABLED',
                'description1': 'Visit the Red Planet in style.',
                'description2': 'Low-gravity fun for everyone!!!',
                'headline': 'Luxury Cruise to Mars'

            }
        },
        'exemptionRequests': [
            {
                'key': {
                    'policyName': 'nonstandard_punctuation',
                    'violatingText': 'everyone!!!'
                }
            },
            {
                'key': {
                    'policyName': 'nonstandard_punctuation',
                    'violatingText': '!!!'
                }
            }
        ]
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddImageAd(self):
    """Test whether we can add an image ad."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
            'ad': {
                'type': 'ImageAd',
                'image': {
                    'dimensions': [{
                        'key': 'FULL',
                        'value': {'width': '300', 'height': '250'}
                    }],
                    'name': 'image.jpg',
                    'data': self.__class__.IMAGE_DATA
                },
                'name': 'Test image',
                'url': 'http://www.example.com',
                'displayUrl': 'www.example.com'
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

  def testAddMobileImageAd(self):
    """Test whether we can add a mobile image ad."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad_group_id,
            'ad': {
                'type': 'MobileImageAd',
                'markupLanguages': ['HTML'],
                'mobileCarriers': ['T-Mobile@US', 'Verizon@US'],
                'image': {
                    'dimensions': [{
                        'key': 'SHRUNKEN',
                        'value': {'width': '192', 'height': '53'}
                    }],
                    'name': 'image_192x53.jpg',
                    'data': self.__class__.MOBILE_IMAGE_DATA
                },
                'url': 'http://www.example.com',
                'displayUrl': 'www.example.com'
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

  def testGetAllAdsFromCampaign(self):
    """Test whether we can fetch all ads from given campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAd(self):
    """Test whether we can fetch an ad."""
    if self.__class__.ad == None:
      self.testAddTextAd()
    selector = {
        'adGroupIds': [self.__class__.ad['adGroupId']],
        'adIds': [self.__class__.ad['ad']['id']]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUpdateAd(self):
    """Test whether we can update an ad."""
    if self.__class__.ad == None:
      self.testAddTextAd()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': self.__class__.ad['adGroupId'],
            'ad': {
                'id': self.__class__.ad['ad']['id'],
            },
            'status': 'PAUSED'
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.SET',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdGroupAdServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdGroupAdServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
