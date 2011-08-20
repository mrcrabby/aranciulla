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

"""Contains common constants for AdWords scripts."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os


API_TARGETS = [
    {
        'version': 'v13',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v13'),
        'server': 'https://adwords.google.com',
        'services': ('AccountService', 'ReportService',
                     'TrafficEstimatorService')
    },
    {
        'version': 'v200909',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v200909'),
        'group': 'cm',
        'server': 'https://adwords.google.com',
        'services': ('AdExtensionOverrideService', 'AdGroupAdService',
                     'AdGroupCriterionService', 'AdGroupService',
                     'AdParamService', 'CampaignAdExtensionService',
                     'CampaignCriterionService', 'CampaignService',
                     'CampaignTargetService', 'GeoLocationService')
    },
    {
        'version': 'v200909',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v200909'),
        'group': 'info',
        'server': 'https://adwords.google.com',
        'services': ('InfoService',)
    },
    {
        'version': 'v200909',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v200909'),
        'group': 'job',
        'server': 'https://adwords.google.com',
        'services': ('BulkMutateJobService',)
    },
    {
        'version': 'v200909',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v200909'),
        'group': 'o',
        'server': 'https://adwords.google.com',
        'services': ('TargetingIdeaService',)
    },
    {
        'version': 'v201003',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201003'),
        'group': 'cm',
        'server': 'https://adwords.google.com',
        'services': ('AdExtensionOverrideService', 'AdGroupAdService',
                     'AdGroupCriterionService', 'AdGroupService',
                     'AdParamService', 'BidLandscapeService',
                     'CampaignAdExtensionService', 'CampaignCriterionService',
                     'CampaignService', 'CampaignTargetService',
                     'GeoLocationService', 'MediaService',
                     'ReportDefinitionService')
    },
    {
        'version': 'v201003',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201003'),
        'group': 'job',
        'server': 'https://adwords.google.com',
        'services': ('BulkMutateJobService',)
    },
    {
        'version': 'v201003',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201003'),
        'group': 'info',
        'server': 'https://adwords.google.com',
        'services': ('InfoService',)
    },
    {
        'version': 'v201003',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201003'),
        'group': 'o',
        'server': 'https://adwords.google.com',
        'services': ('TargetingIdeaService',)
    },
    {
        'version': 'v201008',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201008'),
        'group': 'cm',
        'server': 'https://adwords.google.com',
        'services': ('AdExtensionOverrideService', 'AdGroupAdService',
                     'AdGroupCriterionService', 'AdGroupService',
                     'AdParamService', 'BidLandscapeService',
                     'CampaignAdExtensionService', 'CampaignCriterionService',
                     'CampaignService', 'CampaignTargetService',
                     'ExperimentService', 'GeoLocationService', 'MediaService',
                     'ReportDefinitionService', 'UserListService')
    },
    {
        'version': 'v201008',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201008'),
        'group': 'job',
        'server': 'https://adwords.google.com',
        'services': ('BulkMutateJobService',)
    },
    {
        'version': 'v201008',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201008'),
        'group': 'info',
        'server': 'https://adwords.google.com',
        'services': ('InfoService',)
    },
    {
        'version': 'v201008',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201008'),
        'group': 'o',
        'server': 'https://adwords.google.com',
        'services': ('TargetingIdeaService', 'TrafficEstimatorService')
    },
    {
        'version': 'v201008',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201008'),
        'group': 'ch',
        'server': 'https://adwords.google.com',
        'services': ('CustomerSyncService',)
    },
    {
        'version': 'v201008',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201008'),
        'group': 'mcm',
        'server': 'https://adwords.google.com',
        'services': ('AlertService', 'ServicedAccountService')
    },
    {
        'version': 'v201101',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201101'),
        'group': 'cm',
        'server': 'https://adwords.google.com',
        'services': ('AdExtensionOverrideService', 'AdGroupAdService',
                     'AdGroupCriterionService', 'AdGroupService',
                     'AdParamService', 'CampaignAdExtensionService',
                     'CampaignCriterionService', 'CampaignService',
                     'CampaignTargetService', 'ConversionTrackerService',
                     'DataService', 'ExperimentService',
                     'GeoLocationService', 'MediaService',
                     'ReportDefinitionService', 'UserListService')
    },
    {
        'version': 'v201101',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201101'),
        'group': 'job',
        'server': 'https://adwords.google.com',
        'services': ('BulkMutateJobService',)
    },
    {
        'version': 'v201101',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201101'),
        'group': 'info',
        'server': 'https://adwords.google.com',
        'services': ('InfoService',)
    },
    {
        'version': 'v201101',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201101'),
        'group': 'o',
        'server': 'https://adwords.google.com',
        'services': ('TargetingIdeaService', 'TrafficEstimatorService',
                     'BulkOpportunityService')
    },
    {
        'version': 'v201101',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201101'),
        'group': 'ch',
        'server': 'https://adwords.google.com',
        'services': ('CustomerSyncService',)
    },
    {
        'version': 'v201101',
        'location': os.path.join('..', '..', '..', 'adspygoogle', 'adwords',
                                 'zsi', 'v201101'),
        'group': 'mcm',
        'server': 'https://adwords.google.com',
        'services': ('AlertService', 'ServicedAccountService')
    }
]
