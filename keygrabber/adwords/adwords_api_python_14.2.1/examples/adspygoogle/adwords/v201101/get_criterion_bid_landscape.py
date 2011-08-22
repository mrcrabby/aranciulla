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

"""This example gets a bid landscape for an ad group and a criterion. To get ad
groups, run get_all_ad_groups.py. To get criteria, run
get_all_ad_group_criteria.py.

Tags: BidLandscapeService.getBidLandscape
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
data_service = client.GetDataService(
    'https://adwords-sandbox.google.com', 'v201101')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
criterion_id = 'INSERT_CRITERION_ID_HERE'

# Construct bid landscape selector object and retrieve bid landscape.
selector = {
    'fields': ['AdGroupId', 'CriterionId', 'StartDate', 'EndDate', 'Bid',
               'LocalClicks', 'LocalCost', 'MarginalCpc', 'LocalImpressions'],
    'predicates': [
        {
            'field': 'AdGroupId',
            'operator': 'EQUALS',
            'values': [ad_group_id]
        },
        {
            'field': 'CriterionId',
            'operator': 'EQUALS',
            'values': [criterion_id]
        }
    ]
}
bid_landscapes = data_service.GetCriterionBidLandscape(selector)[0]

# Display results.
if 'entries' in bid_landscapes:
  for bid_landscape in bid_landscapes['entries']:
    if bid_landscape['BidLandscape_Type'] == 'CriterionBidLandscape':
      print ('Criterion bid landscape with ad group id \'%s\', criterion id '
             '\'%s\', start date \'%s\', end date \'%s\', with landscape '
             'points was found:'
             % (bid_landscape['adGroupId'], bid_landscape['criterionId'],
                bid_landscape['startDate'], bid_landscape['endDate']))
      for bid_landscape_point in bid_landscape['landscapePoints']:
        print ('  bid: %s => clicks: %s, cost: %s, marginalCpc: %s, '
               'impressions: %s'
               % (bid_landscape_point['bid']['microAmount'],
                  bid_landscape_point['clicks'],
                  bid_landscape_point['cost']['microAmount'],
                  bid_landscape_point['marginalCpc']['microAmount'],
                  bid_landscape_point['impressions']))
else:
  print 'No bid landscapes found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
