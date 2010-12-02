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

"""This demo fetches info for all direct sub accounts.

Tags: AccountService.getClientAccounts, AccountService.getAccountInfo
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.append('../..')

# Import appropriate constants and classes from the client library.
from aw_api import SOAPPY
from aw_api.Client import Client


# Initialize Client object. The "path" parameter should point to the location of
# pickles, which get generated after execution of "aw_api_config.py" script. The
# same location is used for the "logs/" directory, if logging is enabled. The
# "soap_lib" parameter can be used to specify which SOAP toolkit to use.
client = Client(path='../..', soap_lib=SOAPPY)
# OR another way of specifying authentication data is through "headers"
# parameter, which takes precedence over loading from a pickle. The "path" is
# optional here and is specified to let client library know where to place logs.
#client = Client(headers={
#    'email': 'johndoe@example.com',
#    'password': 'secret',
#    'userAgent': 'My Test',
#    'developerToken': 'johndoe@example.com++USD'}, path='..')

# Temporarily disable debugging. If enabled, the debugging data will be send to
# STDOUT.
client.debug = False

# Force following API requests to go against MCC account. This can be changed
# at any time by setting it back to False.
client.use_mcc = True

# Initialize appropriate API service and fetch all sub accounts' logins. By
# default, the request is always made against production environment. Thus, we
# need to send server parameter here to explicitly point requests against
# Sandbox, "sandbox.google.com".
logins = client.GetAccountService(
    'https://sandbox.google.com').GetClientAccounts()
client.UseMcc(False)
for login in logins:
  client.SetClientEmail(login)

  # Initialize appropriate API service and fetch account info for each sub
  # account.
  info = client.GetAccountService('https://sandbox.google.com').GetAccountInfo()
  print ('Customer Id: %s\n  Client email: %s\n  '
         'Descriptive name: %s\n  Time zone Id: %s\n'
         % (info[0]['customerId'], login, info[0]['descriptiveName'],
            info[0]['timeZoneId']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
