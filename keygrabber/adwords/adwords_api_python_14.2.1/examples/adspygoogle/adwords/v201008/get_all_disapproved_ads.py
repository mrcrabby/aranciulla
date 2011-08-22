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

"""This example gets all disapproved ads for a given campaign. To add an ad, run
add_ads.py.

Tags: AdGroupAdService.get
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
ad_group_ad_service = client.GetAdGroupAdService(
    'https://adwords-sandbox.google.com', 'v201008')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct selector and get all ads for a given ad group.
selector = {
    'campaignIds': [campaign_id]
}
ads = ad_group_ad_service.Get(selector)[0]

# Display results.
if 'entries' in ads:
  has_disapproved_ads = False
  for ad in ads['entries']:
    if ad['ad']['approvalStatus'] == ' DISAPPROVED':
      has_disapproved_ads = True
      print ('Ad with id \'%s\' was disapproved for the following reasons: '
             % (ad['ad']['id']))
      for reason in ad['ad']['disapprovalReasons']:
        print '  %s' % reason
  if not has_disapproved_ads:
    print 'No disapproved ads were found.'
else:
  print 'No ads were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
