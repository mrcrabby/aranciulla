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
#

"""This example gets all ad groups for a given campaign. To add an ad group,
run add_ad_group.py.

Tags: AdGroupService.get
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('../..')

# Import appropriate classes from the client library.
from aw_api.Client import Client


# Initialize client object.
client = Client(path='../..')

# Initialize appropriate service.
ad_group_service = client.GetAdGroupService(
    'https://adwords-sandbox.google.com', 'v200909')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct selector and get all ad groups.
selector = {
    'campaignId': campaign_id
}
ad_groups = ad_group_service.Get(selector)[0]

# Display results.
if 'entries' in ad_groups:
  for ad_group in ad_groups['entries']:
    print ('Ad group with name \'%s\', id \'%s\', and status \'%s\' was found.'
           % (ad_group['name'], ad_group['id'], ad_group['status']))
else:
  print 'No ad groups were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
