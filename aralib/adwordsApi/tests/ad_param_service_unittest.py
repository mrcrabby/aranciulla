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

"""Unit tests to cover AdParamService."""

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


class AdParamServiceTestV200909(unittest.TestCase):

  """Unittest suite for AdParamService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  ad_group_id = '0'
  text_ad_id = '0'
  criterion_id = '0'
  has_param = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdParamService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.ad_group_id is '0' or self.__class__.text_ad_id is '0' or
        self.__class__.criterion_id is '0'):
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
      campaign_id = campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id,
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
      self.__class__.ad_group_id = \
          ad_group_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_ad_service = client.GetAdGroupAdService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
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
                  'description1': 'Good deals, only {param2:} left',
                  'description2': 'Low prices under {param1:}!',
                  'headline': 'MacBook Pro Sale'
              }
          }
      }]
      self.__class__.text_ad_id = \
          ad_group_ad_service.Mutate(operations)[0]['value'][0]['ad']['id']
      ad_group_criterion_service = \
          client.GetAdGroupCriterionService(
              self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'BiddableAdGroupCriterion',
              'adGroupId': self.__class__.ad_group_id,
              'criterion': {
                  'type': 'Keyword',
                  'matchType': 'BROAD',
                  'text': 'macbook pro'
              }
          }
      }]
      self.__class__.criterion_id = ad_group_criterion_service.Mutate(
          operations)[0]['value'][0]['criterion']['id']

  def testGetAllAdParamsForAdGroup(self):
    """Test whether we can fetch all existing ad params in a given ad group."""
    selector = {
        'adGroupIds': [self.__class__.ad_group_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAdParam(self):
    """Test whether we can fetch an existing ad param for a given ad group and
    criterion."""
    if not self.__class__.has_param:
      self.testCreateAdParam()
    selector = {
        'adGroupIds': [self.__class__.ad_group_id],
        'criterionId': self.__class__.criterion_id
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testCreateAdParam(self):
    """Test whether we can create a new ad param."""
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'adGroupId': self.__class__.ad_group_id,
                'criterionId': self.__class__.criterion_id,
                'insertionText': '$1,699',
                'paramIndex': '1'
            }
        },
        {
            'operator': 'SET',
            'operand': {
                'adGroupId': self.__class__.ad_group_id,
                'criterionId': self.__class__.criterion_id,
                'insertionText': '139',
                'paramIndex': '2'
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.SET',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())
    self.__class__.has_param = True

  def testUpdateAdParam(self):
    """Test whether we can update an existing ad param."""
    if not self.__class__.has_param:
      self.testCreateAdParam()
    operations = [{
        'operator': 'SET',
        'operand': {
            'adGroupId': self.__class__.ad_group_id,
            'criterionId': self.__class__.criterion_id,
            'insertionText': '$15',
            'paramIndex': '1'
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

  def testRemoveAdParam(self):
    """Test whether we can remove an existing ad param."""
    if not self.__class__.has_param:
      self.testCreateAdParam()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'adGroupId': self.__class__.ad_group_id,
            'criterionId': self.__class__.criterion_id,
            'paramIndex': '1'
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.REMOVE',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())
    self.__class__.has_param = False


class AdParamServiceTestV201003(unittest.TestCase):

  """Unittest suite for AdParamService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  ad_group_id = '0'
  text_ad_id = '0'
  criterion_id = '0'
  has_param = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdParamService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.ad_group_id is '0' or self.__class__.text_ad_id is '0' or
        self.__class__.criterion_id is '0'):
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
      campaign_id = campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id,
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
      self.__class__.ad_group_id = \
          ad_group_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_ad_service = client.GetAdGroupAdService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
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
                  'description1': 'Good deals, only {param2:} left',
                  'description2': 'Low prices under {param1:}!',
                  'headline': 'MacBook Pro Sale'
              }
          }
      }]
      self.__class__.text_ad_id = \
          ad_group_ad_service.Mutate(operations)[0]['value'][0]['ad']['id']
      ad_group_criterion_service = \
          client.GetAdGroupCriterionService(
              self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'type': 'BiddableAdGroupCriterion',
              'adGroupId': self.__class__.ad_group_id,
              'criterion': {
                  'type': 'Keyword',
                  'matchType': 'BROAD',
                  'text': 'macbook pro'
              }
          }
      }]
      self.__class__.criterion_id = ad_group_criterion_service.Mutate(
          operations)[0]['value'][0]['criterion']['id']

  def testGetAllAdParamsForAdGroup(self):
    """Test whether we can fetch all existing ad params in a given ad group."""
    selector = {
        'adGroupIds': [self.__class__.ad_group_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAdParam(self):
    """Test whether we can fetch an existing ad param for a given ad group and
    criterion."""
    if not self.__class__.has_param:
      self.testCreateAdParam()
    selector = {
        'adGroupIds': [self.__class__.ad_group_id],
        'criterionId': self.__class__.criterion_id
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testCreateAdParam(self):
    """Test whether we can create a new ad param."""
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'adGroupId': self.__class__.ad_group_id,
                'criterionId': self.__class__.criterion_id,
                'insertionText': '$1,699',
                'paramIndex': '1'
            }
        },
        {
            'operator': 'SET',
            'operand': {
                'adGroupId': self.__class__.ad_group_id,
                'criterionId': self.__class__.criterion_id,
                'insertionText': '139',
                'paramIndex': '2'
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.SET',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())
    self.__class__.has_param = True

  def testUpdateAdParam(self):
    """Test whether we can update an existing ad param."""
    if not self.__class__.has_param:
      self.testCreateAdParam()
    operations = [{
        'operator': 'SET',
        'operand': {
            'adGroupId': self.__class__.ad_group_id,
            'criterionId': self.__class__.criterion_id,
            'insertionText': '$15',
            'paramIndex': '1'
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

  def testRemoveAdParam(self):
    """Test whether we can remove an existing ad param."""
    if not self.__class__.has_param:
      self.testCreateAdParam()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'adGroupId': self.__class__.ad_group_id,
            'criterionId': self.__class__.criterion_id,
            'paramIndex': '1'
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.REMOVE',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())
    self.__class__.has_param = False


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdParamServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdParamServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
