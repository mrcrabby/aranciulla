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

"""This example gets all videos. To upload video, see
http://adwords.google.com/support/aw/bin/answer.py?hl=en&answer=39454.

Tags: MediaService.get
Api: AdWordsOnly
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
media_service = client.GetMediaService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct selector and get all videos.
selector = {
    'fields': ['MediaId', 'Type', 'Width', 'Height'],
    'predicates': [{
        'field': 'Type',
        'operator': 'EQUALS',
        'values': ['VIDEO']
    }]
}
videos = media_service.Get(selector)[0]

# Display results.
if 'media' in videos:
  for video in videos['media']:
    print ('Video with id \'%s\' and name \'%s\' '
           'was found.'  % (video['mediaId'], video['name']))
else:
  print 'No videos were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
