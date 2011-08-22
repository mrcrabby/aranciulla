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

"""This example updates a conversion tracker by setting its status to DISABLED.

To get conversion trackers, run get_all_conversion_trackers.py.

Tags: ConversionTrackerService.mutate
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

conversion_tracker_id = 'INSERT_CONVERSION_TRACKER_ID_HERE'

# Construct operations and update conversion_tracker.
operations = [
    {
        'operator': 'SET',
        'operand': {
            'xsi_type': 'AdWordsConversionTracker',
            'id': conversion_tracker_id,
            'status': 'DISABLED'
        }
    }
]
conversion_trackers = conversion_tracker_service.Mutate(operations)[0]

# Display results.
for conversion_tracker in conversion_trackers['value']:
  print ('Conversion tracker with id \'%s\', name \'%s\', status \'%s\' '
         'and category \'%s\' was disabled.\n' %
         (conversion_tracker['id'], conversion_tracker['name'],
          conversion_tracker['status'], conversion_tracker['category']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
