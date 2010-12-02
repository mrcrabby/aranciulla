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

"""This example retrieves keywords that are related to a given keyword.

Tags: TargetingIdeaService.get
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('../..')

# Import appropriate classes from the client library.
from aw_api.Client import Client


# Initialize client object.
client = Client(path='../..')

# Initialize appropriate service.
targeting_idea_service = client.GetTargetingIdeaService(
    'https://adwords-sandbox.google.com', 'v200909')

# Construct info selector object and retrieve usage info.
keyword = 'space cruise'
selector = {
    'searchParameters': [{
        'type': 'RelatedToKeywordSearchParameter',
        'keywords': [{
            'text': keyword,
            'matchType': 'EXACT'
        }]
    }],
    'ideaType': 'KEYWORD',
    'requestType': 'IDEAS',
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
    print ('Keyword with \'%s\' text and \'%s\' match type is found.'
           % (result['value']['text'], result['value']['matchType']))
  print
  print 'Total keywords found related to \'%s\': %s' % (keyword,
                                                        page['totalNumEntries'])
else:
  print 'No keywords found related to \'%s\'.' % keyword

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
