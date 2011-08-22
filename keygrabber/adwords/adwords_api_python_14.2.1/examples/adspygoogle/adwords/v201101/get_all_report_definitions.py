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

"""This example gets all report definitions. To add a report definition, run
add_keywords_performance_report.py.

Tags: ReportDefinitionService.get
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
report_definition_service = client.GetReportDefinitionService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct selector and get all report definitions.
selector = {}
report_definitions = report_definition_service.Get(selector)[0]

# Display results.
if 'entries' in report_definitions:
  for report_definition in report_definitions['entries']:
    print ('Report definition with name \'%s\' and id \'%s\' was found.'
           % (report_definition['reportName'], report_definition['id']))
else:
  print 'No report definitions were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
