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

"""Validation and type conversion functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.zsi import SanityCheck as ZsiSanityCheck


def ValidateAccountInfoV13(acct_info):
  """Validate AccountInfo object.

  Args:
    acct_info: dict AccountInfo object.
  """
  SanityCheck.ValidateTypes(((acct_info, dict),))
  for key in acct_info:
    if key in ('defaultNetworkTargeting',):
      SanityCheck.ValidateTypes(((acct_info[key], list),))
      network_types = []
      for sub_key in acct_info[key]:
        SanityCheck.ValidateTypes(((sub_key, (str, unicode)),))
        network_types.append(sub_key)
      acct_info[key] = {'networkTypes': network_types}
    elif key in ('emailPromotionsPreferences',):
      SanityCheck.ValidateTypes(((acct_info[key], dict),))
      for sub_key in acct_info[key]:
        SanityCheck.ValidateTypes(
            ((acct_info[key][sub_key], (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((acct_info[key], (str, unicode)),))


def ValidateDefinedReportJobV13(job, web_services):
  """Validate DefinedReportJob object.

  Args:
    job: dict DefinedReportJob object.
    web_services: module Web services.

  Returns:
    DefinedReportJob instance.
  """
  report_type = ZsiSanityCheck.GetPyClass('DefinedReportJob', web_services)
  new_job = report_type()
  for key in job:
    if job[key] == 'None': continue
    if key in ('adGroups', 'adGroupStatuses', 'aggregationTypes', 'campaigns',
               'campaignStatuses', 'clientEmails', 'keywords',
               'keywordStatuses', 'selectedColumns'):
      SanityCheck.ValidateTypes(((job[key], list),))
      for item in job[key]:
        SanityCheck.ValidateTypes(((item, (str, unicode)),))
    else:
      SanityCheck.ValidateTypes(((job[key], (str, unicode)),))
    new_job.__dict__.__setitem__('_%s' % key, job[key])
  return new_job


def ValidateKeywordTrafficRequestV13(request):
  """Validate KeywordTrafficRequest object.

  Args:
    request: dict KeywordTrafficRequest object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    SanityCheck.ValidateTypes(((request[key], (str, unicode)),))


def ValidateGeoTargetV13(target):
  """Validate GeoTarget object.

  Args:
    target: dict GeoTarget object.

  Returns:
    dict Updated GeoTarget object.
  """
  SanityCheck.ValidateTypes(((target, dict),))
  for key in target:
    if target[key] == 'None': continue
    if key in ('targetAll',):
      SanityCheck.ValidateTypes(((target[key], (str, unicode)),))
      data = target[key]
    else:
      SanityCheck.ValidateTypes(((target[key], dict),))
      geo_target = target[key]
      for sub_key in geo_target:
        SanityCheck.ValidateTypes(((geo_target[sub_key], list),))
        for item in geo_target[sub_key]:
          if sub_key in ('circles',):
            circle = {}
            for sub_sub_key in item:
              SanityCheck.ValidateTypes(((item[sub_sub_key],
                                          (str, unicode)),))
              circle[sub_sub_key] = item[sub_sub_key]
            item = circle
          else:
            SanityCheck.ValidateTypes(((item, (str, unicode)),))
        # If value is an empty list, remove key from the dictionary.
        if not geo_target[sub_key]:
          geo_target = Utils.UnLoadDictKeys(geo_target, [sub_key])
      data = geo_target
    target[key] = data
  return target


def ValidateLanguageTargetV13(targets):
  """Validate LanguageTarget object.

  Args:
    targets: list LanguageTarget objects.

  Returns:
    list Updated LanguageTarget objects.
  """
  SanityCheck.ValidateTypes(((targets, list),))
  languages = []
  for item in targets:
    SanityCheck.ValidateTypes(((item, (str, unicode)),))
    languages.append({'languages': item})
  return languages


def ValidateNetworkTargetV13(targets):
  """Validate NetworkTarget object.

  Args:
    targets: list NetworkTarget objects.

  Returns:
    list Updated NetworkTarget objects.
  """
  SanityCheck.ValidateTypes(((targets, list),))
  networks = []
  for item in targets:
    SanityCheck.ValidateTypes(((item, (str, unicode)),))
    networks.append({'networkTypes': item})
  return networks


def ValidateCampaignRequestV13(request):
  """Validate CampaignRequest object.

  Args:
    request: dict CampaignRequest object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    if key in ('adGroupRequests',):
      SanityCheck.ValidateTypes(((request[key], list),))
      for item in request[key]:
        ValidateAdGroupRequestV13(item)
    elif key in ('geoTargeting',):
      request[key] = ValidateGeoTargetV13(request[key])
    elif key in ('languageTargeting',):
      request[key] = ValidateLanguageTargetV13(request[key])
    elif key in ('networkTargeting',):
      request[key] = ValidateNetworkTargetV13(request[key])
    else:
      SanityCheck.ValidateTypes(((request[key], (str, unicode)),))


def ValidateAdGroupRequestV13(request):
  """Validate AdGroupRequest object.

  Args:
    request: dict AdGroupRequest object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    if key in ('keywordRequests',):
      SanityCheck.ValidateTypes(((request[key], list),))
      for item in request[key]:
        ValidateKeywordRequestV13(item)
    else:
      SanityCheck.ValidateTypes(((request[key], (str, unicode)),))


def ValidateKeywordRequestV13(request):
  """Validate KeywordRequest object.

  Args:
    request: dict KeywordRequest object.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    SanityCheck.ValidateTypes(((request[key], (str, unicode)),))
