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

"""This demo gets account info by posting raw SOAP XML message."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
# Locate the client library. If module was installed via "setup.py" script, then
# the following two lines are not needed.
import sys
sys.path.append('../..')

# Import appropriate constants and classes from the client library.
from aw_api import LIB_HOME
from aw_api import MIN_API_VERSION
from aw_api import Utils
from aw_api.Client import Client
from aw_api.Errors import ApiError


# Initialize Client object. The "path" parameter should point to the location of
# pickles, which get generated after execution of "aw_api_config.py" script. The
# same location is used for the "logs/" directory, if logging is enabled.
client = Client(path='../..')

# Temporarily disable debugging. If enabled, the debugging data will be send to
# STDOUT.
client.debug = False

# Construct SOAP message by loading XML from existing data file.
soap_message = Utils.ReadFile(
    os.path.join(LIB_HOME, 'data', 'request_getaccountinfo.xml'))
url = '/api/adwords/%s/AccountService' % MIN_API_VERSION
http_proxy = None

try:
  response = client.CallRawMethod(soap_message, url, http_proxy)[0]

  # Display results.
  print 'Response:\n%s' % response
except ApiError, e:
  print 'Note: this should fail, unless you provide valid authentication data.'
  print
  raise e

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
