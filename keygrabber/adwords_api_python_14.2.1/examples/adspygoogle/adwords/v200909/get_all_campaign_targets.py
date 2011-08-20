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

"""This example gets all campaign targets. To set campaign target, run
set_campaign_targets.py.

Tags: CampaignTargetService.get
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

# Construct selector and get all campaign targets.
selector = {}
campaign_targets = campaign_target_service.Get(selector)[0]

# Display results.
if 'entries' in campaign_targets:
  for campaign_target in campaign_targets['entries']:
    print ('Campaign target with id \'%s\' and of type \'%s\' was found.'
           % (campaign_target['campaignId'],
              campaign_target['TargetList_Type']))
else:
  print 'No campaign targets were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
