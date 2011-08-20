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

"""This example gets account info by posting a raw SOAP XML message.

Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate constants and classes from the client library.
from adspygoogle.adwords import MIN_API_VERSION
from adspygoogle.common import Utils
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsApiError


# Initialize AdWordsClient object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Construct SOAP message by loading XML from existing data file.
soap_message = Utils.ReadFile(
    os.path.join('..', '..', '..', '..', 'tests', 'adspygoogle', 'adwords',
                 'data', 'request_getaccountinfo.xml'))
server = 'https://adwords-sandbox.google.com'
url = '/api/adwords/%s/AccountService' % MIN_API_VERSION
http_proxy = None

try:
  response = client.CallRawMethod(soap_message, url, server, http_proxy)[0]

  # Display results.
  print 'Response:\n%s' % response
except AdWordsApiError, e:
  print 'Note: this should fail, unless you\'ve set valid authentication data.'
  print
  raise e

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
