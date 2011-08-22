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

"""Unit tests to cover CampaignService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest
from datetime import date

from adspygoogle.common import Utils
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
            'endDate': date(date.today().year + 1, 12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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

  def testGetCampaign(self):
    """Test whether we can fetch an existing campaign."""
    if self.__class__.campaign1 is None:
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

  def testGetAllCampaigns(self):
    """Test whether we can fetch all existing campaigns."""
    selector = {
        'ids': []
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testUpdateCampaign(self):
    """Test whether we can update an existing campaign."""
    if self.__class__.campaign1 is None:
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

  def testUpdateCampaignList(self):
    """Test whether we can update a list of existing campaign."""
    if self.__class__.campaign1 is None or self.__class__.campaign2 is None:
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
            'endDate': date(date.today().year + 1, 12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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

  def testGetCampaign(self):
    """Test whether we can fetch an existing campaign."""
    if self.__class__.campaign1 is None:
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

  def testGetAllCampaigns(self):
    """Test whether we can fetch all existing campaigns."""
    selector = {
        'ids': []
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testUpdateCampaign(self):
    """Test whether we can update an existing campaign."""
    if self.__class__.campaign1 is None:
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

  def testUpdateCampaignList(self):
    """Test whether we can update a list of existing campaign."""
    if self.__class__.campaign1 is None or self.__class__.campaign2 is None:
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


class CampaignServiceTestV201008(unittest.TestCase):

  """Unittest suite for CampaignService using v201003."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
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
            'endDate': date(date.today().year + 1, 12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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

  def testGetCampaign(self):
    """Test whether we can fetch an existing campaign."""
    if self.__class__.campaign1 is None:
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

  def testGetAllCampaigns(self):
    """Test whether we can fetch all existing campaigns."""
    selector = {
        'ids': []
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testUpdateCampaign(self):
    """Test whether we can update an existing campaign."""
    if self.__class__.campaign1 is None:
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

  def testUpdateCampaignList(self):
    """Test whether we can update a list of existing campaign."""
    if self.__class__.campaign1 is None or self.__class__.campaign2 is None:
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


class CampaignServiceTestV201101(unittest.TestCase):

  """Unittest suite for CampaignService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
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
            'endDate': date(date.today().year + 1, 12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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
                'endDate': date(date.today().year + 1,
                                12, 31).strftime('%Y%m%d'),
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

  def testGetCampaign(self):
    """Test whether we can fetch an existing campaign."""
    if self.__class__.campaign1 is None:
      self.testAddCampaigns()
    selector = {
        'fields': ['Id', 'Name', 'Status'],
        'predicates': [{
            'field': 'CampaignId',
            'operator': 'EQUALS',
            'values': [self.__class__.campaign1['id']]
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testGetAllCampaigns(self):
    """Test whether we can fetch all existing campaigns."""
    selector = {
        'fields': ['Id', 'Name', 'Status']
    }

    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testUpdateCampaign(self):
    """Test whether we can update an existing campaign."""
    if self.__class__.campaign1 is None:
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

  def testUpdateCampaignList(self):
    """Test whether we can update a list of existing campaign."""
    if self.__class__.campaign1 is None or self.__class__.campaign2 is None:
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


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  suite_v201008 = makeTestSuiteV201008()
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003, suite_v201008,
                                 suite_v201101])
  unittest.main(defaultTest='alltests')
