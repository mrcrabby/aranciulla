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

"""Validation and type conversion functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import cgi
import re

from aw_api import SanityCheck as glob_sanity_check
from aw_api.Errors import MissingPackageError
from aw_api.soappy_toolkit import MIN_SOAPPY_VERSION
try:
  import SOAPpy
except ImportError:
  msg = 'SOAPpy v%s or newer is required.' % MIN_SOAPPY_VERSION
  raise MissingPackageError(msg)
else:
  if (map(eval, SOAPpy.version.__version__.split('.')) <
      (list(map(eval, MIN_SOAPPY_VERSION.split('.'))))):
    msg = 'SOAPpy v%s or newer is required.' % MIN_SOAPPY_VERSION
    raise MissingPackageError(msg)


def UnType(item):
  """Convert given string into untyped type.

  Args:
    item: str string to untype.

  Returns:
    untypedType string converted into untypedType.
  """
  glob_sanity_check.ValidateTypes(((item, (str, unicode)),))

  # HTML encode non-complex strings. Complex strings would be XML snippets,
  # like <networkTypes>GoogleSearch</networkTypes>.
  pattern = re.compile('<.*>|</.*>')
  if pattern.search(item) is None:
    pattern = re.compile('&#(x\w{2,4}|\d{3});')
    result = pattern.findall(item)
    # Escape only ASCII characters.
    if not result:
      item = cgi.escape(item)

  return SOAPpy.Types.untypedType(item)


def IsUnTypedClass(obj):
  """Return True if a given object is of type SOAPpy.Types.untypedType, False
  otherwise.

  Args:
    obj: object an object to check.

  Returns:
    bool True if a given object is untyped, False otherwise.
  """
  return isinstance(obj, SOAPpy.Types.untypedType)


def ValidateAccountInfoV13(acct_info):
  """Validate AccountInfo object.

  Args:
    acct_info: dict AccountInfo object with updated values.
  """
  glob_sanity_check.ValidateTypes(((acct_info, dict),))
  for key in acct_info:
    if key == 'defaultNetworkTargeting':
      glob_sanity_check.ValidateTypes(((acct_info[key], list),))
      items = []
      for sub_key in acct_info[key]:
        glob_sanity_check.ValidateTypes(((sub_key, (str, unicode)),))
        items.append('<networkTypes>%s</networkTypes>' % sub_key)
      acct_info[key] = UnType(''.join(items))
    elif key == 'emailPromotionsPreferences':
      glob_sanity_check.ValidateTypes(((acct_info[key], dict),))
      for sub_key in acct_info[key]:
        glob_sanity_check.ValidateTypes(((acct_info[key][sub_key],
                                          (str, unicode)),))
        acct_info[key][sub_key] = UnType(acct_info[key][sub_key])
    else:
      glob_sanity_check.ValidateTypes(((acct_info[key], (str, unicode)),))


def ValidateLanguageTargetV13(language_target):
  """Validate LanguageTarget object.

  Args:
    language_target: list languages targeted by this entity.

  Returns:
    str languages targeted converted into str type.
  """
  glob_sanity_check.ValidateTypes(((language_target, list),))
  items = []
  for item in language_target:
    glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
    items.append('<languages>%s</languages>' % item)

  return ''.join(items)


def ValidateGeoTargetV13(geo_target):
  """Validate GeoTarget object.

  Args:
    geo_target: dict geographic targeting rules for this entity.

  Returns:
    str geographic targeting converted into str type.
  """
  glob_sanity_check.ValidateTypes(((geo_target, dict),))
  items = []
  for key in geo_target:
    if key == 'targetAll':
      glob_sanity_check.ValidateTypes(((geo_target[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, geo_target[key], key))
    elif key == 'cityTargets':
      glob_sanity_check.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        glob_sanity_check.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'countryTargets':
      glob_sanity_check.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        glob_sanity_check.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'metroTargets':
      glob_sanity_check.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        glob_sanity_check.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'regionTargets':
      glob_sanity_check.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        glob_sanity_check.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>%s</%s>' % (sub_key, item, sub_key))
      items.append('</%s>' % key)
    elif key == 'proximityTargets':
      glob_sanity_check.ValidateTypes(((geo_target[key], dict),))
      items.append('<%s>' % key)
      for sub_key in geo_target[key]:
        glob_sanity_check.ValidateTypes(((geo_target[key][sub_key], list),))
        for item in geo_target[key][sub_key]:
          items.append('<%s>' % sub_key)
          glob_sanity_check.ValidateTypes(((item, dict),))
          for sub_sub_key in item:
            glob_sanity_check.ValidateTypes(((item[sub_sub_key],
                                              (str, unicode)),))
            items.append('<%s>%s</%s>' % (sub_sub_key, item[sub_sub_key],
                                          sub_sub_key))
          items.append('</%s>' % sub_key)
      items.append('</%s>' % key)
    else:
      pass

  return ''.join(items)


def ValidateNetworkTargetV13(network_target):
  """Validate NetworkTarget object.

  Args:
    network_target: list advertising networks targeted by this entity.

  Returns:
    str adertising networks converted into str type.
  """
  glob_sanity_check.ValidateTypes(((network_target, list),))
  items = []
  for item in network_target:
    glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
    items.append('<networkTypes>%s</networkTypes>' % item)

  return ''.join(items)


def ValidateKeywordTrafficRequestV13(request):
  """Validate KeywordTrafficRequest object.

  Args:
    request: dict keyword traffic request.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  for key in request:
    glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))
    request[key] = UnType(request[key])


