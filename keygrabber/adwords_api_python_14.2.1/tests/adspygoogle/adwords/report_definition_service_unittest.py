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

"""Unit tests to cover ReportDefinitionService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V201003
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import VERSION_V201003
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import client


class ReportDefinitionServiceTestV201003(unittest.TestCase):

  """Unittest suite for ReportDefinitionService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  ad_group_id = '0'
  report_definition_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportDefinitionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_group_id == '0':
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
      campaign_id = campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id,
              'name': 'AdGroup #%s' % Utils.GetUniqueName(),
              'status': 'ENABLED',
              'bids': {
                  'type': 'ManualCPCAdGroupBids',
                  'keywordMaxCpc': {
                      'amount': {
                          'microAmount': '1000000'
                      }
                  }
              }
          }
      }]
      ad_groups = ad_group_service.Mutate(operations)[0]['value']
      self.__class__.ad_group_id = ad_groups[0]['id']

  def testGetAllReportDefinitions(self):
    """Test whether we can fetch all existing report definitions."""
    selector = {}
    self.assert_(isinstance(self.__class__.service.Get(selector),
                            tuple))

  def testGetKeywordsPerformanceReportFields(self):
    """Test whether we can fetch report fields for keywords performance report
    type."""
    report_type = 'KEYWORDS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad performance report
    type."""
    report_type = 'AD_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetUrlPerformanceReportFields(self):
    """Test whether we can fetch report fields for url performance report
    type."""
    report_type = 'URL_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdGroupPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad group performance report
    type."""
    report_type = 'ADGROUP_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign performance report
    type."""
    report_type = 'CAMPAIGN_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetSearchQueryPerformanceReportFields(self):
    """Test whether we can fetch report fields for search query performance
    report type."""
    report_type = 'SEARCH_QUERY_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetManagedPlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for managed placements
    performance report type."""
    report_type = 'MANAGED_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAutomaticPlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for automatic placements
    performance report type."""
    report_type = 'AUTOMATIC_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdGroupNegativeKeywordsPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad group negative keywords
    performance report type."""
    report_type = 'ADGROUP_NEGATIVE_KEYWORDS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignNegativeKeywordsPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign negative keywords
    performance report type."""
    report_type = 'CAMPAIGN_NEGATIVE_KEYWORDS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdGroupNegativePlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad group negative placements
    performance report type."""
    report_type = 'ADGROUP_NEGATIVE_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignNegativePlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign negative placements
    performance report type."""
    report_type = 'CAMPAIGN_NEGATIVE_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testAddKeywordPerformanceReport(self):
    """Test whether we can add a keywords performance report."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'type': 'ReportDefinition',
            'reportName': ('Keywords performance report #%s'
                           % Utils.GetUniqueName()),
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
            'downloadFormat': 'XML',
            'selector': {
                'fields': ['AdGroupId', 'Id', 'KeywordText', 'KeywordMatchType',
                           'Impressions', 'Clicks', 'Cost'],
                'predicates': [{
                    'field': 'AdGroupId',
                    'operator': 'EQUALS',
                    'values': [self.__class__.ad_group_id]
                }],
                'dateRange': {
                    'min': '20100101',
                    'max': '20100131'
                }
            }
        }
    }]
    report_definition = self.__class__.service.Mutate(operations)
    self.__class__.report_definition_id = report_definition[0]['id']
    self.assert_(isinstance(report_definition, tuple))

  def testDeleteReportDefinition(self):
    """Test wether we can delete report definition."""
    if self.__class__.report_definition_id == '0':
      self.testAddKeywordPerformanceReport()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'id': self.__class__.report_definition_id
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


