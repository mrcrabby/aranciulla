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

"""Unit tests to cover CampaignTargetService."""

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
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import VERSION_V200909
from tests.adspygoogle.adwords import VERSION_V201003
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import client


class CampaignTargetServiceTestV200909(unittest.TestCase):

  """Unittest suite for CampaignTargetService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  campaign_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignTargetService(
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
      self.__class__.campaign_id = campaign_service.Mutate(
          operations)[0]['value'][0]['id']

  def testGetAllTargets(self):
    """Test whether we can fetch all existing targets for given campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testAddAdScheduleTarget(self):
    """Test whether we can add an ad schedule target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'AdScheduleTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'type': 'AdScheduleTarget',
                'dayOfWeek': 'MONDAY',
                'startHour': '8',
                'startMinute': 'ZERO',
                'endHour': '17',
                'endMinute': 'ZERO',
                'bidMultiplier': '1.0',
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddDemographicTarget(self):
    """Test whether we can add an age target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'DemographicTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [
                {
                    'type': 'AgeTarget',
                    'age': 'AGE_18_24'
                },
                {
                    'type': 'GenderTarget',
                    'gender': 'FEMALE'
                }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddGeoTarget(self):
    """Test whether we can add a geo target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'type': 'CityTarget',
                'cityName': 'New York',
                'countryCode': 'US'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddNetworkLanguageTargets(self):
    """Test whether we can add a network and language targets to campaign."""
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'type': 'LanguageTargetList',
                'campaignId': self.__class__.campaign_id,
                'targets': [{
                    'type': 'LanguageTarget',
                    'languageCode': 'en'
                }]
            }
        },
        {
            'operator': 'SET',
            'operand': {
                'type': 'NetworkTargetList',
                'campaignId': self.__class__.campaign_id,
                'targets': [{
                    'type': 'NetworkTarget',
                    'networkCoverageType': 'GOOGLE_SEARCH'
                },
                {
                    'type': 'NetworkTarget',
                    'networkCoverageType': 'CONTENT_NETWORK'
                }]
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddPlatformTarget(self):
    """Test whether we can add a platform target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'PlatformTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'type': 'PlatformTarget',
                'platformType': 'HIGH_END_MOBILE'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testRemoveGeoTarget(self):
    """Test whether we can remove a geo target in campaign."""
    if self.__class__.campaign_id == '0':
      self.testAddGeoTarget()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': []
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


