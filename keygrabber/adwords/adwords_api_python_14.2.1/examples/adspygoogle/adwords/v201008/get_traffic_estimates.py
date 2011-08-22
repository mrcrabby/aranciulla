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

"""This example retrieves keyword traffic estimates.

Tags: TrafficEstimatorService.get
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
traffic_estimator_service = client.GetTrafficEstimatorService(
    'https://adwords-sandbox.google.com', 'v201008')

# Construct selector object and retrieve traffic estimates.
keywords = [
    {'text': 'mars cruise', 'matchType': 'BROAD'},
    {'text': 'cheap cruise', 'matchType': 'PHRASE'},
    {'text': 'cruise', 'matchType': 'EXACT'}
]
selector = {
    'campaignEstimateRequests': [{
        'adGroupEstimateRequests': [{
            'keywordEstimateRequests': [
                {
                    'keyword': {
                        'xsi_type': 'Keyword',
                        'matchType': keywords[0]['matchType'],
                        'text': keywords[0]['text']
                    }
                },
                {
                    'keyword': {
                        'xsi_type': 'Keyword',
                        'matchType': keywords[1]['matchType'],
                        'text': keywords[1]['text']
                    }
                },
                {
                    'keyword': {
                        'xsi_type': 'Keyword',
                        'matchType': keywords[2]['matchType'],
                        'text': keywords[2]['text']
                    }
                }
            ],
            'maxCpc': {
                'xsi_type': 'Money',
                'microAmount': '1000000'
            }
        }],
        'targets': [
            {
                'xsi_type': 'CountryTarget',
                'countryCode': 'US'
            },
            {
                'xsi_type': 'LanguageTarget',
                'languageCode': 'en'
            }
        ]
    }]
}
estimates = traffic_estimator_service.Get(selector)[0]

# Display results.
if estimates:
  ad_group_estimate = estimates['campaignEstimates'][0]['adGroupEstimates'][0]
  keyword_estimates = ad_group_estimate['keywordEstimates']
  for index in xrange(len(keyword_estimates)):
    keyword = keywords[index]
    estimate = keyword_estimates[index]

    # Find the mean of the min and max values.
    mean_avg_cpc = (long(estimate['max']['averageCpc']['microAmount']) +
                    long(estimate['max']['averageCpc']['microAmount'])) / 2
    mean_avg_pos = (float(estimate['min']['averagePosition']) +
                    float(estimate['max']['averagePosition'])) / 2
    mean_clicks = (long(estimate['min']['clicks']) +
                   long(estimate['max']['clicks'])) / 2
    mean_total_cost = (long(estimate['min']['totalCost']['microAmount']) +
                       long(estimate['max']['totalCost']['microAmount'])) / 2

    print ('Results for the keyword with text \'%s\' and match type \'%s\':'
           % (keyword['text'], keyword['matchType']))
    print '  Estimated average CPC: %s' % mean_avg_cpc
    print '  Estimated ad position: %s' % mean_avg_pos
    print '  Estimated daily clicks: %s' % mean_clicks
    print '  Estimated daily cost: %s' % mean_total_cost
else:
  print 'No traffic estimates were returned.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
