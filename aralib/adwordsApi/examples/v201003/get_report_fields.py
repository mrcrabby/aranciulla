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

"""This example gets report fields.

Tags: ReportDefinitionService.getReportFields
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import sys
sys.path.append('../..')

# Import appropriate classes from the client library.
from aw_api.Client import Client


# Initialize client object.
client = Client(path='../..')

# Initialize appropriate service.
report_definition_service = client.GetReportDefinitionService(
    'https://adwords-sandbox.google.com', 'v201003')

report_type = 'INSERT_REPORT_TYPE_HERE'

# Get report fields.
fields = report_definition_service.GetReportFields(report_type)

# Display results.
print 'Report type \'%s\' contains the following fields:' % report_type
for field in fields:
  print ' - %s (%s)' % (field['fieldName'], field['fieldType'])
  if field['enumValues']:
    print '  := [%s]' % ', '.join(field['enumValues'])

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
