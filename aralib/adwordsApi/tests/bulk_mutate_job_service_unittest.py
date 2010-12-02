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

"""Unit tests to cover BulkMutateJobService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from tests import HTTP_PROXY
from tests import SERVER_V200909
from tests import SERVER_V201003
from tests import VERSION_V200909
from tests import VERSION_V201003
from tests import client


class BulkMutateJobServiceTestV200909(unittest.TestCase):

  """Unittest suite for BulkMutateJobService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  client.debug = False
  service = None
  campaign_id = '0'
  ad_group_id1 = '0'
  ad_group_id2 = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetBulkMutateJobService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign_id == '0':
      operations = [
          {
              'operator': 'ADD',
              'operand': {
                  'name': 'Campaign #%s' % Utils.GetUniqueName(),
                  'status': 'PAUSED',
                  'biddingStrategy': {
                      'type': 'ManualCPC'
                  },
                  'endDate': '20110101',
                  'budget': {
                      'period': 'DAILY',
                      'amount': {
                          'microAmount': '1000000'
                      },
                      'deliveryMethod': 'STANDARD'
                  }
              }
          }
      ]
      service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      self.__class__.campaign_id = \
          service.Mutate(operations)[0]['value'][0]['id']

    if (self.__class__.ad_group_id1 == '0' or
        self.__class__.ad_group_id2 == '0'):
      operations = [
          {
              'operator': 'ADD',
              'operand': {
                  'campaignId': self.__class__.campaign_id,
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
          },
          {
              'operator': 'ADD',
              'operand': {
                  'campaignId': self.__class__.campaign_id,
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
          }
      ]
      service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      ad_groups = service.Mutate(operations)[0]['value']
      self.__class__.ad_group_id1 = ad_groups[0]['id']
      self.__class__.ad_group_id2 = ad_groups[1]['id']

  def testGetAllJobs(self):
    """Test whether we can fetch all jobs currently in the queue."""
    selector = {}
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAllCompletedJobs(self):
    """Test whether we can fetch all COMPLETED jobs."""
    selector = {
        'jobStatuses': ['COMPLETED']
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testSinglePartSingleStreamMultipleOperations(self):
    """Test whether we can set campaign targets using single part job with
    single stream and multiple operations."""
    stream = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': [
            {
                'type': 'CampaignTarget',
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
            },
            {
                'type': 'CampaignTarget',
                'operator': 'SET',
                'operand': {
                    'type': 'NetworkTargetList',
                    'campaignId': self.__class__.campaign_id,
                    'targets': [{
                        'type': 'NetworkTarget',
                        'networkCoverageType': 'CONTENT_NETWORK'
                    }]
                }
            },
            {
                'type': 'CampaignTarget',
                'operator': 'SET',
                'operand': {
                    'type': 'LanguageTargetList',
                    'campaignId': self.__class__.campaign_id,
                    'targets': [{
                        'type': 'LanguageTarget',
                        'languageCode': 'en'
                    }]
                }
            }
        ]
    }
    part = {
        'partIndex': '0',
        'operationStreams': [stream]
    }
    operation = {
        'operator': 'ADD',
        'operand': {
            'type': 'BulkMutateJob',
            'request': part,
            'numRequestParts': '1'
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))
    result = self.__class__.service.DownloadBulkJob(job[0]['id'])
    self.assert_(isinstance(result, list))

  def testSinglePartMultipleStreamsSingleOperation(self):
    """Test whether we can add ads using single part job with multiple
    streams."""
    stream1 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': [
            {
                'type': 'AdGroupAd',
                'operator': 'ADD',
                'operand': {
                    'type': 'AdGroupAd',
                    'adGroupId': self.__class__.ad_group_id1,
                    'ad': {
                        'type': 'TextAd',
                        'url': 'http://www.example.com',
                        'displayUrl': 'example.com',
                        'status': 'ENABLED',
                        'description1': 'Visit the Red Planet in style.',
                        'description2': 'Low-gravity fun for everyone!',
                        'headline': 'Luxury Cruise to Mars'

                    }
                }
            }
        ]
    }
    stream2 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': [
            {
                'type': 'AdGroupAd',
                'operator': 'ADD',
                'operand': {
                    'type': 'AdGroupAd',
                    'adGroupId': self.__class__.ad_group_id2,
                    'ad': {
                        'type': 'TextAd',
                        'url': 'http://www.example.com',
                        'displayUrl': 'example.com',
                        'status': 'ENABLED',
                        'description1': 'Visit the Red Planet in style.',
                        'description2': 'Low-gravity fun for everyone!',
                        'headline': 'Luxury Cruise to Mars is here now!!!'

                    }
                }
            }
        ]
    }
    part = {
        'partIndex': '0',
        'operationStreams': [stream1, stream2]
    }
    operation = {
        'operator': 'ADD',
        'operand': {
            'type': 'BulkMutateJob',
            'request': part,
            'numRequestParts': '1'
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))

    result = self.__class__.service.DownloadBulkJob(job[0]['id'])
    self.assert_(isinstance(result, list))

  def testMultiplePartsMultipleStreamsSingleOperation(self):
    """Test whether we can add ads and keywords using multiple part job with
    multiple streams."""
    ad_stream1 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': [
            {
                'type': 'AdGroupAd',
                'operator': 'ADD',
                'operand': {
                    'type': 'AdGroupAd',
                    'adGroupId': self.__class__.ad_group_id1,
                    'ad': {
                        'type': 'TextAd',
                        'url': 'http://www.example.com',
                        'displayUrl': 'example.com',
                        'status': 'ENABLED',
                        'description1': 'Visit the Red Planet in style.',
                        'description2': 'Low-gravity fun for everyone!',
                        'headline': 'Luxury Cruise to Mars'

                    }
                }
            }
        ]
    }
    ad_stream2 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': [
            {
                'type': 'AdGroupAd',
                'operator': 'ADD',
                'operand': {
                    'type': 'AdGroupAd',
                    'adGroupId': self.__class__.ad_group_id2,
                    'ad': {
                        'type': 'TextAd',
                        'url': 'http://www.example.com',
                        'displayUrl': 'example.com',
                        'status': 'ENABLED',
                        'description1': 'Visit the Red Planet in style.',
                        'description2': 'Low-gravity fun for everyone!',
                        'headline': 'Luxury Cruise to Mars is here now!!!'

                    }
                }
            }
        ]
    }
    part1 = {
        'partIndex': '0',
        'operationStreams': [ad_stream1, ad_stream2]
    }
    operation = {
        'operator': 'ADD',
        'operand': {
            'type': 'BulkMutateJob',
            'request': part1,
            'numRequestParts': '2'
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))

    kw_stream1 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': [
            {
                'type': 'AdGroupCriterion',
                'operator': 'ADD',
                'operand': {
                    'type': 'BiddableAdGroupCriterion',
                    'adGroupId': self.__class__.ad_group_id1,
                    'criterion': {
                        'type': 'Keyword',
                        'matchType': 'BROAD',
                        'text': 'mars cruise'
                    }
                }
            }
        ]
    }
    kw_stream2 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': [
            {
                'type': 'AdGroupCriterion',
                'operator': 'ADD',
                'operand': {
                    'type': 'BiddableAdGroupCriterion',
                    'adGroupId': self.__class__.ad_group_id2,
                    'criterion': {
                        'type': 'Keyword',
                        'matchType': 'BROAD',
                        'text': 'mars cruise'
                    }
                }
            }
        ]
    }
    part2 = {
        'partIndex': '1',
        'operationStreams': [kw_stream1, kw_stream2]
    }
    operation = {
        'operator': 'SET',
        'operand': {
            'type': 'BulkMutateJob',
            'id': job[0]['id'],
            'request': part2
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))

    result = self.__class__.service.DownloadBulkJob(job[0]['id'])
    self.assert_(isinstance(result, list))


