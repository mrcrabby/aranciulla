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

"""This example creates new negative campaign criterion. To create campaign, run
add_campaign.py.

Tags: CampaignCriterionService.mutate
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
campaign_criterion_service = client.GetCampaignCriterionService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct campaign criterion object and add negative campaign criterion.
campaign_id = 'INSERT_CAMPAIGN_ID_HERE'
operations = [{
    'operator': 'ADD',
    'operand': {
        'xsi_type': 'NegativeCampaignCriterion',
        'campaignId': campaign_id,
        'criterion': {
            'xsi_type': 'Keyword',
            'matchType': 'BROAD',
            'text': 'jupiter cruise'
        }
    }
}]
campaign_criterion = campaign_criterion_service.Mutate(
    operations)[0]['value'][0]

# Display results.
print ('New negative campaign criterion with \'%s\' id and \'%s\' text was '
       'successfully added to \'%s\' campaign.'
       % (campaign_criterion['criterion']['id'],
          campaign_criterion['criterion']['text'],
          campaign_criterion['campaignId']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
