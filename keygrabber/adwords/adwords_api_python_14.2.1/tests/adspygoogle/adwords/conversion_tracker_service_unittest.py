#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Unit tests to cover ConversionTrackerService."""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import client
from adspygoogle.common import Utils


class ConversionTrackerServiceTestV201101(unittest.TestCase):

  """Unittest suite for ConversionTrackerService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetConversionTrackerService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testAddConversion(self):
    """Test whether we can add a conversion."""
    operations = [
        {
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'AdWordsConversionTracker',
                'name': 'Mars cruise customers #%s' % Utils.GetUniqueName(),
                'category': 'DEFAULT',
                'markupLanguage': 'HTML',
                'httpProtocol': 'HTTP',
                'textFormat': 'HIDDEN'
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testGetAllConversions(self):
    """Test whether we can retrieve all conversions."""
    selector = {
        'fields': ['Name', 'Status', 'Category'],
        'ordering': [{
            'field': 'Name',
            'sortOrder': 'ASCENDING'
        }]
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ConversionTrackerServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v201101])
  unittest.main(defaultTest='alltests')
