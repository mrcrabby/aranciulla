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

"""Unit tests to cover TrafficEstimator."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V13
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import VERSION_V13
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import client


class TrafficEstimatorServiceTestV13(unittest.TestCase):

  """Unittest suite for TrafficEstimatorService using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetTrafficEstimatorService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testCheckKeywordTraffic(self):
    """Test whether we can check keyword traffic."""
    requests = [{
        'keywordText': 'Flowers',
        'keywordType': 'Broad',
        'language': 'en'
    }]
    self.assert_(isinstance(
        self.__class__.service.CheckKeywordTraffic(requests), tuple))

  def testEstimateAdGroupList(self):
    """Test whether we can estimate ad group list."""
    requests = [{
        'keywordRequests': [{
            'maxCpc': '1000000',
            'negative': 'False',
            'text': 'Flowers',
            'type': 'Broad'
          }],
        'maxCpc': '1000000'
    }]
    self.assert_(isinstance(
        self.__class__.service.EstimateAdGroupList(requests), tuple))

  def testEstimateCampaignList(self):
    """Test wheter we can estimate campaign list."""
    requests = [{
        'adGroupRequests': [{
            'keywordRequests': [{
                'maxCpc': '1000000',
                'negative': 'False',
                'text': 'Flowers',
                'type': 'Broad'
              }],
            'maxCpc': '1000000'
        }],
        'geoTargeting': {
            'cityTargets': {
                'cities': ['New York, NY US'],
            }
        },
        'languageTargeting': ['en'],
        'networkTargeting': ['GoogleSearch', 'SearchNetwork']
    }]
    self.assert_(isinstance(
        self.__class__.service.EstimateCampaignList(requests), tuple))

  def testEstimateKeywordList(self):
    """Test whether we can estimate keyword list."""
    requests = [{
        'maxCpc': '1000000',
        'negative': 'False',
        'text': 'Flowers',
        'type': 'Broad'
    },
    {
        'maxCpc': '2000000',
        'negative': 'False',
        'text': 'House',
        'type': 'Broad'
    }]
    self.assert_(isinstance(
        self.__class__.service.EstimateKeywordList(requests), tuple))

  def testEstimateKeywordListOneItem(self):
    """Test whether we can estimate keyword list, with only one keyword."""
    requests = [{
        'maxCpc': '1000000',
        'negative': 'False',
        'text': 'Flowers',
        'type': 'Broad'
    }]
    self.assert_(isinstance(
        self.__class__.service.EstimateKeywordList(requests), tuple))


class TrafficEstimatorServiceTestV201008(unittest.TestCase):

  """Unittest suite for TrafficEstimatorService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetTrafficEstimatorService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testKeywordTrafficEstimates(self):
    """Test whether we can estimate keyword traffic."""
    selector = {
        'campaignEstimateRequests': [{
            'adGroupEstimateRequests': [{
                'keywordEstimateRequests': [
                    {
                        'keyword': {
                            'xsi_type': 'Keyword',
                            'matchType': 'BROAD',
                            'text': 'mars cruise'
                        },
                        'maxCpc': {
                            'xsi_type': 'Money',
                            'microAmount': '1000000'
                        }
                    },
                    {
                        'keyword': {
                            'xsi_type': 'Keyword',
                            'matchType': 'PHRASE',
                            'text': 'cheap cruise'
                        },
                        'maxCpc': {
                            'xsi_type': 'Money',
                            'microAmount': '1000000'
                        }
                    },
                    {
                        'keyword': {
                            'xsi_type': 'Keyword',
                            'matchType': 'EXACT',
                            'text': 'cruise'
                        },
                        'maxCpc': {
                            'xsi_type': 'Money',
                            'microAmount': '1000000'
                        }
                    }
                ],
                'maxCpc': {
                    'xsi_type': 'Money',
                    'microAmount': '1000000'
                }
            }],
            'targets': [
                {
                    'xsi_type': 'CountryTarget',
                    'countryCode': 'US'
                },
                {
                    'xsi_type': 'LanguageTarget',
                    'languageCode': 'en'
                }
            ]
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))


class TrafficEstimatorServiceTestV201101(unittest.TestCase):

  """Unittest suite for TrafficEstimatorService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetTrafficEstimatorService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testKeywordTrafficEstimates(self):
    """Test whether we can estimate keyword traffic."""
    selector = {
        'campaignEstimateRequests': [{
            'adGroupEstimateRequests': [{
                'keywordEstimateRequests': [
                    {
                        'keyword': {
                            'xsi_type': 'Keyword',
                            'matchType': 'BROAD',
                            'text': 'mars cruise'
                        },
                        'maxCpc': {
                            'xsi_type': 'Money',
                            'microAmount': '1000000'
                        }
                    },
                    {
                        'keyword': {
                            'xsi_type': 'Keyword',
                            'matchType': 'PHRASE',
                            'text': 'cheap cruise'
                        },
                        'maxCpc': {
                            'xsi_type': 'Money',
                            'microAmount': '1000000'
                        }
                    },
                    {
                        'keyword': {
                            'xsi_type': 'Keyword',
                            'matchType': 'EXACT',
                            'text': 'cruise'
                        },
                        'maxCpc': {
                            'xsi_type': 'Money',
                            'microAmount': '1000000'
                        }
                    }
                ],
                'maxCpc': {
                    'xsi_type': 'Money',
                    'microAmount': '1000000'
                }
            }],
            'targets': [
                {
                    'xsi_type': 'CountryTarget',
                    'countryCode': 'US'
                },
                {
                    'xsi_type': 'LanguageTarget',
                    'languageCode': 'en'
                }
            ]
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TrafficEstimatorServiceTestV13))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TrafficEstimatorServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TrafficEstimatorServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v13 = makeTestSuiteV13()
  suite_v201008 = makeTestSuiteV201008()
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v13, suite_v201008, suite_v201101])
  unittest.main(defaultTest='alltests')
