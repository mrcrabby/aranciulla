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

"""This example gets the changes in the account during the last 24 hours.

Tags: CustomerSyncService.get
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import datetime
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
customer_sync_service = client.GetCustomerSyncService(
    'https://adwords-sandbox.google.com', 'v201101')
campaign_service = client.GetCampaignService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct selector and get all campaigns.
selector = {
    'fields': ['Id', 'Name', 'Status']
}
campaigns = campaign_service.Get(selector)[0]
campaign_ids = []
if 'entries' in campaigns:
  for campaign in campaigns['entries']:
    campaign_ids.append(campaign['id'])
else:
  print 'No campaigns were found.'
  sys.exit(0)

# Construct selector and get all changes.
today = datetime.datetime.today()
yesterday = today - datetime.timedelta(1)
selector = {
    'dateTimeRange': {
        'min': yesterday.strftime('%Y%m%d %H%M%S'),
        'max': today.strftime('%Y%m%d %H%M%S')
    },
    'campaignIds': campaign_ids
}
account_changes = customer_sync_service.Get(selector)[0]

# Display results.
if account_changes:
  print 'Most recent changes: %s' % account_changes['lastChangeTimestamp']
  if account_changes['changedCampaigns']:
    for data in account_changes['changedCampaigns']:
      print ('Campaign with id \'%s\' has change status \'%s\'.'
             % (data['campaignId'], data['campaignChangeStatus']))
      if (data['campaignChangeStatus'] != 'NEW' and data['campaignChangeStatus']
          != 'FIELDS_UNCHANGED'):
        print '  Added ad extensions: %s' % data['addedAdExtensions']
        print '  Deleted ad extensions: %s' % data['deletedAdExtensions']
        print '  Added campaign criteria: %s' % data['addedCampaignCriteria']
        print ('  Deleted campaign criteria: %s'
               % data['deletedCampaignCriteria'])
        print ('  Campaign targeting changed: %s'
               % data['campaignTargetingChanged'])
        if data['changedAdGroups']:
          for ad_group_data in data['changedAdGroups']:
            print ('  Ad group with id \'%s\' has change status \'%s\'.'
                   % (ad_group_data['adGroupId'],
                      ad_group_data['adGroupChangeStatus']))
            if ad_group_data['adGroupChangeStatus'] != 'NEW':
              print '    Changed ads: %s' % ad_group_data['changedAds']
              print ('    Changed criteria: %s'
                     % ad_group_data['changedCriteria'])
              print ('    Deleted criteria: %s'
                     % ad_group_data['deletedCriteria'])
else:
  print 'No changes were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
