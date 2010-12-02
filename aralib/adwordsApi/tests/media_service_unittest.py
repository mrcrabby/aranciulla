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

"""Unit tests to cover MediaService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import base64
import os
import sys
sys.path.append('..')
import unittest

from aw_api import SOAPPY
from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V201003
from tests import VERSION_V201003
from tests import client


class MediaServiceTestV201003(unittest.TestCase):

  """Unittest suite for MediaService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  IMAGE_DATA = Utils.ReadFile(os.path.join('data', 'image.jpg'))
  if client.soap_lib == SOAPPY:
    IMAGE_DATA = base64.encodestring(IMAGE_DATA)
  client.debug = False
  service = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetMediaService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testGetAllImageMedia(self):
    """Test whether we can fetch all existing image media."""
    selector = {
        'mediaType': 'IMAGE'
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testUploadImageMedia(self):
    """Test whether we can upload new image media."""
    media = [{
        'type': 'Image',
        'data': self.__class__.IMAGE_DATA,
        'mediaTypeDb': 'IMAGE',
        'name': 'Sample Image'
    }]
    self.assert_(isinstance(self.__class__.service.Upload(media), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'upload',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(MediaServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v201003])
  unittest.main(defaultTest='alltests')
