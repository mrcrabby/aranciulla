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
from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck


def ValidateAccountInfoV13(acct_info):
  """Validate AccountInfo object.

  Args:
    acct_info: dict AccountInfo object with updated values.
  """
  SanityCheck.ValidateTypes(((acct_info, dict),))
  for key in acct_info:
    if key == 'defaultNetworkTargeting':
      SanityCheck.ValidateTypes(((acct_info[key], list),))
      items = []
      for sub_key in acct_info[key]:
        SanityCheck.ValidateTypes(((sub_key, (str, unicode)),))
        items.append('<networkTypes>%s</networkTypes>' % sub_key)
      acct_info[key] = SoappySanityCheck.UnType(''.join(items))
    elif key == 'emailPromotionsPreferences':
      SanityCheck.ValidateTypes(((acct_info[key], dict),))
      for sub_key in acct_info[key]:
        SanityCheck.ValidateTypes(((acct_info[key][sub_key], (str, unicode)),))
        acct_info[key][sub_key] = SoappySanityCheck.UnType(
            acct_info[key][sub_key])
    else:
      SanityCheck.ValidateTypes(((acct_info[key], (str, unicode)),))


def ValidateDefinedReportJobV13(job, name_space):
  """Validate DefinedReportJob object.

  Args:
    job: dict report job object.
    name_space: str namespace to use for this ReportJob.

  Returns:
    instance Untyped instance of the defined report job.
  """
  items = []
  for key in job:
    if (key == 'adWordsType' or key == 'crossClient' or key == 'endDay' or
        key == 'includeZeroImpression' or key == 'keywordType' or
        key == 'name' or key == 'selectedReportType' or key == 'startDay'):
      SanityCheck.ValidateTypes(((job[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, job[key], key))
    else:
      SanityCheck.ValidateTypes(((job[key], list),))
      for item in job[key]:
        SanityCheck.ValidateTypes(((item, (str, unicode)),))
        items.append('<%s>%s</%s>' % (key, item, key))
  # Explicitly set job's namespace and type.
  job = SoappySanityCheck.UnType(''.join(items))
  job._setAttr('xmlns:impl', name_space)
  job._setAttr('xsi3:type', 'impl:DefinedReportJob')
  return job


def ValidateKeywordTrafficRequestV13(request):
  """Validate KeywordTrafficRequest object.

  Args:
    request: dict keyword traffic request.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  for key in request:
    SanityCheck.ValidateTypes(((request[key], (str, unicode)),))
    request[key] = SoappySanityCheck.UnType(request[key])


def ValidateGeoTargetV13(geo_target):
  """Validate GeoTarget object.

  Args:
    geo_target: dict Geographic targeting rules for this entity.

  Returns:
    str Geographic targeting converted into str type.
  """
  SanityCheck.ValidateTypes(((geo_target, dict),))
  items = []
  for key in geo_target:
    if key == 'targetAll':
      SanityCheck.ValidateTypes(((geo_target[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, geo_target[key], key))
    elif key == 'cityTargets':
      SanityCheck.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        SanityCheck.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'countryTargets':
      SanityCheck.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        SanityCheck.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'metroTargets':
      SanityCheck.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        SanityCheck.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'regionTargets':
      SanityCheck.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        SanityCheck.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'proximityTargets':
      SanityCheck.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        SanityCheck.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>' % sub_key)
          SanityCheck.ValidateTypes(((item, dict),))
          for sub_sub_key in item:
            SanityCheck.ValidateTypes(((item[sub_sub_key], (str, unicode)),))
            items.append('<%s>%s</%s>' % (sub_sub_key, item[sub_sub_key],
                                          sub_sub_key))
          items.append('</%s>' % sub_key)
      items.append('</%s>' % key)
  return ''.join(items)


def ValidateLanguageTargetV13(language_target):
  """Validate LanguageTarget object.

  Args:
    language_target: list Languages targeted by this entity.

  Returns:
    str Languages targeted converted into str type.
  """
  SanityCheck.ValidateTypes(((language_target, list),))
  items = []
  for item in language_target:
    SanityCheck.ValidateTypes(((item, (str, unicode)),))
    items.append('<languages>%s</languages>' % item)
  return ''.join(items)


def ValidateNetworkTargetV13(network_target):
  """Validate NetworkTarget object.

  Args:
    network_target: list Advertising networks targeted by this entity.

  Returns:
    str Adertising networks converted into str type.
  """
  SanityCheck.ValidateTypes(((network_target, list),))
  items = []
  for item in network_target:
    SanityCheck.ValidateTypes(((item, (str, unicode)),))
    items.append('<networkTypes>%s</networkTypes>' % item)
  return ''.join(items)


def ValidateCampaignRequestV13(request):
  """Validate CampaignRequest object.

  Args:
    request: dict Campaign request.

  Returns:
    str Campaign request converted into str type.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  items = []
  for key in request:
    if key == 'adGroupRequests':
      SanityCheck.ValidateTypes(((request[key], list),))
      items.append('<adGroupRequests>')
      for item in request[key]:
        items.append(ValidateAdGroupRequestV13(item))
      items.append('</adGroupRequests>')
    elif key == 'geoTargeting':
      SanityCheck.ValidateTypes(((request[key], dict),))
      items.append(('<geoTargeting>%s</geoTargeting>'
                    % ValidateGeoTargetV13(request[key])))
    elif key == 'id':
      SanityCheck.ValidateTypes(((request[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, request[key], key))
    elif key == 'languageTargeting':
      SanityCheck.ValidateTypes(((request[key], list),))
      items.append('<%s>%s</%s>' % (key,
                                    ValidateLanguageTargetV13(request[key]),
                                    key))
    elif key == 'networkTargeting':
      SanityCheck.ValidateTypes(((request[key], list),))
      items.append('<%s>%s</%s>' % (key, ValidateNetworkTargetV13(request[key]),
                                    key))
  return ''.join(items)


def ValidateAdGroupRequestV13(request):
  """Validate AdGroupRequest object.

  Args:
    request: dict ad group request.

  Returns:
    str ad group request converted into str type.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  items = []
  for key in request:
    if key == 'keywordRequests':
      items.append('<keywordRequests>')
      SanityCheck.ValidateTypes(((request[key], list),))
      for item in request[key]:
        items.append(ValidateKeywordRequestV13(item))
      items.append('</keywordRequests>')
    else:
      SanityCheck.ValidateTypes(((request[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, request[key], key))
  return ''.join(items)


def ValidateKeywordRequestV13(request):
  """Validate KeywordRequest object.

  Args:
    request: dict keyword request.

  Returns:
    str keyword request converted into str type.
  """
  SanityCheck.ValidateTypes(((request, dict),))
  items = []
  for key in request:
    SanityCheck.ValidateTypes(((request[key], (str, unicode)),))
    items.append('<%s>%s</%s>' % (key, request[key], key))
  return ''.join(items)
