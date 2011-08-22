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

"""Unit tests to cover CampaignCriterionService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V200909
from tests.adspygoogle.adwords import SERVER_V201003
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import VERSION_V200909
from tests.adspygoogle.adwords import VERSION_V201003
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import client


class CampaignCriterionServiceTestV200909(unittest.TestCase):

  """Unittest suite for CampaignCriterionService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  campaign_id = '0'
  kw = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignCriterionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.campaign_id == '0'):
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

  def testAddCriterionKeyword(self):
    """Test whether we can add an ad group criterion keyword."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'NegativeCampaignCriterion',
            'campaignId': self.__class__.campaign_id,
            'criterion': {
                'type': 'Keyword',
                'matchType': 'BROAD',
                'text': 'mars cruise'
            }
        }
    }]
    criteria = self.__class__.service.Mutate(operations)
    self.__class__.kw = criteria[0]['value'][0]
    self.assert_(isinstance(criteria, tuple))

  def testGetAllCriteriaCampaignLevel(self):
    """Test whether we can fetch criteria at campaign level."""
    selector = {
        'idFilters': [{
            'campaignId': self.__class__.campaign_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testDeleteCriterion(self):
    """Test whether we can delete criterion at campaign level."""
    if self.__class__.kw is None:
      self.testAddCriterionKeyword()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'type': 'NegativeCampaignCriterion',
            'campaignId': self.__class__.kw['campaignId'],
            'criterion': {
                'id': self.__class__.kw['criterion']['id']
            }
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


class CampaignCriterionServiceTestV201003(unittest.TestCase):

  """Unittest suite for CampaignCriterionService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  campaign_id = '0'
  kw = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignCriterionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.campaign_id == '0'):
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

  def testAddCriterionKeyword(self):
    """Test whether we can add an ad group criterion keyword."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'NegativeCampaignCriterion',
            'campaignId': self.__class__.campaign_id,
            'criterion': {
                'type': 'Keyword',
                'matchType': 'BROAD',
                'text': 'mars cruise'
            }
        }
    }]
    criteria = self.__class__.service.Mutate(operations)
    self.__class__.kw = criteria[0]['value'][0]
    self.assert_(isinstance(criteria, tuple))

  def testGetAllCriteriaCampaignLevel(self):
    """Test whether we can fetch criteria at campaign level."""
    selector = {
        'idFilters': [{
            'campaignId': self.__class__.campaign_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testDeleteCriterion(self):
    """Test whether we can delete criterion at campaign level."""
    if self.__class__.kw is None:
      self.testAddCriterionKeyword()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'type': 'NegativeCampaignCriterion',
            'campaignId': self.__class__.kw['campaignId'],
            'criterion': {
                'id': self.__class__.kw['criterion']['id']
            }
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


class CampaignCriterionServiceTestV201008(unittest.TestCase):

  """Unittest suite for CampaignCriterionService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None
  campaign_id = '0'
  kw = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignCriterionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.campaign_id == '0'):
      campaign_service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'name': 'Campaign #%s' % Utils.GetUniqueName(),
              'status': 'PAUSED',
              'biddingStrategy': {
                  'xsi_type': 'ManualCPC'
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

  def testAddCriterionKeyword(self):
    """Test whether we can add an ad group criterion keyword."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'xsi_type': 'NegativeCampaignCriterion',
            'campaignId': self.__class__.campaign_id,
            'criterion': {
                'xsi_type': 'Keyword',
                'matchType': 'BROAD',
                'text': 'mars cruise'
            }
        }
    }]
    criteria = self.__class__.service.Mutate(operations)
    self.__class__.kw = criteria[0]['value'][0]
    self.assert_(isinstance(criteria, tuple))

  def testGetAllCriteriaCampaignLevel(self):
    """Test whether we can fetch criteria at campaign level."""
    selector = {
        'idFilters': [{
            'campaignId': self.__class__.campaign_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testDeleteCriterion(self):
    """Test whether we can delete criterion at campaign level."""
    if self.__class__.kw is None:
      self.testAddCriterionKeyword()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'xsi_type': 'NegativeCampaignCriterion',
            'campaignId': self.__class__.kw['campaignId'],
            'criterion': {
                'id': self.__class__.kw['criterion']['id']
            }
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignCriterionServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignCriterionServiceTestV201003))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignCriterionServiceTestV201008))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  suite_v201008 = makeTestSuiteV201008()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003, suite_v201008])
  unittest.main(defaultTest='alltests')
