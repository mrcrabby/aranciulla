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

"""This example adds a text ad with ad parameters. To get ad groups, run
get_all_ad_groups.py. To get ad group criteria, run add_ad_group_criteria.py.

Tags: AdGroupAdService.mutate, AdParamService.mutate
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
    'https://adwords-sandbox.google.com', 'v201008')
ad_param_service = client.GetAdParamService(
    'https://adwords-sandbox.google.com', 'v201008')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
criterion_id = 'INSERT_CRITERION_ID_HERE'

# Construct operations for adding text ad object and add to an ad group.
operations = [{
    'operator': 'ADD',
    'operand': {
        'xsi_type': 'AdGroupAd',
        'adGroupId': ad_group_id,
        'ad': {
            'xsi_type': 'TextAd',
            'url': 'http://www.example.com',
            'displayUrl': 'example.com',
            'status': 'ENABLED',
            'description1': 'Low-gravity fun for {param1:cheap}.',
            'description2': 'Only {param2:a few} seats left!',
            'headline': 'Luxury Mars Cruises'
        }
    }
}]
ads = ad_group_ad_service.Mutate(operations)[0]['value']

# Display results.
for ad in ads:
  print ('Text ad with id \'%s\' was successfully added to an ad group with '
         'id \'%s\'.' % (ad['adGroupId'], ad['ad']['id']))

# Construct operations for setting ad parameters.
operations = [
    {
        'operator': 'SET',
        'operand': {
            'adGroupId': ad_group_id,
            'criterionId': criterion_id,
            'insertionText': '$100',
            'paramIndex': '1'
        }
    },
    {
        'operator': 'SET',
        'operand': {
            'adGroupId': ad_group_id,
            'criterionId': criterion_id,
            'insertionText': '50',
            'paramIndex': '2'
        }
    }
]
ad_params = ad_param_service.Mutate(operations)

# Display results.
for ad_param in ad_params:
  print ('Ad parameter with text \'%s\' was successfully set for criterion '
         'with id \'%s\' and ad group id \'%s\'.'
         % (ad_param['insertionText'], ad_param['criterionId'],
            ad_param['adGroupId']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
