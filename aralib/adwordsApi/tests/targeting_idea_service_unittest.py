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

"""Unit tests to cover TargetingIdeaService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('..')
import unittest

from aw_api import Utils
from aw_api.Errors import RequestError
from tests import HTTP_PROXY
from tests import SERVER_V200909
from tests import SERVER_V201003
from tests import VERSION_V200909
from tests import VERSION_V201003
from tests import client


class TargetingIdeaServiceTestV200909(unittest.TestCase):

  """Unittest suite for TargetingIdeaService using v200909."""

  SERVER = SERVER_V200909
  VERSION = VERSION_V200909
  TRIGGER_MSG = ('TargetingIdeaError.INSUFFICIENT_SEARCH_PARAMETERS @ '
                 'selector.selector.searchParameters')
  client.debug = False
  service = None
  ad_group_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetTargetingIdeaService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_group_id == '0':
      operations = [{
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
      }]
      campaign_id = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY).Mutate(
              operations)[0]['value'][0]['id']
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
      self.__class__.ad_group_id = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY).Mutate(
              operations)[0]['value'][0]['id']

  def testGetEmptySelector(self):
    """Test whether we can catch required search parameter error in selector."""
    selector = {}
    try:
      self.__class__.service.Get(selector)
    except RequestError, e:
      self.failUnless(e.message.find(self.__class__.TRIGGER_MSG) > -1)
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAdTypeSearchParameter(self):
    """Test whether we can request ad type search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'AdTypeSearchParameter',
                'adTypes': ['DISPLAY']
            },
            {
                'type': 'RelatedToUrlSearchParameter',
                'urls': ['http://news.google.com']
            }
         ],
        'ideaType': 'PLACEMENT',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAverageTargetedMonthlySearchesSearchParameter(self):
    """Test whether we can request average targeted monthly search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'AverageTargetedMonthlySearchesSearchParameter',
                'operation': {
                    'minimum': '1',
                    'maximum': '50'
                }
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'flower shop',
                    'matchType': 'BROAD'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCompetitionSearchParameter(self):
    """Test whether we can request competition search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'CompetitionSearchParameter',
                'levels': ['MEDIUM', 'HIGH']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'cash for clunkers',
                    'matchType': 'BROAD'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCountryTargetSearchParameter(self):
    """Test whether we can request country target search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'CountryTargetSearchParameter',
                'countryTargets': [
                    {'countryCode': 'US'},
                    {'countryCode': 'CN'},
                    {'countryCode': 'JP'}
                ]
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'global economy',
                    'matchType': 'BROAD'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetExcludedKeywordSearchParameter(self):
    """Test whether we can request excluded keyword search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'ExcludedKeywordSearchParameter',
                'keywords': [{
                    'text': 'media player',
                    'matchType': 'EXACT'
                }]
            },
            {
                'type': 'KeywordMatchTypeSearchParameter',
                'keywordMatchTypes': ['BROAD', 'EXACT']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'dvd player',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGlobalMonthlySearchesSearchParameter(self):
    """Test whether we can request global monthly search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'GlobalMonthlySearchesSearchParameter',
                'operation': {
                    'minimum': '1000',
                    'maximum': '10000'
                }
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'dvd player',
                    'matchType': 'EXACT'
                }],
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetIncludeAdultContentSearchParameter(self):
    """Test whether we can request include adult content search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'IncludeAdultContentSearchParameter'
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'books',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetKeywordCategoryIdSearchParameter(self):
    """Test whether we can request keyword category id search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'KeywordCategoryIdSearchParameter',
                'categoryId': '5'
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'rent video',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetKeywordMatchTypeSearchParameter(self):
    """Test whether we can request keyword match type search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'KeywordMatchTypeSearchParameter',
                'keywordMatchTypes': ['BROAD', 'EXACT']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'cars',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetLanguageTargetSearchParameter(self):
    """Test whether we can request language target search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'LanguageTargetSearchParameter',
                'languageTargets': [
                    {'languageCode': 'zh_CN'},
                    {'languageCode': 'ja'}
                ]
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'global economy',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetMobileSearchParameter(self):
    """Test whether we can request mobile search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'MobileSearchParameter'
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'movie theater',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetNgramGroupsSearchParameter(self):
    """Test whether we can request ngram groups search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'NgramGroupsSearchParameter',
                'ngramGroups': ['27']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'presidential vote',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetPlacementTypeSearchParameter(self):
    """Test whether we can request placement type search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'PlacementTypeSearchParameter',
                'placementTypes': ['VIDEO', 'GAME']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'iron man',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'PLACEMENT',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetRelatedToKeywordSearchParameter(self):
    """Test whether we can request related to keyword search parameter."""
    selector = {
        'searchParameters': [{
            'type': 'RelatedToKeywordSearchParameter',
            'keywords': [{
                'text': 'flowers',
                'matchType': 'EXACT'
            }]
        }],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetRelatedToKeywordSearchParameterAllPages(self):
    """Test whether we can request related to keyword search parameter and
    retrieve complete set of resulting pages."""
    index = 0
    selector = {
        'searchParameters': [{
            'type': 'RelatedToKeywordSearchParameter',
            'keywords': [{
                'text': 'flowers',
                'matchType': 'BROAD'
            }]
        }],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': str(index),
            'numberResults': '100'
        }
    }
    results = []
    while True:
      page = self.__class__.service.Get(selector)[0]
      self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())
      if 'entries' in page:
        results.extend(page['entries'])
      if int(page['totalNumEntries']) <= index:
        break
      index += 100
      selector = {
          'searchParameters': [{
              'type': 'RelatedToKeywordSearchParameter',
              'keywords': [{
                  'text': 'flowers',
                  'matchType': 'BROAD'
              }]
          }],
          'ideaType': 'KEYWORD',
          'requestType': 'IDEAS',
          'paging': {
              'startIndex': str(index),
              'numberResults': '100'
          }
      }
    self.assert_(isinstance(results, list))
    self.assertEqual(str(len(results)), page['totalNumEntries'])
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetRelatedToUrlSearchParameter(self):
    """Test whether we can request related to url search parameter."""
    selector = {
        'searchParameters': [{
            'type': 'RelatedToUrlSearchParameter',
            'urls': ['http://finance.google.com'],
            'includeSubUrls': 'false'
        }],
        'ideaType': 'PLACEMENT',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetSeedAdGroupIdSearchParameter(self):
    """Test whether we can request seed ad group id search parameter."""
    selector = {
        'searchParameters': [{
            'type': 'SeedAdGroupIdSearchParameter',
            'adGroupId': self.__class__.ad_group_id
        }],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetBulkKeywordIdeas(self):
    """Test whether we can request bulk keyword ideas."""
    selector = {
        'searchParameters': [
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [
                    {
                        'text': 'presidential vote',
                        'matchType': 'EXACT'
                    }
                ]
            },
            {
                'type': 'RelatedToUrlSearchParameter',
                'urls': ['http://finance.google.com'],
                'includeSubUrls': 'false'
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(
        self.__class__.service.GetBulkKeywordIdeas(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


class TargetingIdeaServiceTestV201003(unittest.TestCase):

  """Unittest suite for TargetingIdeaService using v201003."""

  SERVER = SERVER_V201003
  VERSION = VERSION_V201003
  TRIGGER_MSG = ('TargetingIdeaError.INSUFFICIENT_SEARCH_PARAMETERS @ '
                 'selector.selector.searchParameters')
  client.debug = False
  service = None
  ad_group_id = '0'

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetTargetingIdeaService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

    if self.__class__.ad_group_id == '0':
      operations = [{
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
      }]
      campaign_id = client.GetCampaignService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY).Mutate(
              operations)[0]['value'][0]['id']
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
      self.__class__.ad_group_id = client.GetAdGroupService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY).Mutate(
              operations)[0]['value'][0]['id']

  def testGetEmptySelector(self):
    """Test whether we can catch required search parameter error in selector."""
    selector = {}
    try:
      self.__class__.service.Get(selector)
    except RequestError, e:
      self.failUnless(e.message.find(self.__class__.TRIGGER_MSG) > -1)
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAdTypeSearchParameter(self):
    """Test whether we can request ad type search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'AdTypeSearchParameter',
                'adTypes': ['DISPLAY']
            },
            {
                'type': 'RelatedToUrlSearchParameter',
                'urls': ['http://news.google.com']
            }
         ],
        'ideaType': 'PLACEMENT',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetAverageTargetedMonthlySearchesSearchParameter(self):
    """Test whether we can request average targeted monthly search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'AverageTargetedMonthlySearchesSearchParameter',
                'operation': {
                    'minimum': '1',
                    'maximum': '50'
                }
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'flower shop',
                    'matchType': 'BROAD'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCompetitionSearchParameter(self):
    """Test whether we can request competition search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'CompetitionSearchParameter',
                'levels': ['MEDIUM', 'HIGH']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'cash for clunkers',
                    'matchType': 'BROAD'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetCountryTargetSearchParameter(self):
    """Test whether we can request country target search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'CountryTargetSearchParameter',
                'countryTargets': [
                    {'countryCode': 'US'},
                    {'countryCode': 'CN'},
                    {'countryCode': 'JP'}
                ]
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'global economy',
                    'matchType': 'BROAD'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetExcludedKeywordSearchParameter(self):
    """Test whether we can request excluded keyword search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'ExcludedKeywordSearchParameter',
                'keywords': [{
                    'text': 'media player',
                    'matchType': 'EXACT'
                }]
            },
            {
                'type': 'KeywordMatchTypeSearchParameter',
                'keywordMatchTypes': ['BROAD', 'EXACT']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'dvd player',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGlobalMonthlySearchesSearchParameter(self):
    """Test whether we can request global monthly search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'GlobalMonthlySearchesSearchParameter',
                'operation': {
                    'minimum': '1000',
                    'maximum': '10000'
                }
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'dvd player',
                    'matchType': 'EXACT'
                }],
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetIncludeAdultContentSearchParameter(self):
    """Test whether we can request include adult content search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'IncludeAdultContentSearchParameter'
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'books',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetKeywordCategoryIdSearchParameter(self):
    """Test whether we can request keyword category id search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'KeywordCategoryIdSearchParameter',
                'categoryId': '5'
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'rent video',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetKeywordMatchTypeSearchParameter(self):
    """Test whether we can request keyword match type search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'KeywordMatchTypeSearchParameter',
                'keywordMatchTypes': ['BROAD', 'EXACT']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'cars',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetLanguageTargetSearchParameter(self):
    """Test whether we can request language target search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'LanguageTargetSearchParameter',
                'languageTargets': [
                    {'languageCode': 'zh_CN'},
                    {'languageCode': 'ja'}
                ]
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'global economy',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetMobileSearchParameter(self):
    """Test whether we can request mobile search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'MobileSearchParameter'
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'movie theater',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetPlacementTypeSearchParameter(self):
    """Test whether we can request placement type search parameter."""
    selector = {
        'searchParameters': [
            {
                'type': 'PlacementTypeSearchParameter',
                'placementTypes': ['VIDEO', 'GAME']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'iron man',
                    'matchType': 'EXACT'
                }]
            }
        ],
        'ideaType': 'PLACEMENT',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetRelatedToKeywordSearchParameter(self):
    """Test whether we can request related to keyword search parameter."""
    selector = {
        'searchParameters': [{
            'type': 'RelatedToKeywordSearchParameter',
            'keywords': [{
                'text': 'flowers',
                'matchType': 'EXACT'
            }]
        }],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetRelatedToKeywordSearchParameterAllPages(self):
    """Test whether we can request related to keyword search parameter and
    retrieve complete set of resulting pages."""
    index = 0
    selector = {
        'searchParameters': [{
            'type': 'RelatedToKeywordSearchParameter',
            'keywords': [{
                'text': 'flowers',
                'matchType': 'BROAD'
            }]
        }],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': str(index),
            'numberResults': '100'
        }
    }
    results = []
    while True:
      page = self.__class__.service.Get(selector)[0]
      self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())
      if 'entries' in page:
        results.extend(page['entries'])
      if int(page['totalNumEntries']) <= index:
        break
      index += 100
      selector = {
          'searchParameters': [{
              'type': 'RelatedToKeywordSearchParameter',
              'keywords': [{
                  'text': 'flowers',
                  'matchType': 'BROAD'
              }]
          }],
          'ideaType': 'KEYWORD',
          'requestType': 'IDEAS',
          'paging': {
              'startIndex': str(index),
              'numberResults': '100'
          }
      }
    self.assert_(isinstance(results, list))
    self.assertEqual(str(len(results)), page['totalNumEntries'])
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetRelatedToUrlSearchParameter(self):
    """Test whether we can request related to url search parameter."""
    selector = {
        'searchParameters': [{
            'type': 'RelatedToUrlSearchParameter',
            'urls': ['http://finance.google.com'],
            'includeSubUrls': 'false'
        }],
        'ideaType': 'PLACEMENT',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetSeedAdGroupIdSearchParameter(self):
    """Test whether we can request seed ad group id search parameter."""
    selector = {
        'searchParameters': [{
            'type': 'SeedAdGroupIdSearchParameter',
            'adGroupId': self.__class__.ad_group_id
        }],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetBulkKeywordIdeas(self):
    """Test whether we can request bulk keyword ideas."""
    selector = {
        'searchParameters': [
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [
                    {
                        'text': 'presidential vote',
                        'matchType': 'EXACT'
                    }
                ]
            },
            {
                'type': 'RelatedToUrlSearchParameter',
                'urls': ['http://finance.google.com'],
                'includeSubUrls': 'false'
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(
        self.__class__.service.GetBulkKeywordIdeas(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())

  def testGetIdeaTextMatchesSearchParameter(self):
    """Test whether we can request idea text matches."""
    selector = {
        'searchParameters': [
            {
                'type': 'IdeaTextMatchesSearchParameter',
                'included': ['red flowers']
            },
            {
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': 'flowers',
                    'matchType': 'BROAD'
                }]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'paging': {
            'startIndex': '0',
            'numberResults': '1'
        }
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))
    self.assertEqual(
        Utils.GetMethodCost(self.__class__.VERSION,
                            self.__class__.service.__class__.__name__,
                            'get',
                            client.GetLastOperations(),
                            True),
        client.GetLastUnits())


def makeTestSuiteV200909():
  """Set up test suite using v200909.

  Returns:
    TestSuite test suite using v200909.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TargetingIdeaServiceTestV200909))
  return suite


def makeTestSuiteV201003():
  """Set up test suite using v201003.

  Returns:
    TestSuite test suite using v201003.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TargetingIdeaServiceTestV201003))
  return suite


if __name__ == '__main__':
  suite_v200909 = makeTestSuiteV200909()
  suite_v201003 = makeTestSuiteV201003()
  alltests = unittest.TestSuite([suite_v200909, suite_v201003])
  unittest.main(defaultTest='alltests')
