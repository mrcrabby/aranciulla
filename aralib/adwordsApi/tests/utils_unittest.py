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

"""Unit tests to cover Utils."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from aw_api.SoapBuffer import SoapBuffer


class UtilsTest(unittest.TestCase):

  """Unittest suite for Utils."""

  TRIGGER_MSG = ('502 Server Error. The server encountered a temporary error'
                 ' and could not complete yourrequest. Please try again in 30 '
                 'seconds.')

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testError502(self):
    """Test whether we can handle and report 502 errors."""
    # Temporarily redirect STDOUT into a buffer.
    buf = SoapBuffer()
    sys.stdout = buf

    html_code = Utils.ReadFile(os.path.join('data', 'http_error_502.html'))
    print html_code

    # Restore STDOUT.
    sys.stdout = sys.__stdout__

    if not buf.IsHandshakeComplete():
      data = buf.GetBufferAsStr()
    else:
      data = ''

    self.assertEqual(Utils.GetErrorFromHtml(data), self.__class__.TRIGGER_MSG)

  def testDataFileCategories(self):
    """Test whether csv data file with categories is valid."""
    cols = 2
    for item in Utils.GetCategories():
      self.assertEqual(len(item), cols)

  def testDataFileCountries(self):
    """Test whether csv data file with countries is valid."""
    cols = 2
    for item in Utils.GetCountries():
      self.assertEqual(len(item), cols)

  def testDataFileCurrencies(self):
    """Test whether csv data file with currencies is valid."""
    cols = 2
    for item in Utils.GetCurrencies():
      self.assertEqual(len(item), cols)

  def testDataFileErrorCodes(self):
    """Test whether csv data file with error codes is valid."""
    cols = 2
    for item in Utils.GetErrorCodes():
      self.assertEqual(len(item), cols)

  def testDataFileLanguages(self):
    """Test whether csv data file with languages is valid."""
    cols = 3
    for item in Utils.GetLanguages():
      self.assertEqual(len(item), cols)

  def testDataFileOpsRates(self):
    """Test whether csv data file with ops rates is valid."""
    cols = 5
    for item in Utils.GetOpsRates():
      self.assertEqual(len(item), cols)

  def testDataFileTimezones(self):
    """Test whether csv data file with timezones is valid."""
    cols = 1
    for item in Utils.GetTimezones():
      self.assertEqual(len(item), cols)

  def testDataFileUsCities(self):
    """Test whether csv data file with us cities is valid."""
    cols = 2
    for item in Utils.GetUsCities():
      self.assertEqual(len(item), cols)

  def testDataFileUsMetros(self):
    """Test whether csv data file with us metros is valid."""
    cols = 3
    for item in Utils.GetUsMetros():
      self.assertEqual(len(item), cols)

  def testDataFileWorldCities(self):
    """Test whether csv data file with world cities is valid."""
    cols = 2
    for item in Utils.GetWorldCities():
      self.assertEqual(len(item), cols)

  def testDataFileWorldRegions(self):
    """Test whether csv data file with world regions is valid."""
    cols = 3
    for item in Utils.GetWorldRegions():
      self.assertEqual(len(item), cols)


def makeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UtilsTest))
  return suite


if __name__ == '__main__':
  suite = makeTestSuite()
  alltests = unittest.TestSuite([suite])
  unittest.main(defaultTest='alltests')
