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

"""Unit tests to cover AdGroupCriterionService."""

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


class AdGroupCriterionServiceTestV200909(unittest.TestCase):

  """Unittest suite for AdGroupCriterionService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  campaign_id = '0'
  kw_ad_group_id = '0'
  place_ad_group_id = '0'
  kw = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdGroupCriterionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.campaign_id is '0' or
        self.__class__.kw_ad_group_id is '0' or
        self.__class__.place_ad_group_id is '0'):
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
      },
      {
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
      ad_groups = ad_group_service.Mutate(operations)[0]['value']
      self.__class__.kw_ad_group_id = ad_groups[0]['id']
      self.__class__.place_ad_group_id = ad_groups[1]['id']

  def testAddCriterionKeyword(self):
    """Test whether we can add an ad group criterion keyword."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw_ad_group_id,
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
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddCriterionPlacement(self):
    """Test whether we can add an ad group criterion placement."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.place_ad_group_id,
            'criterion': {
                'type': 'Placement',
                'url': 'www.example.com'
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

  def testAddKeywordCrossAdGroup(self):
    """Test whether we can add cross ad group keywords."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw_ad_group_id,
            'criterion': {
                'type': 'Keyword',
                'matchType': 'BROAD',
                'text': 'mars cruise'
            }
        }
    },
    {
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.place_ad_group_id,
            'criterion': {
                'type': 'Placement',
                'url': 'www.example.com'
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

  def testGetAllActivePausedCriteria(self):
    """Test whether we can fetch active and paused criteria."""
    selector = {
        'criterionUse': 'BIDDABLE',
        'userStatuses': ['ACTIVE', 'PAUSED']
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAllCriteriaCampaignLevel(self):
    """Test whether we can fetch criteria at campaign level."""
    selector = {
        'idFilters': [{
            'campaignId': self.__class__.campaign_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCriterion(self):
    """Test whether we can fetch criterion at criterion level."""
    if self.__class__.kw == None:
      self.testAddCriterionKeyword()
    selector = {
        'idFilters': [{
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterionId': self.__class__.kw['criterion']['id']
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testDeleteCriterion(self):
    """Test whether we can delete criterion at ad group level."""
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterion': {
              'id': self.__class__.kw['criterion']['id'],
            }
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
    self.testAddCriterionKeyword()

  def testUpdateCriterionKeywordStatus(self):
    """Test whether we can update a keyword's status."""
    if self.__class__.kw == None:
      self.testAddCriterionKeyword()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterion': {
              'id': self.__class__.kw['criterion']['id'],
            },
            'userStatus': 'PAUSED',
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

  def testUpdateCriterionKeywordBids(self):
    """Test whether we can update a keyword's bids."""
    if self.__class__.kw == None:
      self.testAddCriterionKeyword()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterion': {
              'id': self.__class__.kw['criterion']['id'],
            },
            'bids': {
                'type': 'ManualCPCAdGroupCriterionBids',
                'maxCpc': {
                    'amount': {
                        'microAmount': '500000'
                    }
                }
            }
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


class AdGroupCriterionServiceTestV201003(unittest.TestCase):

  """Unittest suite for AdGroupCriterionService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  campaign_id = '0'
  kw_ad_group_id = '0'
  place_ad_group_id = '0'
  kw = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAdGroupCriterionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if (self.__class__.campaign_id is '0' or
        self.__class__.kw_ad_group_id is '0' or
        self.__class__.place_ad_group_id is '0'):
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
      },
      {
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
      ad_groups = ad_group_service.Mutate(operations)[0]['value']
      self.__class__.kw_ad_group_id = ad_groups[0]['id']
      self.__class__.place_ad_group_id = ad_groups[1]['id']

  def testAddCriterionKeyword(self):
    """Test whether we can add an ad group criterion keyword."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw_ad_group_id,
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
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testAddCriterionPlacement(self):
    """Test whether we can add an ad group criterion placement."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.place_ad_group_id,
            'criterion': {
                'type': 'Placement',
                'url': 'www.example.com'
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

  def testAddKeywordCrossAdGroup(self):
    """Test whether we can add cross ad group keywords."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw_ad_group_id,
            'criterion': {
                'type': 'Keyword',
                'matchType': 'BROAD',
                'text': 'mars cruise'
            }
        }
    },
    {
        'operator': 'ADD',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.place_ad_group_id,
            'criterion': {
                'type': 'Placement',
                'url': 'www.example.com'
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

  def testGetAllActivePausedCriteria(self):
    """Test whether we can fetch active and paused criteria."""
    selector = {
        'criterionUse': 'BIDDABLE',
        'userStatuses': ['ACTIVE', 'PAUSED']
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAllCriteriaCampaignLevel(self):
    """Test whether we can fetch criteria at campaign level."""
    selector = {
        'idFilters': [{
            'campaignId': self.__class__.campaign_id
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCriterion(self):
    """Test whether we can fetch criterion at criterion level."""
    if self.__class__.kw == None:
      self.testAddCriterionKeyword()
    selector = {
        'idFilters': [{
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterionId': self.__class__.kw['criterion']['id']
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testDeleteCriterion(self):
    """Test whether we can delete criterion at ad group level."""
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterion': {
              'id': self.__class__.kw['criterion']['id'],
            }
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
    self.testAddCriterionKeyword()

  def testUpdateCriterionKeywordStatus(self):
    """Test whether we can update a keyword's status."""
    if self.__class__.kw == None:
      self.testAddCriterionKeyword()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterion': {
              'id': self.__class__.kw['criterion']['id'],
            },
            'userStatus': 'PAUSED',
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

  def testUpdateCriterionKeywordBids(self):
    """Test whether we can update a keyword's bids."""
    if self.__class__.kw == None:
      self.testAddCriterionKeyword()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': self.__class__.kw['adGroupId'],
            'criterion': {
              'id': self.__class__.kw['criterion']['id'],
            },
            'bids': {
                'type': 'ManualCPCAdGroupCriterionBids',
                'maxCpc': {
                    'amount': {
                        'microAmount': '500000'
                    }
                }
            }
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
  suite.addTests(unittest.makeSuite(AdGroupCriterionServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AdGroupCriterionServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