class BulkMutateJobServiceTestV201003(unittest.TestCase):

  """Unittest suite for BulkMutateJobService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  client.debug = False
  service = None
  campaign_id = '0'
  ad_group_id1 = '0'
  ad_group_id2 = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetBulkMutateJobService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.campaign_id == '0':
      operations = [
          {
              'operator': 'ADD',
              'operand': {
                  'name': 'Campaign #%s' % Utils.GetUniqueName(),
                  'status': 'PAUSED',
                  'biddingStrategy': {
                      'type': 'ManualCPC'
                  },
                  'endDate': '20110101',
                  'budget': {
                      'period': 'DAILY',
                      'amount': {
                          'microAmount': '1000000'
                      },
                      'deliveryMethod': 'STANDARD'
                  }
              }
          }
      ]
      service = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      self.__class__.campaign_id = \
          service.Mutate(operations)[0]['value'][0]['id']

    if (self.__class__.ad_group_id1 == '0' or
        self.__class__.ad_group_id2 == '0'):
      operations = [
          {
              'operator': 'ADD',
              'operand': {
                  'campaignId': self.__class__.campaign_id,
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
          },
          {
              'operator': 'ADD',
              'operand': {
                  'campaignId': self.__class__.campaign_id,
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
          }
      ]
      service = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)
      ad_groups = service.Mutate(operations)[0]['value']
      self.__class__.ad_group_id1 = ad_groups[0]['id']
      self.__class__.ad_group_id2 = ad_groups[1]['id']

  def testGetAllJobs(self):
    """Test whether we can fetch all jobs currently in the queue."""
    selector = {}
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAllCompletedJobs(self):
    """Test whether we can fetch all COMPLETED jobs."""
    selector = {
        'jobStatuses': ['COMPLETED']
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testSinglePartSingleStream(self):
    """Test whether we can set campaign geo targets using single part job with
    single stream."""
    ops = []
    for city in Utils.GetUsCities()[:100]:
      ops.append(
          {
                'type': 'CampaignTarget',
                'operator': 'SET',
                'operand': {
                    'type': 'GeoTargetList',
                    'campaignId': self.__class__.campaign_id,
                    'targets': [{
                        'type': 'CityTarget',
                        'cityName': city[1].split(',')[0],
                        'countryCode': 'US'
                    }]
                }
            }
      )
    stream = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': ops
    }
    part = {
        'partIndex': '0',
        'operationStreams': [stream]
    }
    operation = {
        'operator': 'ADD',
        'operand': {
            'type': 'BulkMutateJob',
            'request': part,
            'numRequestParts': '1'
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))
    result = self.__class__.service.DownloadBulkJob(job[0]['id'])
    self.assert_(isinstance(result, list))

  def testSinglePartMultipleStreams(self):
    """Test whether we can add ads using single part job with multiple
    streams."""
    stream1_ops = []
    for index in xrange(50):
      stream1_ops.append(
          {
              'type': 'AdGroupAd',
              'operator': 'ADD',
              'operand': {
                  'type': 'AdGroupAd',
                  'adGroupId': self.__class__.ad_group_id1,
                  'ad': {
                      'type': 'TextAd',
                      'url': 'http://www.example.com',
                      'displayUrl': 'example.com',
                      'status': 'ENABLED',
                      'description1': 'Visit the Red Planet in style.',
                      'description2': 'Low-gravity fun for everyone!',
                      'headline': 'Luxury Cruise to Mars'

                  }
              }
            })
    stream1 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': stream1_ops
    }

    stream2_ops = []
    for index in xrange(50):
      stream2_ops.append(
          {
              'type': 'AdGroupAd',
              'operator': 'ADD',
              'operand': {
                  'type': 'AdGroupAd',
                  'adGroupId': self.__class__.ad_group_id2,
                  'ad': {
                      'type': 'TextAd',
                      'url': 'http://www.example.com',
                      'displayUrl': 'example.com',
                      'status': 'ENABLED',
                      'description1': 'Visit the Red Planet in style.',
                      'description2': 'Low-gravity fun for everyone!',
                      'headline': 'Luxury Cruise to Mars is here now!!!'

                  }
              }
          })
    stream2 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': stream2_ops
    }
    part = {
        'partIndex': '0',
        'operationStreams': [stream1, stream2]
    }
    operation = {
        'operator': 'ADD',
        'operand': {
            'type': 'BulkMutateJob',
            'request': part,
            'numRequestParts': '1'
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))

    result = self.__class__.service.DownloadBulkJob(job[0]['id'])
    self.assert_(isinstance(result, list))

  def testMultiplePartsMultipleStreams(self):
    """Test whether we can add ads and keywords using multiple part job with
    multiple streams."""
    ad_stream1_ops = []
    for index in xrange(25):
      ad_stream1_ops.append(
          {
              'type': 'AdGroupAd',
              'operator': 'ADD',
              'operand': {
                  'type': 'AdGroupAd',
                  'adGroupId': self.__class__.ad_group_id1,
                  'ad': {
                      'type': 'TextAd',
                      'url': 'http://www.example.com',
                      'displayUrl': 'example.com',
                      'status': 'ENABLED',
                      'description1': 'Visit the Red Planet in style.',
                      'description2': 'Low-gravity fun for everyone!',
                      'headline': 'Luxury Cruise to Mars'

                  }
              }
          })
    ad_stream1 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': ad_stream1_ops
    }

    ad_stream2_ops = []
    for index in xrange(25):
      ad_stream2_ops.append(
          {
              'type': 'AdGroupAd',
              'operator': 'ADD',
              'operand': {
                  'type': 'AdGroupAd',
                  'adGroupId': self.__class__.ad_group_id2,
                  'ad': {
                      'type': 'TextAd',
                      'url': 'http://www.example.com',
                      'displayUrl': 'example.com',
                      'status': 'ENABLED',
                      'description1': 'Visit the Red Planet in style.',
                      'description2': 'Low-gravity fun for everyone!',
                      'headline': 'Luxury Cruise to Mars is here now!!!'

                  }
              }
          })
    ad_stream2 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': ad_stream2_ops
    }
    part1 = {
        'partIndex': '0',
        'operationStreams': [ad_stream1, ad_stream2]
    }
    operation = {
        'operator': 'ADD',
        'operand': {
            'type': 'BulkMutateJob',
            'request': part1,
            'numRequestParts': '2'
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))

    kw_stream1_ops = []
    for index in xrange(25):
      kw_stream1_ops.append(
          {
              'type': 'AdGroupCriterion',
              'operator': 'ADD',
              'operand': {
                  'type': 'BiddableAdGroupCriterion',
                  'adGroupId': self.__class__.ad_group_id1,
                  'criterion': {
                      'type': 'Keyword',
                      'matchType': 'BROAD',
                      'text': 'mars cruise'
                  }
              }
          })
    kw_stream1 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': kw_stream1_ops
    }

    kw_stream2_ops = []
    for index in xrange(25):
      kw_stream2_ops.append(
          {
              'type': 'AdGroupCriterion',
              'operator': 'ADD',
              'operand': {
                  'type': 'BiddableAdGroupCriterion',
                  'adGroupId': self.__class__.ad_group_id2,
                  'criterion': {
                      'type': 'Keyword',
                      'matchType': 'BROAD',
                      'text': 'mars cruise'
                  }
              }
          })
    kw_stream2 = {
        'scopingEntityId': {
            'type': 'CAMPAIGN_ID',
            'value': self.__class__.campaign_id,
        },
        'operations': kw_stream2_ops
    }
    part2 = {
        'partIndex': '1',
        'operationStreams': [kw_stream1, kw_stream2]
    }
    operation = {
        'operator': 'SET',
        'operand': {
            'type': 'BulkMutateJob',
            'id': job[0]['id'],
            'request': part2
        }
    }
    job = self.__class__.service.Mutate(operation)
    self.assert_(isinstance(job, tuple))

    result = self.__class__.service.DownloadBulkJob(job[0]['id'])
    self.assert_(isinstance(result, list))


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(BulkMutateJobServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(BulkMutateJobServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
