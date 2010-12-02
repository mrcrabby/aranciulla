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

"""Unit tests to cover CampaignService."""

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


class CampaignServiceTestV200909(unittest.TestCase):

  """Unittest suite for CampaignService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  campaign1 = None
  campaign2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testAddCampaign(self):
    """Test whether we can add campaign."""
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
                    'microAmount': '1000000'
                },
                'deliveryMethod': 'STANDARD'
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

  def testAddCampaigns(self):
    """Test whether we can add two campaigns."""
    operations = [
        {
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
                        'microAmount': '1000000'
                    },
                    'deliveryMethod': 'STANDARD'
                }
            }
        },
        {
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
        }
    ]
    campaigns = self.__class__.service.Mutate(operations)
    self.__class__.campaign1 = campaigns[0]['value'][0]
    self.__class__.campaign2 = campaigns[0]['value'][1]
    self.assert_(isinstance(campaigns, tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCampaign(self):
    """Test whether we can fetch an existing campaign."""
    if self.__class__.campaign1 == None:
      self.testAddCampaigns()
    selector = {
        'ids': [self.__class__.campaign1['id']],
        'statsSelector': {
            'dateRange': {
                 'max': '20090131',
                 'min': '20090101'
             }
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAllCampaigns(self):
    """Test whether we can fetch all existing campaigns."""
    selector = {
        'ids': []
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUpdateCampaign(self):
    """Test whether we can update an existing campaign."""
    if self.__class__.campaign1 == None:
      self.testAddCampaigns()
    operations = [{
        'operator': 'SET',
        'operand': {
            'id': self.__class__.campaign1['id'],
            'status': self.__class__.campaign1['status'],
            'budget': {
                'period': 'DAILY',
                'amount': {
                    'microAmount': '3000000'
                },
                'deliveryMethod': 'STANDARD'
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

  def testUpdateCampaignList(self):
    """Test whether we can update a list of existing campaign."""
    if self.__class__.campaign1 == None or self.__class__.campaign2 == None:
      self.testAddCampaigns()
    operations = [{
        'operator': 'SET',
        'operand': {
            'id': self.__class__.campaign1['id'],
            'status': self.__class__.campaign1['status'],
            'budget': {
                'period': 'DAILY',
                'amount': {
                    'microAmount': '3000000'
                },
                'deliveryMethod': 'STANDARD'
            }
        }
    },
    {
        'operator': 'SET',
        'operand': {
            'id': self.__class__.campaign2['id'],
            'status': self.__class__.campaign2['status'],
            'budget': {
                'period': 'DAILY',
                'amount': {
                    'microAmount': '4000000'
                },
                'deliveryMethod': 'STANDARD'
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


class CampaignServiceTestV201003(unittest.TestCase):

  """Unittest suite for CampaignService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  campaign1 = None
  campaign2 = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testAddCampaign(self):
    """Test whether we can add campaign."""
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
                    'microAmount': '1000000'
                },
                'deliveryMethod': 'STANDARD'
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

  def testAddCampaigns(self):
    """Test whether we can add two campaigns."""
    operations = [
        {
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
                        'microAmount': '1000000'
                    },
                    'deliveryMethod': 'STANDARD'
                }
            }
        },
        {
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
        }
    ]
    campaigns = self.__class__.service.Mutate(operations)
    self.__class__.campaign1 = campaigns[0]['value'][0]
    self.__class__.campaign2 = campaigns[0]['value'][1]
    self.assert_(isinstance(campaigns, tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'mutate.ADD',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCampaign(self):
    """Test whether we can fetch an existing campaign."""
    if self.__class__.campaign1 == None:
      self.testAddCampaigns()
    selector = {
        'ids': [self.__class__.campaign1['id']],
        'statsSelector': {
            'dateRange': {
                 'max': '20090131',
                 'min': '20090101'
             }
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAllCampaigns(self):
    """Test whether we can fetch all existing campaigns."""
    selector = {
        'ids': []
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUpdateCampaign(self):
    """Test whether we can update an existing campaign."""
    if self.__class__.campaign1 == None:
      self.testAddCampaigns()
    operations = [{
        'operator': 'SET',
        'operand': {
            'id': self.__class__.campaign1['id'],
            'status': self.__class__.campaign1['status'],
            'budget': {
                'period': 'DAILY',
                'amount': {
                    'microAmount': '3000000'
                },
                'deliveryMethod': 'STANDARD'
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

  def testUpdateCampaignList(self):
    """Test whether we can update a list of existing campaign."""
    if self.__class__.campaign1 == None or self.__class__.campaign2 == None:
      self.testAddCampaigns()
    operations = [{
        'operator': 'SET',
        'operand': {
            'id': self.__class__.campaign1['id'],
            'status': self.__class__.campaign1['status'],
            'budget': {
                'period': 'DAILY',
                'amount': {
                    'microAmount': '3000000'
                },
                'deliveryMethod': 'STANDARD'
            }
        }
    },
    {
        'operator': 'SET',
        'operand': {
            'id': self.__class__.campaign2['id'],
            'status': self.__class__.campaign2['status'],
            'budget': {
                'period': 'DAILY',
                'amount': {
                    'microAmount': '4000000'
                },
                'deliveryMethod': 'STANDARD'
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
  suite.addTests(unittest.makeSuite(CampaignServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