class ReportDefinitionServiceTestV201008(unittest.TestCase):

  """Unittest suite for ReportDefinitionService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None
  ad_group_id = '0'
  report_definition_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportDefinitionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_group_id == '0':
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
      campaign_id = campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id,
              'name': 'AdGroup #%s' % Utils.GetUniqueName(),
              'status': 'ENABLED',
              'bids': {
                  'xsi_type': 'ManualCPCAdGroupBids',
                  'keywordMaxCpc': {
                      'amount': {
                          'microAmount': '1000000'
                      }
                  }
              }
          }
      }]
      ad_groups = ad_group_service.Mutate(operations)[0]['value']
      self.__class__.ad_group_id = ad_groups[0]['id']

  def testGetAllReportDefinitions(self):
    """Test whether we can fetch all existing report definitions."""
    selector = {}
    self.assert_(isinstance(self.__class__.service.Get(selector),
                            tuple))

  def testGetKeywordsPerformanceReportFields(self):
    """Test whether we can fetch report fields for keywords performance report
    type."""
    report_type = 'KEYWORDS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad performance report
    type."""
    report_type = 'AD_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetUrlPerformanceReportFields(self):
    """Test whether we can fetch report fields for url performance report
    type."""
    report_type = 'URL_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdGroupPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad group performance report
    type."""
    report_type = 'ADGROUP_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign performance report
    type."""
    report_type = 'CAMPAIGN_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetSearchQueryPerformanceReportFields(self):
    """Test whether we can fetch report fields for search query performance
    report type."""
    report_type = 'SEARCH_QUERY_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetManagedPlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for managed placements
    performance report type."""
    report_type = 'MANAGED_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAutomaticPlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for automatic placements
    performance report type."""
    report_type = 'AUTOMATIC_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignNegativeKeywordsPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign negative keywords
    performance report type."""
    report_type = 'CAMPAIGN_NEGATIVE_KEYWORDS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignNegativePlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign negative placements
    performance report type."""
    report_type = 'CAMPAIGN_NEGATIVE_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAccountPerformanceReportFields(self):
    """Test whether we can fetch report fields for account performance report
    type."""
    report_type = 'ACCOUNT_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testAddKeywordPerformanceReport(self):
    """Test whether we can add a keywords performance report."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'xsi_type': 'ReportDefinition',
            'reportName': ('Keywords performance report #%s'
                           % Utils.GetUniqueName()),
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
            'downloadFormat': 'XML',
            'selector': {
                'fields': ['AdGroupId', 'Id', 'KeywordText', 'KeywordMatchType',
                           'Impressions', 'Clicks', 'Cost'],
                'predicates': [{
                    'field': 'AdGroupId',
                    'operator': 'EQUALS',
                    'values': [self.__class__.ad_group_id]
                }],
                'dateRange': {
                    'min': '20100101',
                    'max': '20100131'
                }
            }
        }
    }]
    report_definition = self.__class__.service.Mutate(operations)
    self.__class__.report_definition_id = report_definition[0]['id']
    self.assert_(isinstance(report_definition, tuple))

  def testDeleteReportDefinition(self):
    """Test wether we can delete report definition."""
    if self.__class__.report_definition_id == '0':
      self.testAddKeywordPerformanceReport()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'id': self.__class__.report_definition_id
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


class ReportDefinitionServiceTestV201101(unittest.TestCase):

  """Unittest suite for ReportDefinitionService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None
  ad_group_id = '0'
  report_definition_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetReportDefinitionService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_group_id == '0':
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
      campaign_id = campaign_service.Mutate(operations)[0]['value'][0]['id']
      ad_group_service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      operations = [{
          'operator': 'ADD',
          'operand': {
              'campaignId': campaign_id,
              'name': 'AdGroup #%s' % Utils.GetUniqueName(),
              'status': 'ENABLED',
              'bids': {
                  'xsi_type': 'ManualCPCAdGroupBids',
                  'keywordMaxCpc': {
                      'amount': {
                          'microAmount': '1000000'
                      }
                  }
              }
          }
      }]
      ad_groups = ad_group_service.Mutate(operations)[0]['value']
      self.__class__.ad_group_id = ad_groups[0]['id']

  def testGetAllReportDefinitions(self):
    """Test whether we can fetch all existing report definitions."""
    selector = {}
    self.assert_(isinstance(self.__class__.service.Get(selector),
                            tuple))

  def testGetKeywordsPerformanceReportFields(self):
    """Test whether we can fetch report fields for keywords performance report
    type."""
    report_type = 'KEYWORDS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad performance report
    type."""
    report_type = 'AD_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetUrlPerformanceReportFields(self):
    """Test whether we can fetch report fields for url performance report
    type."""
    report_type = 'URL_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAdGroupPerformanceReportFields(self):
    """Test whether we can fetch report fields for ad group performance report
    type."""
    report_type = 'ADGROUP_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign performance report
    type."""
    report_type = 'CAMPAIGN_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetSearchQueryPerformanceReportFields(self):
    """Test whether we can fetch report fields for search query performance
    report type."""
    report_type = 'SEARCH_QUERY_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetManagedPlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for managed placements
    performance report type."""
    report_type = 'MANAGED_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAutomaticPlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for automatic placements
    performance report type."""
    report_type = 'AUTOMATIC_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignNegativeKeywordsPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign negative keywords
    performance report type."""
    report_type = 'CAMPAIGN_NEGATIVE_KEYWORDS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetCampaignNegativePlacementsPerformanceReportFields(self):
    """Test whether we can fetch report fields for campaign negative placements
    performance report type."""
    report_type = 'CAMPAIGN_NEGATIVE_PLACEMENTS_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testGetAccountPerformanceReportFields(self):
    """Test whether we can fetch report fields for account performance report
    type."""
    report_type = 'ACCOUNT_PERFORMANCE_REPORT'
    self.assert_(isinstance(self.__class__.service.GetReportFields(report_type),
                            tuple))

  def testAddKeywordPerformanceReport(self):
    """Test whether we can add a keywords performance report."""
    operations = [{
        'operator': 'ADD',
        'operand': {
            'xsi_type': 'ReportDefinition',
            'reportName': ('Keywords performance report #%s'
                           % Utils.GetUniqueName()),
            'dateRangeType': 'CUSTOM_DATE',
            'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
            'downloadFormat': 'XML',
            'selector': {
                'fields': ['AdGroupId', 'Id', 'KeywordText', 'KeywordMatchType',
                           'Impressions', 'Clicks', 'Cost'],
                'predicates': [{
                    'field': 'AdGroupId',
                    'operator': 'EQUALS',
                    'values': [self.__class__.ad_group_id]
                }],
                'dateRange': {
                    'min': '20100101',
                    'max': '20100131'
                }
            }
        }
    }]
    report_definition = self.__class__.service.Mutate(operations)
    self.__class__.report_definition_id = report_definition[0]['id']
    self.assert_(isinstance(report_definition, tuple))

  def testDeleteReportDefinition(self):
    """Test wether we can delete report definition."""
    if self.__class__.report_definition_id == '0':
      self.testAddKeywordPerformanceReport()
    operations = [{
        'operator': 'REMOVE',
        'operand': {
            'id': self.__class__.report_definition_id
        }
    }]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportDefinitionServiceTestV201003))
  return suite


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportDefinitionServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(ReportDefinitionServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v201003 = makeTestSuiteV201003()
  suite_v201008 = makeTestSuiteV201008()
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v201003, suite_v201008, suite_v201101])
  unittest.main(defaultTest='alltests')
