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

"""This example downloads a cross client (MCC) report.

To add a report, run add_mcc_report_definition.py.
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# NOTE: this should be run with the clientEmail set to the MCC.

# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
report_definition_service = client.GetReportDefinitionService(
    'https://adwords.google.com', 'v201101')

# Insert your own values here. If file_path is None, the report gets returned
# as a string.
file_path = ''
report_definition_id = 'INSERT_REPORT_DEFINITION_ID_HERE'

# Download the report - this call blocks.
print report_definition_service.DownloadMCCReport(report_definition_id,
                                                  file_path, True)
