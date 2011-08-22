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

"""This example gets all experiments in a campaign. To add an experiment, run
add_experiment.py. To get campaigns, run get_all_campaigns.py.

Tags: ExperimentService.get
Api: AdWordsOnly
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
experiment_service = client.GetExperimentService(
    'https://adwords-sandbox.google.com', 'v201008')

campaign_id = 'INSERT_CAMPAIGN_ID_HERE'

# Construct selector and get all experiments.
selector = {
    'campaignIds': [campaign_id],
    'includeStats': 'true'
}
experiments = experiment_service.Get(selector)[0]

# Display results.
if 'entries' in experiments:
  for experiment in experiments['entries']:
    print ('Experiment with name \'%s\', id \'%s\', and control id \'%s\' was'
           'found. It includes %s ad groups and %s criteria.'
           % (experiment['name'], experiment['id'], experiment['controlId'],
              experiment['experimentSummaryStats']['adGroupsCount'],
              experiment['experimentSummaryStats']['adGroupCriteriaCount']))
else:
  print 'No experiments were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
