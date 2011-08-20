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

"""Unit tests to cover AlertService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import client


class AlertServiceTestV201008(unittest.TestCase):

  """Unittest suite for AlertService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None
  ad_group_id = '0'
  criterion_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAlertService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetCampaignAlerts(self):
    """Test whether we can fetch existing campaign alerts."""
    selector = {
        'query': {
            'clientSpec': 'ALL',
            'filterSpec': 'ALL',
            'types': ['CAMPAIGN_ENDING', 'CAMPAIGN_ENDED'],
            'severities': ['GREEN', 'YELLOW', 'RED'],
            'triggerTimeSpec': 'ALL_TIME'
        },
        'paging': {
            'startIndex': '0',
            'numberResults': '100'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))


class AlertServiceTestV201101(unittest.TestCase):

  """Unittest suite for AlertService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None
  ad_group_id = '0'
  criterion_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetAlertService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetCampaignAlerts(self):
    """Test whether we can fetch existing campaign alerts."""
    selector = {
        'query': {
            'clientSpec': 'ALL',
            'filterSpec': 'ALL',
            'types': ['CAMPAIGN_ENDING', 'CAMPAIGN_ENDED'],
            'severities': ['GREEN', 'YELLOW', 'RED'],
            'triggerTimeSpec': 'ALL_TIME'
        },
        'paging': {
            'startIndex': '0',
            'numberResults': '100'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AlertServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(AlertServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v201008 = makeTestSuiteV201008()
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v201008, suite_v201101])
  unittest.main(defaultTest='alltests')
