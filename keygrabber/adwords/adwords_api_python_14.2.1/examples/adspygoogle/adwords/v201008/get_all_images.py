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

"""This example gets all images. To upload an image, run upload_image.py.

Tags: MediaService.get
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
media_service = client.GetMediaService(
    'https://adwords-sandbox.google.com', 'v201008')

# Construct selector and get all images.
selector = {
    'mediaType': 'IMAGE'
}
images = media_service.Get(selector)[0]

# Display results.
if 'media' in images:
  for image in images['media']:
    dimensions = Utils.GetDictFromMap(image['dimensions'])
    print ('Image with id \'%s\', dimensions \'%sx%s\', and MIME type \'%s\' '
           'was found.' % (image['mediaId'], dimensions['FULL']['height'],
                           dimensions['FULL']['width'], image['mimeType']))
else:
  print 'No images were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
