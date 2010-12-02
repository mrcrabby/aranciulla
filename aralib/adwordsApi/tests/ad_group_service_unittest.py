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

"""Unit tests to cover AdGroupService."""

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


class AdGroupServiceTestV200909(unittest.TestCase):

  """Unittest suite for AdGroupService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  cpc_campaign_id = '0'
  ad_group = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.cpc_campaign_id is '0'):
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
              'endDate': '20110101',
              'budget': {
                  'period': 'DAILY',
                  'amount': {
                      'microAmount': '2000000'
                  },
                  'deliveryMethod': 'STANDARD'
              }
          }
      }]
      self.__class__.cpc_campaign_id = \
          campaign_service.Mutate(operations)[0]['value'][0]['id']

  def testAddAdGroupKeyword(self):
    """Test whether we can add an ad group for keywords."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': self.__class__.cpc_campaign_id,
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
    ad_groups = self.__class__.service.Mutate(operations)
    self.__class__.ad_group = ad_groups[0]['value'][0]
    self.assert_(isinstance(ad_groups, tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddAdGroupPlacement(self):
    """Test whether we can add an ad group for placements."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': self.__class__.cpc_campaign_id,
            'name': 'AdGroup #%s' % Utils.GetUniqueName(),
            'status': 'ENABLED',
            'bids': {
                'type': 'ManualCPCAdGroupBids',
                'siteMaxCpc': {
                    'amount': {
                        'microAmount': '1000000'
                    }
                }
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

  def testAddAdGroupKeywordPlacement(self):
    """Test whether we can add an ad group for all criteria types."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': self.__class__.cpc_campaign_id,
            'name': 'AdGroup #%s' % Utils.GetUniqueName(),
            'status': 'ENABLED',
            'bids': {
                'type': 'ManualCPCAdGroupBids',
                'keywordMaxCpc': {
                    'amount': {
                        'microAmount': '1000000'
                    }
                },
                'siteMaxCpc': {
                    'amount': {
                        'microAmount': '1000000'
                    }
                }
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

  def testGetAdGroup(self):
    """Test whether we can fetch an existing ad group."""
    if self.__class__.ad_group == None:
      self.testAddAdGroupKeyword()
    selector = {
        'campaignId': self.__class__.cpc_campaign_id,
        'adGroupIds': [self.__class__.ad_group['id']]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAdGroups(self):
    """Test whether we can fetch all existing ad groups."""
    selector = {
        'campaignId': self.__class__.cpc_campaign_id,
        'adGroupIds': []
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUpdateAdGroup(self):
    """Test whether we can update an existing ad group."""
    if self.__class__.ad_group == None:
      self.testAddAdGroupKeyword()
    ad_group = self.__class__.ad_group
    ad_group['status'] = 'PAUSED'
    ad_group['bids']['keywordMaxCpc']['amount']['microAmount'] = '2000000'
    operations = [{
        'operator': 'SET',
        'operand': ad_group
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.SET',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


class AdGroupServiceTestV201003(unittest.TestCase):

  """Unittest suite for AdGroupService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  cpc_campaign_id = '0'
  ad_group = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.cpc_campaign_id is '0'):
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
              'endDate': '20110101',
              'budget': {
                  'period': 'DAILY',
                  'amount': {
                      'microAmount': '2000000'
                  },
                  'deliveryMethod': 'STANDARD'
              }
          }
      }]
      self.__class__.cpc_campaign_id = \
          campaign_service.Mutate(operations)[0]['value'][0]['id']

  def testAddAdGroupKeyword(self):
    """Test whether we can add an ad group for keywords."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': self.__class__.cpc_campaign_id,
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
    ad_groups = self.__class__.service.Mutate(operations)
    self.__class__.ad_group = ad_groups[0]['value'][0]
    self.assert_(isinstance(ad_groups, tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddAdGroupPlacement(self):
    """Test whether we can add an ad group for placements."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': self.__class__.cpc_campaign_id,
            'name': 'AdGroup #%s' % Utils.GetUniqueName(),
            'status': 'ENABLED',
            'bids': {
                'type': 'ManualCPCAdGroupBids',
                'siteMaxCpc': {
                    'amount': {
                        'microAmount': '1000000'
                    }
                }
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

  def testAddAdGroupKeywordPlacement(self):
    """Test whether we can add an ad group for all criteria types."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignId': self.__class__.cpc_campaign_id,
            'name': 'AdGroup #%s' % Utils.GetUniqueName(),
            'status': 'ENABLED',
            'bids': {
                'type': 'ManualCPCAdGroupBids',
                'keywordMaxCpc': {
                    'amount': {
                        'microAmount': '1000000'
                    }
                },
                'siteMaxCpc': {
                    'amount': {
                        'microAmount': '1000000'
                    }
                }
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

  def testGetAdGroup(self):
    """Test whether we can fetch an existing ad group."""
    if self.__class__.ad_group == None:
      self.testAddAdGroupKeyword()
    selector = {
        'campaignIds': [self.__class__.cpc_campaign_id],
        'adGroupIds': [self.__class__.ad_group['id']]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAdGroups(self):
    """Test whether we can fetch all existing ad groups."""
    selector = {
        'campaignIds': [self.__class__.cpc_campaign_id],
        'adGroupIds': []
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUpdateAdGroup(self):
    """Test whether we can update an existing ad group."""
    if self.__class__.ad_group == None:
      self.testAddAdGroupKeyword()
    ad_group = self.__class__.ad_group
    ad_group['status'] = 'PAUSED'
    ad_group['bids']['keywordMaxCpc']['amount']['microAmount'] = '2000000'
    operations = [{
        'operator': 'SET',
        'operand': ad_group
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
  suite.addTests(unittest.makeSuite(AdGroupServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdGroupServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
