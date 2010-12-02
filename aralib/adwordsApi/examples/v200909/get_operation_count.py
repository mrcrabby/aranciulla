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

"""This example retrieves the number of operations recorded over the given date
range.

Tags: InfoService.get
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import datetime
import sys
sys.path.append('../..')

# Import appropriate classes from the client library.
from aw_api.Client import Client


# Initialize client object.
client = Client(path='../..')

# Initialize appropriate service.
info_service = client.GetInfoService(
    'https://adwords-sandbox.google.com', 'v200909')

# Construct info selector object and retrieve usage info.
today = datetime.datetime.today()
selector = {
    'dateRange': {
        'min': '%s%s01' % (today.year, today.month),
        'max': '%s%s%s' % (today.year, today.month, today.day)
    },
    'apiUsageType': 'OPERATION_COUNT'
}
info = info_service.Get(selector)[0]

# Display results.
print ('The total number of operations consumed during \'%s\'-\'%s\' is \'%s\'.'
       % (selector['dateRange']['min'], selector['dateRange']['max'],
          info['cost']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
