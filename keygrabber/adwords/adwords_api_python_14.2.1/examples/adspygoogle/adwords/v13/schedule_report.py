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

"""This example schedules a DefinedReportJob.

Tags: ReportService.scheduleReportJob
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate constants and classes from the client library.
from adspygoogle.adwords import MIN_API_VERSION
from adspygoogle.common import SOAPPY
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize AdWordsClient object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Option 1: Schedule report job by calling "scheduleReportJob" method directly,
# bypassing library's validation logic. This way of scheduling report only works
# with SOAPpy toolkit.
#
# Construct report job.
if client.soap_lib == SOAPPY:
  job = ("""<aggregationTypes>%s</aggregationTypes>
<endDay>%s</endDay>
<name>%s</name>
<selectedColumns>%s</selectedColumns>
<selectedColumns>%s</selectedColumns>
<selectedColumns>%s</selectedColumns>
<selectedColumns>%s</selectedColumns>
<selectedReportType>%s</selectedReportType>
<startDay>%s</startDay>""" % ('Summary', '2009-01-31', 'Test Campaign Report',
                              'Campaign', 'CampaignId', 'CPC', 'CTR',
                              'Campaign', '2009-01-01'))
  from adspygoogle.common.soappy import SanityCheck
  job = SanityCheck.UnType(job)
  job._setAttr('xmlns:impl', ('https://adwords.google.com/api/adwords/%s'
                              % MIN_API_VERSION))
  job._setAttr('xsi:type', 'impl:DefinedReportJob')

  # Schedule report and get back report's job id.
  job_id = client.CallMethod(
      ('https://sandbox.google.com/api/adwords/%s/ReportService'
       % MIN_API_VERSION), 'scheduleReportJob', (job), None)[0]
  print 'Report job Id is \'%s\'' % job_id


# Option 2: Schedule report job while using library's validation logic.
#
# Construct report job.
job = {
    'aggregationTypes': ['Summary'],
    'endDay': '2009-01-31',
    'name': 'Test Campaign Report',
    'selectedColumns': ['Campaign', 'CampaignId', 'CPC', 'CTR'],
    'selectedReportType': 'Campaign',
    'startDay': '2009-01-01',
}

# Schedule report and get back report job id.
job_id = client.GetReportService(
    'https://sandbox.google.com', 'v13').ScheduleDefinedReportJob(job)[0]
print 'Report job Id is \'%s\'' % job_id

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
