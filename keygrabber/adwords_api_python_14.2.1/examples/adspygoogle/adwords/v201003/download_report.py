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

"""This example gets and downloads a report from a report definition. To get a
report definition, run add_keywords_performance_report_definition.py. Currently,
there is only production support for report download."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
report_definition_service = client.GetReportDefinitionService(
    'https://adwords-sandbox.google.com', 'v201003')

report_definition_id = 'INSERT_REPORT_DEFINITION_ID'
file_name = 'INSERT_OUTPUT_FILE_NAME_HERE'

path = os.path.join(os.path.abspath('.'), file_name)

# Downlaod report.
data = report_definition_service.DownloadReport(report_definition_id)

# Save report to a data file.
fh = open(path, 'w')
try:
  fh.write(data)
finally:
  fh.close()

print ('Report with definition id \'%s\' was downloaded to \'%s\'.'
       % (report_definition_id, path))
