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

"""This example adds ads and criteria asynchronously to a given ad group. To
get ad_group, run get_all_ad_groups.py.

Tags: BulkMutateJobService.mutate, BulkMutateJobService.get
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

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
bulk_mutate_job_service = client.GetBulkMutateJobService(
    'https://adwords-sandbox.google.com', 'v201101')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'
ad_group_id = 'INSERT_AD_GROUP_ID_HERE'
image_data = Utils.ReadFile('INSERT_IMAGE_PATH_HERE')
if client.soap_lib == SOAPPY:
  image_data = base64.encodestring(image_data)

# Construct part for adding ads and add it to a job.
ads = {
    'scopingEntityId': {
        'type': 'CAMPAIGN_ID',
        'value': campaign_id,
    },
    'operations': [
        {
            'xsi_type': 'AdGroupAd',
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'AdGroupAd',
                'adGroupId': ad_group_id,
                'ad': {
                    'xsi_type': 'TextAd',
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
            'xsi_type': 'AdGroupAd',
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'AdGroupAd',
                'adGroupId': ad_group_id,
                'ad': {
                    'xsi_type': 'ImageAd',
                    'image': {
                        'dimensions': [{
                            'key': 'FULL',
                            'value': {'width': '300', 'height': '250'}
                        }],
                        'name': 'image.jpg',
                        'data': image_data
                    },
                    'name': 'Test image',
                    'url': 'http://www.example.com',
                    'displayUrl': 'www.example.com'
                }
            }
        }
    ]
}
operation = {
    'operator': 'ADD',
    'operand': {
        'type': 'BulkMutateJob',
        'request': {
            'partIndex': '0',
            'operationStreams': [ads]
        },
        'numRequestParts': '2'
    }
}
job = bulk_mutate_job_service.Mutate(operation)[0]

# Construct part for adding criteria and add it to a job.
operations = []
for index in xrange(100):
  operations.append(
      {
          'xsi_type': 'AdGroupCriterion',
          'operator': 'ADD',
          'operand': {
              'xsi_type': 'BiddableAdGroupCriterion',
              'adGroupId': ad_group_id,
              'criterion': {
                  'xsi_type': 'Keyword',
                  'matchType': 'BROAD',
                  'text': 'mars%s' % index
              }
          }
      })
criteria = {
    'scopingEntityId': {
        'type': 'CAMPAIGN_ID',
        'value': campaign_id,
    },
    'operations': operations
}
operation = {
    'operator': 'SET',
    'operand': {
        'xsi_type': 'BulkMutateJob',
        'id': job['id'],
        'request': {
            'partIndex': '1',
            'operationStreams': [criteria]
        }
    }
}
job = bulk_mutate_job_service.Mutate(operation)[0]

# Wait for job to finish and get results.
results = bulk_mutate_job_service.DownloadBulkJob(job['id'])
ads = results[0]['result']['operationStreamResults'][0]['operationResults']
criteria = results[1]['result']['operationStreamResults'][0]['operationResults']

# Display results.
for ad in ads:
  ad = ad['returnValue']['AdGroupAd']
  print ('Ad of type \'%s\' and id \'%s\' was added.'
         % (ad['ad']['Ad_Type'], ad['ad']['id']))

for criterion in criteria:
  criterion = criterion['returnValue']['AdGroupCriterion']
  print ('Criterion of type \'%s\' and id \'%s\' was added.'
         % (criterion['criterion']['Criterion_Type'],
            criterion['criterion']['id']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
