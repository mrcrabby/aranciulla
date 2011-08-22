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

"""This example adds an ad group to a given campaign. To get ad groups, run
get_all_ad_groups.py.

Tags: AdGroupService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
ad_group_service = client.GetAdGroupService(
    'https://adwords-sandbox.google.com', 'v201101')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct operations and add an ad group.
operations = [{
    'operator': 'ADD',
    'operand': {
        'campaignId': campaign_id,
        'name': 'Earth to Mars Cruises #%s' % Utils.GetUniqueName(),
        'status': 'ENABLED',
        'bids': {
            'xsi_type': 'ManualCPCAdGroupBids',
            'keywordMaxCpc': {
                'amount': {
                    'microAmount': '10000000'
                }
            }
        }
    }
}]
ad_groups = ad_group_service.Mutate(operations)[0]

# Display results.
for ad_group in ad_groups['value']:
  print ('Ad group with name \'%s\' and id \'%s\' was added.'
         % (ad_group['name'], ad_group['id']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
