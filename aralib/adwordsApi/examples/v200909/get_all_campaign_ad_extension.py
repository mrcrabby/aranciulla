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

"""This example gets all campaign ad extensions in a given campaign. To add a
campaign ad extension override, run add_campaign_ad_extension_override.py.

Tags: CampaignAdExtensionService.get
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('../..')

# Import appropriate classes from the client library.
from aw_api.Client import Client


# Initialize client object.
client = Client(path='../..')

# Initialize appropriate service.
campaign_ad_extension_service = client.GetCampaignAdExtensionService(
    'https://adwords-sandbox.google.com', 'v200909')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct selector and get all campaigns.
selector = {
    'campaignIds': [campaign_id]
}
ad_extensions = campaign_ad_extension_service.Get(selector)[0]

# Display results.
if 'entries' in ad_extensions:
  for ad_extension in ad_extensions['entries']:
    print ('Campaign ad extension with id \'%s\' and status \'%s\' was found.'
           % (ad_extension['adExtension']['id'], ad_extension['status']))
else:
  print 'No campaign ad extensions were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
