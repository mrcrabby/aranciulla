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

"""This examples fetches existing campaigns using v200909 and schedules report
for active campaigns, using v13.

Tags: CampaignService.get, ReportService.scheduleDefinedReportJob
Api: AdWordsOnly
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate constants and classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize AdWordsClient object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Fetch existing campaigns.
print 'Fetching existing campaigns using v200909...'
selector = {'ids': []}
campaigns = client.GetCampaignService(
    'https://adwords-sandbox.google.com', 'v200909').Get(selector)
campaign_ids = []
for campaign in campaigns[0]['entries']:
  # We only care about active campaigns.
  if campaign['status'] not in ('DELETED', 'PAUSED'):
    campaign_ids.append(campaign['id'])
print 'Campaign ids: %s' % campaign_ids

# Construct report job.
job = {
    'aggregationTypes': ['Summary'],
    'campaigns': campaign_ids,
    'endDay': '2009-01-31',
    'name': 'Test Campaign Report',
    'selectedColumns': ['Campaign', 'CampaignId', 'CPC', 'CTR'],
    'selectedReportType': 'Campaign',
    'startDay': '2009-01-01',
}

# Schedule report and get back report job id.
print 'Scheduling report job using v13...'
report_service = client.GetReportService('https://sandbox.google.com', 'v13')
job_id = report_service.ScheduleDefinedReportJob(job)[0]
print 'Report job id is \'%s\'.' % job_id

print 'Downloading report using v13...'
print report_service.DownloadXmlReport(job_id)

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
