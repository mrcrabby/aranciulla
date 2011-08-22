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

"""This example shows how to check for conversion optimizer eligibility.

Tags: CampaignService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.adwords.AdWordsErrors import AdWordsRequestError


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service with validate only flag enabled.
client.validate_only = True
campaign_service = client.GetCampaignService(
    'https://adwords-sandbox.google.com', 'v200909')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct operations for setting bidding transition on a campaign.
try:
  operations = [{
      'operator': 'SET',
      'biddingTransition': {
          'targetBiddingStrategy': {
              'type': 'ConversionOptimizer',
              'pricingModel': 'CONVERSIONS'
          },
          'explicitAdGroupBids': {
              'type': 'ConversionOptimizerAdGroupBids'
          }
      },
      'operand': {
          'id': campaign_id
      }
  }]
  campaigns = campaign_service.Mutate(operations)[0]

  # Display results.
  print ('Campaign with id \'%s\' is eligible to use conversion optimizer.'
         % campaign_id)
except AdWordsRequestError, e:
  # Display results.
  for error in e.errors:
    if error.type == 'BiddingTransitionError':
      print ('Campaign with id \'%s\' is not eligible to use conversion '
             'optimizer due to \'%s\'.' % (campaign_id, error.reason))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
