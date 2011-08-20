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

"""This example gets all users lists. To add a user list, run add_user_list.py.

Tags: UserListService.get
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
user_list_service = client.GetUserListService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct selector and get all user lists.
selector = {
    'fields': ['Id', 'Name', 'Status', 'Size']
}
page = user_list_service.Get(selector)[0]

# Display results.
if 'entries' in page:
  for user_list in page['entries']:
    print ('User list with name \'%s\', id \'%s\', status \'%s\', and number '
           'of users \'%s\' was found.'
           % (user_list['name'], user_list['id'], user_list['status'],
              user_list['size']))
else:
  print 'No user lists were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
