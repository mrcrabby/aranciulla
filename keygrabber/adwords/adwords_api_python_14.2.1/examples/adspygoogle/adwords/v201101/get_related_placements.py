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

"""This example retrieves urls that have content keywords related to a given
website.

Tags: TargetingIdeaService.get
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
targeting_idea_service = client.GetTargetingIdeaService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct selector object and retrieve related placements.
url = 'http://mars.google.com'
selector = {
    'searchParameters': [{
        'xsi_type': 'RelatedToUrlSearchParameter',
        'urls': [url],
        'includeSubUrls': 'False'
    }],
    'ideaType': 'PLACEMENT',
    'requestType': 'IDEAS',
    'requestedAttributeTypes': ['SAMPLE_URL'],
    'paging': {
        'startIndex': '0',
        'numberResults': '10'
    }
}
page = targeting_idea_service.Get(selector)[0]

# Display results.
if 'entries' in page:
  for result in page['entries']:
    result = result['data'][0]['value']
    print ('Related content keywords were found at \'%s\' url.'
           % result['value'])
  print
  print ('Total urls found with content keywords related to keywords at \'%s\':'
         ' %s' % (url, page['totalNumEntries']))
else:
  print 'No content keywords were found at \'%s\'.' % url

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
