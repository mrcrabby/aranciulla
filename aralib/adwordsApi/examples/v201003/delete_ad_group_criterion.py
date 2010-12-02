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

"""This example deletes an ad group criterion using the 'REMOVE' operator. To
get ad group criteria, run get_all_ad_group_criteria.py.

Tags: AdGroupCriterionService.mutate
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('../..')

# Import appropriate classes from the client library.
from aw_api.Client import Client


# Initialize client object.
client = Client(path='../..')

# Initialize appropriate service.
ad_group_criterion_service = client.GetAdGroupCriterionService(
    'https://adwords-sandbox.google.com', 'v201003')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
criterion_id = 'INSERT_CRITERION_ID_HERE'

# Construct operations and delete ad group criteria.
operations = [
    {
        'operator': 'REMOVE',
        'operand': {
            'type': 'BiddableAdGroupCriterion',
            'adGroupId': ad_group_id,
            'criterion': {
                'id': criterion_id
            }
        }
    }
]
result = ad_group_criterion_service.Mutate(operations)[0]

# Display results.
if 'value' in result:
  for criterion in result['value']:
    print ('Ad group criterion with ad group id \'%s\', criterion id \'%s\', '
           'and type \'%s\' was deleted.'
           % (criterion['adGroupId'], criterion['criterion']['id'],
              criterion['criterion']['Criterion_Type']))
else:
  print 'No ad group criteria were deleted.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
