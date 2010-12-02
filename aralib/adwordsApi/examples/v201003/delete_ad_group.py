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

"""This example deletes an ad group by setting the status to 'DELETED'. To get
ad groups, run get_all_ad_groups.py.

Tags: AdGroupService.mutate
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
    'https://adwords-sandbox.google.com', 'v201003')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'

# Construct operations and delete ad group.
operations = [{
    'operator': 'SET',
    'operand': {
        'id': ad_group_id,
        'status': 'DELETED'
    }
}]
result = ad_group_service.Mutate(operations)[0]

# Display results.
if 'value' in result:
  for ad_group in result['value']:
    print ('Ad group with name \'%s\' and id \'%s\' was deleted.'
           % (ad_group['name'], ad_group['id']))
else:
  print 'No campaigns were deleted.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
