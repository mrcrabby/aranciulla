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

"""Unit tests to cover Logger."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import logging
import os
import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V13
from tests import VERSION_V13
from tests import client


class LoggerTestV13(unittest.TestCase):

  """Unittest suite for Logger using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  TMP_LOG = os.path.join('..', 'logs', 'logger_unittest.log')
  DEBUG_MSG1 = 'Message before call to an API method.'
  DEBUG_MSG2 = 'Message after call to an API method.'
  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testUpperStackLogging(self):
    """Tests whether we can define logger at client level and log before and
    after the API request is made."""
    logger = logging.getLogger('LoggerTest')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(self.__class__.TMP_LOG)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # Clean up temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)

    logger.debug(self.__class__.DEBUG_MSG1)
    account_service = client.GetAccountService(
        self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
    account_service.GetAccountInfo()
    logger.debug(self.__class__.DEBUG_MSG2)

    data = Utils.ReadFile(self.__class__.TMP_LOG)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG1), 0)
    self.assertEqual(data.find(self.__class__.DEBUG_MSG2),
                     len(self.__class__.DEBUG_MSG1) + 1)

    # Clean up and remove temporary log file.
    Utils.PurgeLog(self.__class__.TMP_LOG)
    os.remove(self.__class__.TMP_LOG)


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(LoggerTestV13))
  return suite


if __name__ == '__main__':
  suite_v13 = makeTestSuiteV13()
  alltests = unittest.TestSuite([suite_v13])
  unittest.main(defaultTest='alltests')
