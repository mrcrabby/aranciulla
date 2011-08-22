#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""This example adds a cross client (MCC) report.

To get report fields, run get_report_fields.py.

Tags: ReportDefinitionService.mutate
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import Utils


# NOTE: This should be run with the clientEmail set to the MCC.
# NOTE: This feature is still under development and subject to change.

# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
report_definition_service = client.GetReportDefinitionService(
    'https://adwords.google.com', 'v201101')

# Construct operations and create report definition.
operations = [{
    'operator': 'ADD',
    'operand': {
        'xsi_type': 'ReportDefinition',
        'reportName': 'MCC report example #%s' % Utils.GetUniqueName(),
        'dateRangeType': 'LAST_30_DAYS',
        'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
        'downloadFormat': 'XML',
        'crossClient': 'true',
        'selector': {
            'fields': ['AccountDescriptiveName', 'AdGroupId', 'Id',
                       'KeywordText', 'KeywordMatchType', 'Impressions',
                       'Clicks', 'Cost']
        }
    }
}]
report_definitions = report_definition_service.Mutate(operations)

# Display results.
for report_definition in report_definitions:
  print ('Report definition with name \'%s\' and id \'%s\' was added'
         % (report_definition['reportName'], report_definition['id']))

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