def ValidateKeywordRequestV13(request):
  """Validate KeywordRequest object.

  Args:
    request: dict keyword request.

  Returns:
    str keyword request converted into str type.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  items = []
  for key in request:
    glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))
    items.append('<%s>%s</%s>' % (key, request[key], key))

  return ''.join(items)


def ValidateAdGroupRequestV13(request):
  """Validate AdGroupRequest object.

  Args:
    request: dict ad group request.

  Returns:
    str ad group request converted into str type.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  items = []
  for key in request:
    if key == 'keywordRequests':
      items.append('<keywordRequests>')
      glob_sanity_check.ValidateTypes(((request[key], list),))
      for item in request[key]:
        items.append(ValidateKeywordRequestV13(item))
      items.append('</keywordRequests>')
    else:
      glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, request[key], key))

  return ''.join(items)


def ValidateCampaignRequestV13(request):
  """Validate CampaignRequest object.

  Args:
    request: dict campaign request.

  Returns:
    str campaign request converted into str type.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  items = []
  for key in request:
    if key == 'adGroupRequests':
      glob_sanity_check.ValidateTypes(((request[key], list),))
      items.append('<adGroupRequests>')
      for item in request[key]:
        items.append(ValidateAdGroupRequestV13(item))
      items.append('</adGroupRequests>')
    elif key == 'geoTargeting':
      glob_sanity_check.ValidateTypes(((request[key], dict),))
      items.append(('<geoTargeting>%s</geoTargeting>'
                    % ValidateGeoTargetV13(request[key])))
    elif key == 'id':
      glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, request[key], key))
    elif key == 'languageTargeting':
      glob_sanity_check.ValidateTypes(((request[key], list),))
      items.append('<%s>%s</%s>' % (key,
                                    ValidateLanguageTargetV13(request[key]),
                                    key))
    elif key == 'networkTargeting':
      glob_sanity_check.ValidateTypes(((request[key], list),))
      items.append('<%s>%s</%s>' % (key, ValidateNetworkTargetV13(request[key]),
                                    key))
    else:
      pass

  return ''.join(items)


def ValidateDefinedReportJobV13(job, name_space):
  """Validate DefinedReportJob object.

  Args:
    job: dict report job object.
    name_space: str namespace to use for this ReportJob.

  Returns:
    instance untyped instance of ReportJob.
  """
  items = []
  for key in job:
    if (key == 'adWordsType' or key == 'crossClient' or key == 'endDay' or
        key == 'includeZeroImpression' or key == 'keywordType' or
        key == 'name' or key == 'selectedReportType' or key == 'startDay'):
      glob_sanity_check.ValidateTypes(((job[key], (str, unicode)),))
      items.append('<%s>%s</%s>' % (key, job[key], key))
    else:
      glob_sanity_check.ValidateTypes(((job[key], list),))
      for item in job[key]:
        glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
        items.append('<%s>%s</%s>' % (key, item, key))
  # Explicitly set job's namespace and type.
  job = UnType(''.join(items))
  job._setAttr('xmlns:impl', name_space)
  job._setAttr('xsi3:type', 'impl:DefinedReportJob')

  return job


# TODO(api.sgrinberg): Add validation for Get/Mutate calls.
def ValidateOperation(operation):
  """Validate Operation object.

  Args:
    operation: dict operation object.
  """
  pass


def ValidateSelector(selector):
  """Validate Selector object.

  Args:
    selector: dict selector object.
  """
  pass


def ValidateBidLandscapeSelector(selector):
  """Validate BidLandscapeSelector object.

  Args:
    selector: dict BidLandscapeSelector object.
  """
  pass


def ValidateMedia(media):
  """Validate Media object.

  Args:
    media: dict Media object.
  """
  pass
