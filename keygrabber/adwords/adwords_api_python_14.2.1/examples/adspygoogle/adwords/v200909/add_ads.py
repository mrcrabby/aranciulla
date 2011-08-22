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

"""This example adds a text and image ads to a given ad group. To get ad_group,
run get_all_ad_groups.py.

Tags: AdGroupAdService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import base64
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import SOAPPY
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
ad_group_ad_service = client.GetAdGroupAdService(
    'https://adwords-sandbox.google.com', 'v200909')

ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
image_data = Utils.ReadFile('INSERT_IMAGE_PATH_HERE')
if client.soap_lib == SOAPPY:
  image_data = base64.encodestring(image_data)

# Construct operations and add ads.
operations = [
    {
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': ad_group_id,
            'ad': {
                'type': 'TextAd',
                'url': 'http://www.example.com',
                'displayUrl': 'example.com',
                'status': 'ENABLED',
                'description1': 'Visit the Red Planet in style.',
                'description2': 'Low-gravity fun for everyone!',
                'headline': 'Luxury Cruise to Mars'
            }
        }
    },
    {
        'operator': 'ADD',
        'operand': {
            'type': 'AdGroupAd',
            'adGroupId': ad_group_id,
            'ad': {
                'type': 'ImageAd',
                'image': {
                    'dimensions': [{
                        'key': 'FULL',
                        'value': {'width': '300', 'height': '250'}
                    }],
                    'name': 'image.jpg',
                    'data': image_data
                },
                'name': 'Cruise to mars image ad #%s' % Utils.GetUniqueName(),
                'url': 'http://www.example.com',
                'displayUrl': 'www.example.com'
            }
        }
    }
]
ads = ad_group_ad_service.Mutate(operations)[0]

# Display results.
for ad in ads['value']:
  print ('Ad with id \'%s\' and of type \'%s\' was added.'
         % (ad['ad']['id'], ad['ad']['Ad_Type']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
