#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example demonstrates how to authenticate using OAuth.

This example is meant to be run from the command line and requires
user input.
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys

sys.path.append(os.path.join('..', '..', '..', '..'))
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common.oauth.PythonOAuth2OAuthHandler import PythonOAuth2OAuthHandler

# Set the OAuth consumer key and secret. Anonymous values can be used for
# testing, and real values can be obtained by registering your application:
# http://code.google.com/apis/accounts/docs/RegistrationForWebAppsAuto.html
credentials = {
    'oauth_consumer_key': 'anonymous',
    'oauth_consumer_secret': 'anonymous',
}

# Create the AdWordsUser and set the OAuth credentials.
client = AdWordsClient(path=os.path.join('..', '..', '..'))
client.SetOAuthCredentials(credentials)

# Now set the handler and enable OAuth.
client.SetOAuthHandler(PythonOAuth2OAuthHandler())
client.EnableOAuth()

# Request a new OAuth token. Web applications should pass in a callback URL to
# redirect the user to after authorizing the token.
client.RequestOAuthToken('https://adwords.google.com',
                         applicationname='OAuth Example')

# Get the authorization URL for the OAuth token.
authorizationurl = client.GetOAuthAuthorizationUrl()

# In a web application you would redirect the user to the authorization URL
# and after approving the token they would be redirected back to the
# callback URL with the URL parameter "oauth_verifier" added. For desktop or
# server applications, spawn a browser to the URL and then have the user enter
# the verification code that is displayed.
print ('Log in to your AdWords account and open the following URL: %s\n' %
       authorizationurl)
print 'After approving the token enter the verification code (if specified).'
verifier = raw_input('Verifier: ')

# Upgrade the authorized token.
client.UpgradeOAuthToken(verifier)

# An upgraded token does not expire and should be stored and reused for
# every request to the API.
credentials = client.GetOAuthCredentials()
print ('OAuth authorization successful.  Store these credentials to reuse' +
       ' until revoked: %s' % credentials)

# Note: you could simply client.SetOAuthCredentials(credentials) and skip the
# previous steps once access has been granted.

campaign_service = client.GetCampaignService(
    'https://adwords.google.com', 'v201101')

# Get all campaigns.
# Construct selector and get all campaigns.
selector = {
    'fields': ['Id', 'Name', 'Status']
}
campaigns = campaign_service.Get(selector)[0]

# Display results.
if 'entries' in campaigns:
  for campaign in campaigns['entries']:
    print ('Campaign with id \'%s\', name \'%s\', and status \'%s\' was found.'
           % (campaign['id'], campaign['name'], campaign['status']))
else:
  print 'No campaigns were found.'
