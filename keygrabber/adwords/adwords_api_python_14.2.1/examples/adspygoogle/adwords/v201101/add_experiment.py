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

"""This example creates an experiment using a query percentage of 10, which
defines what fraction of auctions should go to the control split (90%) vs. the
experiment split (10%), then adds experimental bid changes for an ad group, and
adds an experiment-only keyword. To get campaigns, run get_all_campaigns.py. To
get ad groups, run get_all_ad_groups.py. To get criteria,
run get_all_ad_group_criteria.py.

Tags: ExperimentService.mutate
Api: AdWordsOnly
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import datetime
import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
experiment_service = client.GetExperimentService(
    'https://adwords-sandbox.google.com', 'v201101')
ad_group_service = client.GetAdGroupService(
    'https://adwords-sandbox.google.com', 'v201101')
ad_group_criterion_service = client.GetAdGroupCriterionService(
    'https://adwords-sandbox.google.com', 'v201101')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'
ad_group_id = 'INSERT_AD_GROUP_ID_HERE'

# Construct operations and add experiment.
today = datetime.datetime.now()
operations = [{
    'operator': 'ADD',
    'operand': {
        'campaignId': campaign_id,
        'name': 'Interplanetary Experiment #%s' % Utils.GetUniqueName(),
        'queryPercentage': '10',
        'startDateTime': today.strftime('%Y%m%d %H%M%S')
    }
}]
result = experiment_service.Mutate(operations)[0]

# Display results.
if 'value' in result:
  for experiment in result['value']:
    print ('Experiment with name \'%s\' and id \'%s\' was added.'
           % (experiment['name'], experiment['id']))

    # Construct operations and update ad group.
    operations = [{
        'operator': 'SET',
        'operand': {
            'id': ad_group_id,
            'experimentData': {
                'xsi_type': 'AdGroupExperimentData',
                'experimentId': experiment['id'],
                'experimentDeltaStatus': 'MODIFIED',
                'experimentBidMultipliers': {
                    'xsi_type': 'ManualCPCAdGroupExperimentBidMultipliers',
                    'maxCpcMultiplier': {
                        'multiplier': '0.5'
                    }
                }
            }
        }
    }]
    result = ad_group_service.Mutate(operations)[0]

    # Display results.
    if 'value' in result:
      for ad_group in result['value']:
        print ('Ad group with name \'%s\' and id \'%s\' was updated in the '
               'experiment.' % (ad_group['name'], ad_group['id']))

        # Construct operations and add ad group crierion.
        operations = [{
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'BiddableAdGroupCriterion',
                'adGroupId': ad_group['id'],
                'criterion': {
                    'xsi_type': 'Keyword',
                    'matchType': 'BROAD',
                    'text': 'mars cruise'
                },
                'experimentData': {
                    'xsi_type': 'BiddableAdGroupCriterionExperimentData',
                    'experimentId': experiment['id'],
                    'experimentDeltaStatus': 'EXPERIMENT_ONLY'
                }
            }
        }]
        result = ad_group_criterion_service.Mutate(operations)[0]

        # Display results.
        if 'value' in result:
          for criterion in result['value']:
            print ('Ad group criterion with ad group id \'%s\' and criterion '
                   'id \'%s\' was added to the experiment.'
                   % (criterion['adGroupId'], criterion['criterion']['id']))
        else:
          print 'No ad group criteria were added.'
    else:
      print 'No ad groups were updated.'
else:
  print 'No experiments were added.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