class CampaignTargetServiceTestV201003(unittest.TestCase):

  """Unittest suite for CampaignTargetService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  campaign_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignTargetService(
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
      self.__class__.campaign_id = campaign_service.Mutate(
          operations)[0]['value'][0]['id']

  def testGetAllTargets(self):
    """Test whether we can fetch all existing targets for given campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testAddAdScheduleTarget(self):
    """Test whether we can add an ad schedule target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'AdScheduleTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'type': 'AdScheduleTarget',
                'dayOfWeek': 'MONDAY',
                'startHour': '8',
                'startMinute': 'ZERO',
                'endHour': '17',
                'endMinute': 'ZERO',
                'bidMultiplier': '1.0',
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddDemographicTarget(self):
    """Test whether we can add an age target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'DemographicTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [
                {
                    'type': 'AgeTarget',
                    'age': 'AGE_18_24'
                },
                {
                    'type': 'GenderTarget',
                    'gender': 'FEMALE'
                }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddGeoTarget(self):
    """Test whether we can add a geo target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'type': 'CityTarget',
                'cityName': 'New York',
                'countryCode': 'US'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddNetworkLanguageTargets(self):
    """Test whether we can add a network and language targets to campaign."""
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'type': 'LanguageTargetList',
                'campaignId': self.__class__.campaign_id,
                'targets': [{
                    'type': 'LanguageTarget',
                    'languageCode': 'en'
                }]
            }
        },
        {
            'operator': 'SET',
            'operand': {
                'type': 'NetworkTargetList',
                'campaignId': self.__class__.campaign_id,
                'targets': [{
                    'type': 'NetworkTarget',
                    'networkCoverageType': 'GOOGLE_SEARCH'
                },
                {
                    'type': 'NetworkTarget',
                    'networkCoverageType': 'CONTENT_NETWORK'
                }]
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddPlatformTarget(self):
    """Test whether we can add a platform target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'PlatformTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'type': 'PlatformTarget',
                'platformType': 'HIGH_END_MOBILE'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testRemoveGeoTarget(self):
    """Test whether we can remove a geo target in campaign."""
    if self.__class__.campaign_id == '0':
      self.testAddGeoTarget()
    operations = [{
        'operator': 'SET',
        'operand': {
            'type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': []
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


class CampaignTargetServiceTestV201008(unittest.TestCase):

  """Unittest suite for CampaignTargetService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None
  campaign_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignTargetService(
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
      self.__class__.campaign_id = campaign_service.Mutate(
          operations)[0]['value'][0]['id']

  def testGetAllTargets(self):
    """Test whether we can fetch all existing targets for given campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testAddAdScheduleTarget(self):
    """Test whether we can add an ad schedule target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'AdScheduleTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'AdScheduleTarget',
                'dayOfWeek': 'MONDAY',
                'startHour': '8',
                'startMinute': 'ZERO',
                'endHour': '17',
                'endMinute': 'ZERO',
                'bidMultiplier': '1.0',
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddDemographicTarget(self):
    """Test whether we can add an age target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'DemographicTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [
                {
                    'xsi_type': 'AgeTarget',
                    'age': 'AGE_18_24'
                },
                {
                    'xsi_type': 'GenderTarget',
                    'gender': 'FEMALE'
                }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddGeoTarget(self):
    """Test whether we can add a geo target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'CityTarget',
                'cityName': 'New York',
                'countryCode': 'US'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddNetworkLanguageTargets(self):
    """Test whether we can add a network and language targets to campaign."""
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'xsi_type': 'LanguageTargetList',
                'campaignId': self.__class__.campaign_id,
                'targets': [{
                    'xsi_type': 'LanguageTarget',
                    'languageCode': 'en'
                }]
            }
        },
        {
            'operator': 'SET',
            'operand': {
                'xsi_type': 'NetworkTargetList',
                'campaignId': self.__class__.campaign_id,
                'targets': [{
                    'xsi_type': 'NetworkTarget',
                    'networkCoverageType': 'GOOGLE_SEARCH'
                },
                {
                    'xsi_type': 'NetworkTarget',
                    'networkCoverageType': 'CONTENT_NETWORK'
                }]
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddPlatformTarget(self):
    """Test whether we can add a platform target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'PlatformTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'PlatformTarget',
                'platformType': 'HIGH_END_MOBILE'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddMobileCarrierTarget(self):
    """Test whether we can add a mobile carrier target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'MobileTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'MobileCarrierTarget',
                'carrierName': 'Verizon',
                'countryCode': 'US'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddMobilePlatformTarget(self):
    """Test whether we can add a mobile platform target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'MobileTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'MobilePlatformTarget',
                'platformName': 'Android'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testRemoveGeoTarget(self):
    """Test whether we can remove a geo target in campaign."""
    if self.__class__.campaign_id == '0':
      self.testAddGeoTarget()
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': []
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


class CampaignTargetServiceTestV201101(unittest.TestCase):

  """Unittest suite for CampaignTargetService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None
  campaign_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetCampaignTargetService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign_id == '0':
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
      self.__class__.campaign_id = campaign_service.Mutate(
          operations)[0]['value'][0]['id']

  def testGetAllTargets(self):
    """Test whether we can fetch all existing targets for given campaign."""
    selector = {
        'campaignIds': [self.__class__.campaign_id]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))

  def testAddAdScheduleTarget(self):
    """Test whether we can add an ad schedule target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'AdScheduleTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'AdScheduleTarget',
                'dayOfWeek': 'MONDAY',
                'startHour': '8',
                'startMinute': 'ZERO',
                'endHour': '17',
                'endMinute': 'ZERO',
                'bidMultiplier': '1.0',
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddDemographicTarget(self):
    """Test whether we can add an age target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'DemographicTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [
                {
                    'xsi_type': 'AgeTarget',
                    'age': 'AGE_18_24'
                },
                {
                    'xsi_type': 'GenderTarget',
                    'gender': 'FEMALE'
                }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddGeoTarget(self):
    """Test whether we can add a geo target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'CityTarget',
                'cityName': 'New York',
                'countryCode': 'US'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddPlatformTarget(self):
    """Test whether we can add a platform target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'PlatformTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'PlatformTarget',
                'platformType': 'HIGH_END_MOBILE'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddMobileCarrierTarget(self):
    """Test whether we can add a mobile carrier target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'MobileTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'MobileCarrierTarget',
                'carrierName': 'Verizon',
                'countryCode': 'US'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddMobilePlatformTarget(self):
    """Test whether we can add a mobile platform target to campaign."""
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'MobileTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': [{
                'xsi_type': 'MobilePlatformTarget',
                'platformName': 'Android'
            }]
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testRemoveGeoTarget(self):
    """Test whether we can remove a geo target in campaign."""
    if self.__class__.campaign_id == '0':
      self.testAddGeoTarget()
    operations = [{
        'operator': 'SET',
        'operand': {
            'xsi_type': 'GeoTargetList',
            'campaignId': self.__class__.campaign_id,
            'targets': []
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignTargetServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignTargetServiceTestV201003))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignTargetServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(CampaignTargetServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  suite_v201008 = makeTestSuiteV201008()
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003, suite_v201008,
                                 suite_v201101])
  unittest.main(defaultTest='alltests')
