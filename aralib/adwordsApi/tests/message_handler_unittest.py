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

"""Unit tests to cover message handler."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import unittest

from aw_api import ZSI
from tests import client


class MessageHandlerTest(unittest.TestCase):

  """Unittest suite for MessageHandler."""

  client.debug = False

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCustomPackListEmptyList(self):
    """Test whether function can handle an empty list."""
    obj = {}
    if client.soap_lib == ZSI:
      from aw_api.zsi_toolkit import MessageHandler
      obj = MessageHandler.CustomPackList([])

    self.assert_(isinstance(obj, dict))


def makeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(MessageHandlerTest))
  return suite


if __name__ == '__main__':
  suite = makeTestSuite()
  alltests = unittest.TestSuite([suite])
  unittest.main(defaultTest='alltests')
