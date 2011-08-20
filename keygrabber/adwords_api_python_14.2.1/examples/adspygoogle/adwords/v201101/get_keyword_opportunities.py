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

"""This example gets all the keyword opportunities for the account.

Tags: BulkOpportunityService.get
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
bulk_opportunity_service = client.GetBulkOpportunityService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct selector and get all campaigns.
selector = {
    'ideaTypes': ['KEYWORD'],
    'requestedAttributeTypes': ['ADGROUP_ID', 'AVERAGE_MONTHLY_SEARCHES',
                                'CAMPAIGN_ID', 'IDEA_TYPE', 'KEYWORD'],
    'paging': {
        'startIndex': '0',
        'numberResults': '10'
    }
}
ret = bulk_opportunity_service.Get(selector)[0]

# Display results.
if 'entries' in ret and ret['entries']:
  for opportunity in ret['entries']:
    for idea in opportunity['opportunityIdeas']:
      data = Utils.GetDictFromMap(idea['data'])
      idea_type = data['IDEA_TYPE']['value']
      keyword_text = data['KEYWORD']['value']['text']
      campaign_id = data['CAMPAIGN_ID']['value']
      ad_group_id = data['ADGROUP_ID']['value']
      average_monthly_searches = data['AVERAGE_MONTHLY_SEARCHES']['value']

      print ('%s opportunity for Campaign %s and AdGroup %s: %s with %s '
             'average monthly searches\n' % (idea_type, campaign_id,
                                             ad_group_id, keyword_text,
                                             average_monthly_searches))
else:
  print 'No campaigns were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
