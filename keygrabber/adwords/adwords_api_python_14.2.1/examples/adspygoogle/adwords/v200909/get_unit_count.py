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

"""This example retrieves the number of API units recorded over the given date
range.

Tags: InfoService.get
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import datetime
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))
client.use_mcc = True

# Initialize appropriate service.
info_service = client.GetInfoService(
    'https://adwords-sandbox.google.com', 'v200909')

# Construct info selector object and retrieve usage info.
today = datetime.datetime.today()
selector = {
    'dateRange': {
        'min': today.strftime('%Y%m01'),
        'max': today.strftime('%Y%m%d')
    },
    'apiUsageType': 'UNIT_COUNT'
}
info = info_service.Get(selector)[0]

# Display results.
print ('The total number of API units consumed during \'%s\'-\'%s\' is \'%s\'.'
       % (selector['dateRange']['min'], selector['dateRange']['max'],
          info['cost']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
