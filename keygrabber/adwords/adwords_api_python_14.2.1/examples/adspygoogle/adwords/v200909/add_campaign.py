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

"""This example adds a campaign. To get campaigns, run get_all_campaigns.py.

Tags: CampaignService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
campaign_service = client.GetCampaignService(
    'https://adwords-sandbox.google.com', 'v200909')

# Construct operations and add campaign.
operations = [{
    'operator': 'ADD',
    'operand': {
        'name': 'Interplanetary Cruise #%s' % Utils.GetUniqueName(),
        'status': 'PAUSED',
        'biddingStrategy': {
            'type': 'ManualCPC'
        },
        'endDate': '20110101',
        'budget': {
            'period': 'DAILY',
            'amount': {
                'microAmount': '50000000'
            },
            'deliveryMethod': 'STANDARD'
        }
    }
}]
campaigns = campaign_service.Mutate(operations)[0]

# Display results.
for campaign in campaigns['value']:
  print ('Campaign with name \'%s\' and id \'%s\' was added.'
         % (campaign['name'], campaign['id']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
