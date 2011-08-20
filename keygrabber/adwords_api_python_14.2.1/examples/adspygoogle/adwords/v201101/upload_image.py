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

"""This example uploads an image. To get images, run get_all_images.py.

Tags: MediaService.upload
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
media_service = client.GetMediaService(
    'https://adwords-sandbox.google.com', 'v201101')

image_data = Utils.ReadFile('INSERT_IMAGE_PATH_HERE')
if client.soap_lib == SOAPPY:
  image_data = base64.encodestring(image_data)

# Construct media and upload image.
media = [{
    # TODO: SOAPpy needs an xsi_type here, but SOAPpy has other problems
    'data': image_data,
    'type': 'IMAGE'
}]
media = media_service.Upload(media)[0]

# Display results.
if media:
  dimensions = Utils.GetDictFromMap(media['dimensions'])
  # WARNING: SOAPpy turns the dimensions field into a list, so this won't work
  print ('Image with id \'%s\', dimensions \'%sx%s\', and MIME type \'%s\' was '
         'uploaded.' % (media['mediaId'], dimensions['FULL']['height'],
                        dimensions['FULL']['width'], media['mimeType']))
else:
  print 'No images were uploaded.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
