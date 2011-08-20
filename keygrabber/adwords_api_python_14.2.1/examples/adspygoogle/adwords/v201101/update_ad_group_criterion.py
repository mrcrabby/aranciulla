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

"""This example updates the bid of an ad group criterion. To add ad group
criteria, run add_ad_group_criteria.py.

Tags: AdGroupCriterionService.mutate
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
ad_group_criterion_service = client.GetAdGroupCriterionService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct operations and update bids.
ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
criterion_id = 'INSERT_CRITERION_ID_HERE'
operations = [{
    'operator': 'SET',
    'operand': {
        'xsi_type': 'BiddableAdGroupCriterion',
        'adGroupId': ad_group_id,
        'criterion': {
            'id': criterion_id,
        },
        'bids': {
            'xsi_type': 'ManualCPCAdGroupCriterionBids',
            'maxCpc': {
                'amount': {
                    'microAmount': '500000'
                }
            }
        }
    }
}]
ad_group_criteria = ad_group_criterion_service.Mutate(operations)[0]

# Display results.
if 'value' in ad_group_criteria:
  for criterion in ad_group_criteria['value']:
    if criterion['criterion']['Criterion_Type'] == 'Keyword':
      print ('Ad group criterion with ad group id \'%s\' and criterion id '
             '\'%s\' had its bid set to \'%s\'.'
             % (criterion['adGroupId'], criterion['criterion']['id'],
                criterion['bids']['maxCpc']['amount']['microAmount']))
else:
  print 'No ad group criteria were updated.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
