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

"""Script to clear current client account in Sandbox of all its data.

The Sandbox is cleared by setting status of all campaigns to "Deleted".
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))

from adspygoogle.adwords.AdWordsClient import AdWordsClient


SERVER = 'https://adwords-sandbox.google.com'
VERSION = 'v200909'
client = AdWordsClient(path=os.path.join('..', '..'))
client.debug = False
client.use_mcc = False


selector = {
    'campaignStatuses': ['ACTIVE', 'PAUSED']
}
campaign_service = client.GetCampaignService(SERVER, VERSION)
campaigns = campaign_service.Get(selector)[0]

if 'entries' in campaigns:
  campaigns = campaigns['entries']
  operations = []
  for campaign in campaigns:
    print '%s: status=\'%s\'' % (campaign['name'], campaign['status']),
    operations.append({
        'operator': 'SET',
        'operand': {
            'id': campaign['id'],
            'status': 'DELETED'
        }
    })
    print '... marked for deletion'
  res = campaign_service.Mutate(operations)

  print
  print 'Total campaigns processed: %s' % len(campaigns)
else:
  print 'No campaigns to process.'
