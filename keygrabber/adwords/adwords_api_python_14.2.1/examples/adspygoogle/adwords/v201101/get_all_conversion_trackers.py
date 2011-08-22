#!/usr/bin/python
#
# Copyright 2010 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example gets all conversions in the account.

To add a conversion, run add_conversion_tracker.py.

Tags: ConversionTrackerService.get
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
conversion_tracker_service = client.GetConversionTrackerService(
    'https://adwords-sandbox.google.com', 'v201101')

# Create selector.
selector = {
    'fields': ['Name', 'Status', 'Category'],
    'ordering': [{
        'field': 'Name',
        'sortOrder': 'ASCENDING'
    }]
}
ret = conversion_tracker_service.Get(selector)[0]

# Display results.
if 'entries' in ret and ret['entries']:
  for conversion_tracker in ret['entries']:
    print ('Conversion tracker with id \'%s\', name \'%s\', status \'%s\' '
           'and category \'%s\' and snippet \n\'%s\'\n was added.\n' %
           (conversion_tracker['id'], conversion_tracker['name'],
            conversion_tracker['status'], conversion_tracker['category'],
            conversion_tracker['snippet']))
else:
  print 'No conversion trackers were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
