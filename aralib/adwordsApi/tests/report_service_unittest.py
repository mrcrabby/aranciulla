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

"""Unit tests to cover ReportService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V13
from tests import VERSION_V13
from tests import client


class ReportServiceTestV13(unittest.TestCase):

  """Unittest suite for ReportService using v13."""

  SERVER = SERVER_V13
  VERSION = VERSION_V13
  client.debug = False
  service = None
  PENDING_REPORT_JOB_ID = '11'
  INPROGRESS_REPORT_JOB_ID = '22'
  COMPLETED_REPORT_JOB_ID = '33'
  FAILED_REPORT_JOB_ID = '44'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testDeleteReport(self):
    """Test whether we can delete an existing report."""
    self.assertEqual(self.__class__.service.DeleteReport(
        self.__class__.FAILED_REPORT_JOB_ID), None)
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'deleteReport',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAllJobs(self):
    """Test whether we can fetch all existing report jobs."""
    self.assert_(isinstance(self.__class__.service.GetAllJobs(), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getAllJobs',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetGzipReportDownloadUrl(self):
    """Test whether we can fetch a Gzip report download URL."""
    self.assert_(isinstance(self.__class__.service.GetGzipReportDownloadUrl(
        self.__class__.COMPLETED_REPORT_JOB_ID), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getGzipReportDownloadUrl',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetReportDownloadUrl(self):
    """Test whether we can fetch a report download URL."""
    self.assert_(isinstance(self.__class__.service.GetReportDownloadUrl(
        self.__class__.COMPLETED_REPORT_JOB_ID), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getReportDownloadUrl',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetReportJobStatus(self):
    """Test whether we can fetch report job status."""
    self.assert_(isinstance(self.__class__.service.GetReportJobStatus(
        self.__class__.PENDING_REPORT_JOB_ID), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'getReportJobStatus',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testScheduleDefinedReportJob(self):
    """Test whether we can schedule a defined report job."""
    job = {
        'adWordsType': 'SearchOnly',
        'aggregationTypes': ['Daily'],
        'campaignStatuses': ['Active', 'Paused'],
        'crossClient': 'False',
        'endDay': '2009-01-31',
        'includeZeroImpression': 'False',
        'name': 'Test Report',
        'selectedColumns': ['Campaign', 'CampaignId', 'CPC', 'CTR'],
        'selectedReportType': 'Campaign',
        'startDay': '2009-01-01',
    }
    self.assert_(isinstance(
        self.__class__.service.ScheduleDefinedReportJob(job), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'scheduleReportJob',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testValidateReportJob(self):
    """Test whether we can validate a report job"""
    job = {
        'adWordsType': 'SearchOnly',
        'aggregationTypes': ['Daily'],
        'campaignStatuses': ['Active', 'Paused'],
        'crossClient': 'False',
        'endDay': '2009-01-31',
        'includeZeroImpression': 'False',
        'name': 'Test Report',
        'selectedColumns': ['Campaign', 'CampaignId', 'CPC', 'CTR'],
        'selectedReportType': 'Campaign',
        'startDay': '2009-01-01',
    }
    self.assertEqual(self.__class__.service.ValidateReportJob(job), None)
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'validateReportJob',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testValidateReportJobStructure(self):
    """Test whether we can validate a structure report job."""
    job = {
        'aggregationTypes': ['Keyword'],
        'name': 'Test Report',
        'selectedColumns': ['CampaignId', 'AdGroupId', 'KeywordId', 'Keyword'],
        'selectedReportType': 'Structure'
    }
    self.assertEqual(self.__class__.service.ValidateReportJob(job), None)
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'validateReportJob',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testDownloadXmlReport(self):
    """Test whether we can download xml report."""
    self.assert_(isinstance(self.__class__.service.DownloadXmlReport(
        self.__class__.COMPLETED_REPORT_JOB_ID), str))

  def testDownloadCsvReport(self):
    """Test whether we can download a csv report."""
    self.assert_(isinstance(self.__class__.service.DownloadCsvReport(
        self.__class__.COMPLETED_REPORT_JOB_ID), str))

  def testDownloadCsvReportNonAscii(self):
    """Test whether we can download a csv report that includes non-ASCII data
    using."""
    xml = Utils.ReadFile(os.path.join('data', 'report_non_ascii.xml'))
    self.assert_(isinstance(self.__class__.service.DownloadCsvReport(
        self.__class__.COMPLETED_REPORT_JOB_ID, xml), (str, unicode)))


def makeTestSuiteV13():
  """Set up test suite using v13.

  Returns:
    TestSuite test suite using v13.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportServiceTestV13))
  return suite


if __name__ == '__main__':
  suite_v13 = makeTestSuiteV13()
  alltests = unittest.TestSuite([suite_v13])
  unittest.main(defaultTest='alltests')
