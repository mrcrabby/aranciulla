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

"""This example updates status for a given ad. To get ads, run
get_all_ads.py.

Tags: AdGroupAdService.mutate
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
ad_group_ad_service = client.GetAdGroupAdService(
    'https://adwords-sandbox.google.com', 'v200909')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
ad_id = 'INSERT_AD_ID_HERE'

# Construct operations and update an ad.
operations = [{
    'operator': 'SET',
    'operand': {
        'adGroupId': ad_group_id,
        'ad': {
            'id': ad_id,
        },
        'status': 'PAUSED'
    }
}]
ads = ad_group_ad_service.Mutate(operations)[0]

# Display results.
for ad in ads['value']:
  print 'Ad with id \'%s\' was updated.'% ad['ad']['id']

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
