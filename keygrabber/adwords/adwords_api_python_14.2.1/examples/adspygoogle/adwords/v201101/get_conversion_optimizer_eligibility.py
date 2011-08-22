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

"""This example shows how to check for conversion optimizer eligibility by
examining the conversionOptimizerEligibility field of the campaign.

Tags: CampaignService.get
Api: AdWordsOnly
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
campaign_service = client.GetCampaignService(
    'https://adwords-sandbox.google.com', 'v201101')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct selector and get campaigns.
selector = {
    'fields': ['Id', 'Name', 'Eligible', 'RejectionReasons'],
    'predicates': [{
        'field': 'CampaignId',
        'operator': 'EQUALS',
        'values': [campaign_id]
    }]
}
campaigns = campaign_service.Get(selector)[0]

# Display results.
if 'entries' in campaigns:
  for campaign in campaigns['entries']:
    if Utils.BoolTypeConvert(
        campaign['conversionOptimizerEligibility']['eligible']):
      print ('Campaign with id \'%s\' and name \'%s\' is eligible to use '
             'conversion optimizer.' % (campaign['id'], campaign['name']))
    else:
      print ('Campaign with id \'%s\' and name \'%s\' is not eligible to use '
             'conversion optimizer for the reasons: %s.'
             % (campaign['id'], campaign['name'],
                campaign['conversionOptimizerEligibility']['rejectionReasons']))
else:
  print 'No campaigns were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
