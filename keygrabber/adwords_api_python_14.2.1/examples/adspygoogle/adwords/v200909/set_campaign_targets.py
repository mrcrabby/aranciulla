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

"""This example adds geo, language, and network targets to a given campaign. To
get campaigns, run get_all_campaigns.py.

Tags: CampaignTargetService.mutate
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
campaign_target_service = client.GetCampaignTargetService(
    'https://adwords-sandbox.google.com', 'v200909')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct operations and set campaign targets.
operations = [
    {
        'operator': 'SET',
        'operand': {
            'type': 'GeoTargetList',
            'campaignId': campaign_id,
            'targets': [
                {
                    'type': 'CountryTarget',
                    'countryCode': 'US'
                },
                {
                    'type': 'CountryTarget',
                    'countryCode': 'JP'
                }
            ]
        }
    },
    {
        'operator': 'SET',
        'operand': {
            'type': 'LanguageTargetList',
            'campaignId': campaign_id,
            'targets': [
                {
                    'type': 'LanguageTarget',
                    'languageCode': 'fr'
                },
                {
                    'type': 'LanguageTarget',
                    'languageCode': 'ja'
                }
            ]
        }
    },
    {
        'operator': 'SET',
        'operand': {
            'type': 'NetworkTargetList',
            'campaignId': campaign_id,
            'targets': [{
                'type': 'NetworkTarget',
                'networkCoverageType': 'GOOGLE_SEARCH'
            },
            {
                'type': 'NetworkTarget',
                'networkCoverageType': 'SEARCH_NETWORK'
            }]
        }
    }
]
campaign_targets = campaign_target_service.Mutate(operations)[0]

# Display results.
for campaign_target in campaign_targets['value']:
  print ('Campaign target with id \'%s\' and of type \'%s\' was set.'
         % (campaign_target['campaignId'], campaign_target['TargetList_Type']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
