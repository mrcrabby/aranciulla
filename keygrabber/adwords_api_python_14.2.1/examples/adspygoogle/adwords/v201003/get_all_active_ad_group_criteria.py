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

"""This example gets all active ad group criteria in an account. To add ad group
criteria, run add_ad_group_criteria.py.

Tags: AdGroupCriterionService.get
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
ad_group_criterion_service = client.GetAdGroupCriterionService(
    'https://adwords-sandbox.google.com', 'v201003')

# Construct selector and get all active ad group criteria.
selector = {
    'userStatuses': ['ACTIVE']
}
ad_group_criteria = ad_group_criterion_service.Get(selector)[0]['entries']

# Display results.
for criterion in ad_group_criteria:
  if criterion['criterion']['Criterion_Type'] == 'Keyword':
    print ('Keyword ad group criterion with ad group id \'%s\', criterion id '
           '\'%s\', text \'%s\', and match type \'%s\' was found.'
           % (criterion['adGroupId'], criterion['criterion']['id'],
              criterion['criterion']['text'],
              criterion['criterion']['matchType']))
  elif criterion['criterion']['Criterion_Type'] == 'Placement':
    print ('Placement ad group criterion with ad group id \'%s\', criterion '
           'id \'%s\', and url \'%s\' was found.'
           % (criterion['adGroupId'], criterion['criterion']['id'],
              criterion['criterion']['url']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
