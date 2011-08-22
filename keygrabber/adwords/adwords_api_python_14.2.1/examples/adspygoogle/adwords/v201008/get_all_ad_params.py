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

"""This example gets all ad parameters in an ad group. To set ad params, run
set_ad_params.py.

Tags: AdParamService.get
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
ad_param_service = client.GetAdParamService(
    'https://adwords-sandbox.google.com', 'v201008')

# Construct selector and get all ad params.
ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
selector = {
    'adGroupIds': [ad_group_id]
}
ad_params = ad_param_service.Get(selector)[0]

# Display results.
if 'entries' in ad_params:
  for ad_param in ad_params['entries']:
    print ('Ad param with text \'%s\' was found for criterion with id \'%s\' '
           'and ad group id \'%s\'.'
           % (ad_param['insertionText'], ad_param['criterionId'],
              ad_param['adGroupId']))
else:
  print 'No ad parameters found in ad group with id \'%s\'.' % ad_group_id

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
