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

"""This example gets all ads for a given ad group. To add an ad, run
add_ads.py.

Tags: AdGroupAdService.get
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
ad_group_ad_service = client.GetAdGroupAdService(
    'https://adwords-sandbox.google.com', 'v201101')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'

# Construct selector and get all ads for a given ad group.
selector = {
    'fields': ['Id', 'AdGroupId', 'Status'],
    'predicates': [
        {
            'field': 'AdGroupId',
            'operator': 'EQUALS',
            'values': [ad_group_id]
        }
    ]
}
ads = ad_group_ad_service.Get(selector)[0]

# Display results.
if 'entries' in ads:
  for ad in ads['entries']:
    print ('Ad with id \'%s\', status \'%s\', and of type \'%s\' was found.'
           % (ad['ad']['id'], ad['status'], ad['ad']['Ad_Type']))
else:
  print 'No ads were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
