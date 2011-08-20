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

"""This example deletes a user list by setting the status to 'CLOSED'. To get
user lists, run get_all_user_lists.py.

Tags: UserListService.mutate
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
user_list_service = client.GetUserListService(
    'https://adwords-sandbox.google.com', 'v201008')

user_list_id = 'INSERT_USER_LIST_ID_HERE'

# Construct operations and delete a user list.
operations = [
    {
        'operator': 'SET',
        'operand': {
            'xsi_type': 'RemarketingUserList',
            'id': user_list_id,
            'status': 'CLOSED'
        }
    }
]
result = user_list_service.Mutate(operations)[0]

# Display results.
if 'value' in result:
  for user_list in result['value']:
    print ('User list with name \'%s\' and id \'%s\' was deleted (closed).'
           % (user_list['name'], user_list['id']))
else:
  print 'No user lists were deleted.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
