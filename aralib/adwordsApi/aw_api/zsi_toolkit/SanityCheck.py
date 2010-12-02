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

from aw_api import MAX_TARGET_NAMESPACE
from aw_api import Utils
from aw_api import SanityCheck as glob_sanity_check
from aw_api.Errors import ValidationError


def GetPyClass(name, web_services):
  """Return Python class for a given class name.

  Args:
    name: str name of the Python class to return.
    web_services: module for web service.

  Returns:
    Python class.
  """
  for index in xrange(MAX_TARGET_NAMESPACE):
    try:
      pyclass = eval('web_services.ns%s.%s_Def(\'%s\').pyclass' % (index, name,
                                                                   name))
      break
    except AttributeError:
      if index == MAX_TARGET_NAMESPACE - 1:
        version = web_services.__dict__['__name__'].split('.')[2]
        msg = ('Given API version, %s, is not compatible with \'%s\' class.' %
               (version, name))
        raise ValidationError(msg)

  return pyclass


def IsPyClass(obj):
  """Return True if a given object is a Python class, False otherwise.

  Args:
    obj: object an object to check.

  Returns:
    bool True if a given object is a Python class, False otherwise.
  """
  if (hasattr(obj, 'typecode') and
      str(obj.typecode.pyclass).find('_Holder') > -1):
    return True
  return False


def ValidateAccountInfoV13(acct_info):
  """Validate AccountInfo object.

  Args:
    acct_info: dict AccountInfo object.
  """
  glob_sanity_check.ValidateTypes(((acct_info, dict),))
  for key in acct_info:
    if key in ('defaultNetworkTargeting',):
      glob_sanity_check.ValidateTypes(((acct_info[key], list),))
      network_types = []
      for sub_key in acct_info[key]:
        glob_sanity_check.ValidateTypes(((sub_key, (str, unicode)),))
        network_types.append(sub_key)
      acct_info[key] = {'networkTypes': network_types}
    elif key in ('emailPromotionsPreferences',):
      glob_sanity_check.ValidateTypes(((acct_info[key], dict),))
      for sub_key in acct_info[key]:
        glob_sanity_check.ValidateTypes(
            ((acct_info[key][sub_key], (str, unicode)),))
    else:
      glob_sanity_check.ValidateTypes(((acct_info[key], (str, unicode)),))


def ValidateLanguageTargetV13(targets):
  """Validate LanguageTarget object.

  Args:
    targets: list LanguageTarget objects.

  Returns:
    list updated LanguageTarget objects.
  """
  glob_sanity_check.ValidateTypes(((targets, list),))
  languages = []
  for item in targets:
    glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
    languages.append({'languages': item})

  return languages


def ValidateGeoTargetV13(target):
  """Validate GeoTarget object.

  Args:
    target: dict GeoTarget object.

  Returns:
    dict updated GeoTarget object.
  """
  glob_sanity_check.ValidateTypes(((target, dict),))
  for key in target:
    if target[key] == 'None': continue
    if key in ('targetAll',):
      glob_sanity_check.ValidateTypes(((target[key], (str, unicode)),))
      data = target[key]
    else:
      glob_sanity_check.ValidateTypes(((target[key], dict),))
      geo_target = target[key]
      for sub_key in geo_target:
        glob_sanity_check.ValidateTypes(((geo_target[sub_key], list),))
        for item in geo_target[sub_key]:
          if sub_key in ('circles',):
            circle = {}
            for sub_sub_key in item:
              glob_sanity_check.ValidateTypes(((item[sub_sub_key],
                                                (str, unicode)),))
              circle[sub_sub_key] = item[sub_sub_key]
            item = circle
          else:
            glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
        # If value is an empty list, remove key from the dictionary.
        if not geo_target[sub_key]:
          geo_target = Utils.UnLoadDictKeys(geo_target, [sub_key])
      data = geo_target
    target[key] = data

  return target


def ValidateNetworkTargetV13(targets):
  """Validate NetworkTarget object.

  Args:
    targets: list NetworkTarget objects.

  Returns:
    list updated NetworkTarget objects.
  """
  glob_sanity_check.ValidateTypes(((targets, list),))
  networks = []
  for item in targets:
    glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
    networks.append({'networkTypes': item})

  return networks


def ValidateKeywordTrafficRequestV13(request):
  """Validate KeywordTrafficRequest object.

  Args:
    request: dict KeywordTrafficRequest object.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  for key in request:
    glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))


def ValidateKeywordRequestV13(request):
  """Validate KeywordRequest object.

  Args:
    request: dict KeywordRequest object.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  for key in request:
    glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))


def ValidateAdGroupRequestV13(request):
  """Validate AdGroupRequest object.

  Args:
    request: dict AdGroupRequest object.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  for key in request:
    if key in ('keywordRequests',):
      glob_sanity_check.ValidateTypes(((request[key], list),))
      for item in request[key]:
        ValidateKeywordRequestV13(item)
    else:
      glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))


def ValidateCampaignRequestV13(request):
  """Validate CampaignRequest object.

  Args:
    request: dict CampaignRequest object.
  """
  glob_sanity_check.ValidateTypes(((request, dict),))
  for key in request:
    if key in ('adGroupRequests',):
      glob_sanity_check.ValidateTypes(((request[key], list),))
      for item in request[key]:
        ValidateAdGroupRequestV13(item)
    elif key in ('geoTargeting',):
      request[key] = ValidateGeoTargetV13(request[key])
    elif key in ('languageTargeting',):
      request[key] = ValidateLanguageTargetV13(request[key])
    elif key in ('networkTargeting',):
      request[key] = ValidateNetworkTargetV13(request[key])
    else:
      glob_sanity_check.ValidateTypes(((request[key], (str, unicode)),))


def ValidateDefinedReportJobV13(job, web_services):
  """Validate DefinedReportJob object.

  Args:
    job: dict DefinedReportJob object.
    web_services: module for web services.

  Returns:
    DefinedReportJob instance.
  """
  report_type = GetPyClass('DefinedReportJob', web_services)
  new_job = report_type()
  for key in job:
    if job[key] == 'None': continue
    if key in ('adGroups', 'adGroupStatuses', 'aggregationTypes', 'campaigns',
               'campaignStatuses', 'clientEmails', 'keywords',
               'keywordStatuses', 'selectedColumns'):
      glob_sanity_check.ValidateTypes(((job[key], list),))
      for item in job[key]:
        glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
    else:
      glob_sanity_check.ValidateTypes(((job[key], (str, unicode)),))
    new_job.__dict__.__setitem__('_%s' % key, job[key])

  return new_job


def ValidateImage(image, web_services):
  """Validate Image object.

  Args:
    image: dict Image object.
    web_services: module for web services.

  Returns:
    Image instance.
  """
  if IsPyClass(image):
    return image

  glob_sanity_check.ValidateTypes(((image, dict),))
  new_image = GetPyClass('Image', web_services)
  for key in image:
    if image[key] == 'None': continue
    if key in ('dimensions',):
      glob_sanity_check.ValidateTypes(((image[key], list),))
      dimensions = []
      for item in image[key]:
        dimensions.append(ValidateMapEntry(item,
                                           'Media_Size_DimensionsMapEntry',
                                           web_services))
      data = dimensions
    elif key in ('urls',):
      glob_sanity_check.ValidateTypes(((image[key], list),))
      urls = []
      for item in image[key]:
        urls.append(ValidateMapEntry(item,
                                     'Media_Size_StringMapEntry',
                                     web_services))
      data = urls
    elif key in ('extendedCapabilities',):
      glob_sanity_check.ValidateTypes(((image[key], list),))
      capabilities = []
      for item in image[key]:
        capabilities.append(ValidateMapEntry(item,
                                             'Media_MediaExtendedCapabilityType_Media_MediaExtendedCapabilityStateMapEntry',
                                             web_services))
      data = capabilities
    else:
      glob_sanity_check.ValidateTypes(((image[key], (str, unicode)),))
      data = image[key]
    new_image.__dict__.__setitem__('_%s' % key, data)

  return new_image


def ValidateDimensions(dimensions, web_services):
  """Validate Dimensions object.

  Args:
    dimensions: dict Dimensions object.
    web_services: module for web services.

  Returns:
    Dimensions instance.
  """
  if IsPyClass(dimensions):
    return dimensions

  glob_sanity_check.ValidateTypes(((dimensions, dict),))
  new_dimensions = GetPyClass('Dimensions', web_services)
  for key in dimensions:
    if dimensions[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((dimensions[key], (str, unicode)),))
    new_dimensions.__dict__.__setitem__('_%s' % key, dimensions[key])

  return new_dimensions


def ValidateMapEntry(entry, type, web_services):
  """Validate MapEntry object.

  MapEntry object is one of Media_MediaExtendedCapabilityType_Media_MediaExtendedCapabilityStateMapEntry,
  Media_Size, Media_Size_StringMapEntry, Type_AttributeMapEntry.

  Args:
    entry: dict MapEntry object.
    web_services: module for web services.

  Returns:
    XxxMapEntry instance.
  """
  if IsPyClass(entry):
    return entry

  glob_sanity_check.ValidateTypes(((entry, dict),))
  new_entry = GetPyClass(type, web_services)
  for key in entry:
    if entry[key] == 'None': continue
    if type in ('Media_Size_DimensionsMapEntry',) and key in ('value',):
      data = ValidateDimensions(entry[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((entry[key], (str, unicode)),))
      data = entry[key]
    new_entry.__dict__.__setitem__('_%s' % key, data)

  return new_entry


def ValidateVideo(video, web_services):
  """Validate Video object.

  Args:
    image: dict Video object.
    web_services: module for web services.

  Returns:
    Video instance.
  """
  if IsPyClass(video):
    return video

  glob_sanity_check.ValidateTypes(((video, dict),))
  new_video = GetPyClass('Video', web_services)
  for key in video:
    if video[key] == 'None': continue
    if key in ('dimensions',):
      glob_sanity_check.ValidateTypes(((video[key], list),))
      dimensions = []
      for item in video[key]:
        dimensions.append(ValidateMapEntry(item,
                                           'Media_Size_DimensionsMapEntry',
                                           web_services))
      data = dimensions
    elif key in ('urls',):
      glob_sanity_check.ValidateTypes(((video[key], list),))
      urls = []
      for item in video[key]:
        urls.append(ValidateMapEntry(item,
                                     'Media_Size_StringMapEntry',
                                     web_services))
      data = urls
    elif key in ('extendedCapabilities',):
      glob_sanity_check.ValidateTypes(((video[key], list),))
      capabilities = []
      for item in video[key]:
        capabilities.append(ValidateMapEntry(item,
                                             'Media_MediaExtendedCapabilityType_Media_MediaExtendedCapabilityStateMapEntry',
                                             web_services))
      data = capabilities
    else:
      glob_sanity_check.ValidateTypes(((video[key], (str, unicode)),))
      data = video[key]
    new_video.__dict__.__setitem__('_%s' % key, data)

  return new_video


def ValidateAudio(audio, web_services):
  """Validate Audio object.

  Args:
    audio: dict Audio object.
    web_services: module for web services.

  Returns:
    Audio instance.
  """
  if IsPyClass(audio):
    return audio

  glob_sanity_check.ValidateTypes(((audio, dict),))
  new_audio = GetPyClass('Audio', web_services)
  for key in audio:
    if audio[key] == 'None': continue
    if key in ('dimensions',):
      glob_sanity_check.ValidateTypes(((audio[key], list),))
      dimensions = []
      for item in audio[key]:
        dimensions.append(ValidateMapEntry(item,
                                           'Media_Size_DimensionsMapEntry',
                                           web_services))
      data = dimensions
    elif key in ('urls',):
      glob_sanity_check.ValidateTypes(((audio[key], list),))
      urls = []
      for item in audio[key]:
        urls.append(ValidateMapEntry(item,
                                     'Media_Size_StringMapEntry',
                                     web_services))
      data = urls
    elif key in ('extendedCapabilities',):
      glob_sanity_check.ValidateTypes(((audio[key], list),))
      capabilities = []
      for item in audio[key]:
        capabilities.append(ValidateMapEntry(item,
                                             'Media_MediaExtendedCapabilityType_Media_MediaExtendedCapabilityStateMapEntry',
                                             web_services))
      data = capabilities
    else:
      glob_sanity_check.ValidateTypes(((audio[key], (str, unicode)),))
      data = audio[key]
    new_audio.__dict__.__setitem__('_%s' % key, data)

  return new_audio


def ValidateTemplateElement(element, web_services):
  """Validate TemplateElement object.

  Args:
    element: dict TemplateElement object.
    web_services: module for web services.

  Returns:
    TemplateElement instance.
  """
  if IsPyClass(element):
    return element

  glob_sanity_check.ValidateTypes(((element, dict),))
  new_element = GetPyClass('TemplateElement', web_services)
  for key in element:
    if element[key] == 'None': continue
    if key in ('fields',):
      glob_sanity_check.ValidateTypes(((element[key], list),))
      fields = []
      for item in element[key]:
        fields.append(ValidateTemplateElementField(item, web_services))
      data = fields
    else:
      glob_sanity_check.ValidateTypes(((element[key], (str, unicode)),))
      data = element[key]
    new_element.__dict__.__setitem__('_%s' % key, data)

  return new_element


def ValidateMedia(media, web_services):
  """Validate Media object.

  Media object is on of Image, Video.

  Args:
    field: dict media object.
    web_services: module for web services.

  Returns:
    Media updated media object.
  """
  if 'data' in media:
    new_media = ValidateImage(media, web_services)
  else:
    new_media = ValidateVideo(media, web_services)

  return new_media


def ValidateTemplateElementField(field, web_services):
  """Validate TemplateElementField object.

  Args:
    field: dict TemplateElementField object.
    web_services: module for web services.

  Returns:
    TemplateElementField instance.
  """
  if IsPyClass(field):
    return field

  glob_sanity_check.ValidateTypes(((field, dict),))
  new_field = GetPyClass('TemplateElementField', web_services)
  for key in field:
    if field[key] == 'None': continue
    if key in ('fieldMedia',):
      data = ValidateMedia(field[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((field[key], (str, unicode)),))
      data = field[key]
    new_field.__dict__.__setitem__('_%s' % key, data)

  return new_field


def ValidateAd(operator, ad, web_services):
  """Validate Ad object.

  An Ad object is one of DeprecatedAd, MobileAd, MobileImageAd, ImageAd,
  LocalBusinessAd, TemplateAd, TextAd,

  Args:
    operator: str operator to use.
    ad: dict ad object.
    web_services: module for web services.

  Returns:
    dict/Ad updated ad object or Ad instance.
  """
  if IsPyClass(ad):
    return ad

  glob_sanity_check.ValidateTypes(((ad, dict),))
  if operator in ('ADD', ''):
    if 'adType' in ad:
      new_ad = GetPyClass(ad['adType'], web_services)
    elif 'type' in ad:
      new_ad = GetPyClass(ad['type'], web_services)
    elif 'Ad_Type' in ad:
      new_ad = GetPyClass(ad['Ad_Type'], web_services)
    else:
      msg = 'The \'adType\' or \'type\' of the ad is missing.'
      raise ValidationError(msg)
  elif operator in ('SET', 'REMOVE'):
    new_ad = GetPyClass('Ad', web_services)
  for key in ad:
    if ad[key] == 'None': continue
    if key in ('productImage', 'image', 'businessImage', 'customIcon', 'icon'):
      data = ValidateImage(ad[key], web_services)
    elif key in ('video',):
      data = ValidateVideo(ad[key], web_services)
    elif key in ('markupLanguages', 'mobileCarriers'):
      glob_sanity_check.ValidateTypes(((ad[key], list),))
      for item in ad[key]:
        glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
      data = ad[key]
    elif key in ('target',):
      data = ValidateProximityTarget(ad[key], web_services)
    elif key in ('adUnionId',):
      data = ValidateEntityId(ad[key], 'AdUnionId', web_services)
    elif key in ('templateElements',):
      glob_sanity_check.ValidateTypes(((ad[key], list),))
      elements = []
      for item in ad[key]:
        elements.append(ValidateTemplateElement(item, web_services))
      data = elements
    elif key in ('dimensions',):
      data = ValidateDimensions(ad[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((ad[key], (str, unicode)),))
      data = ad[key]
    new_ad.__dict__.__setitem__('_%s' % key, data)

  return new_ad


def ValidateProximityTarget(target, web_services):
  """Validate ProximityTarget object.

  Args:
    target: dict ProximityTarget object.
    web_services: module for web services.

  Returns:
    ProximityTarget instance.
  """
  if IsPyClass(target):
    return target

  glob_sanity_check.ValidateTypes(((target, dict),))
  new_target = GetPyClass('ProximityTarget', web_services)
  for key in target:
    if target[key] == 'None': continue
    if key in ('geoPoint',):
      data = ValidateGeoPoint(target[key], web_services)
    elif key in ('address',):
      data = ValidateAddress(target[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((target[key], (str, unicode)),))
      data = target[key]
    new_target.__dict__.__setitem__('_%s' % key, data)

  return new_target


def ValidateCriterion(operator, criterion, web_services):
  """Validate Criterion object.

  A Criterion object is one of Keyword, Website, Placement.

  Args:
    operator: str operator to use.
    criterion: dict Criterion object.
    web_services: module for web services.

  Returns:
    dict/Criterion updated criterion object or Criterion instance.
  """
  if IsPyClass(criterion):
    return criterion

  glob_sanity_check.ValidateTypes(((criterion, dict),))
  if operator in ('ADD', ''):
    if 'criterionType' in criterion:
      new_criterion = GetPyClass(criterion['criterionType'], web_services)
    elif 'type' in criterion:
      new_criterion = GetPyClass(criterion['type'], web_services)
    elif 'Criterion_Type' in criterion:
      new_criterion = GetPyClass(criterion['Criterion_Type'], web_services)
    else:
      msg = 'The \'criterionType\' or \'type\' of the criterion is missing.'
      raise ValidationError(msg)
  elif operator in ('SET', 'REMOVE'):
    new_criterion = GetPyClass('Criterion', web_services)
  for key in criterion:
    if criterion[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((criterion[key], (str, unicode)),))
    new_criterion.__dict__.__setitem__('_%s' % key, criterion[key])

  return new_criterion


def ValidateDateRange(range, web_services):
  """Validate DateRange object.

  Args:
    range: dict DateRange object.
    web_services: module for web services.

  Returns:
    DateRange instance.
  """
  if IsPyClass(range):
    return range

  glob_sanity_check.ValidateTypes(((range, dict),))
  new_range = GetPyClass('DateRange', web_services)
  for key in range:
    if range[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((range[key], (str, unicode)),))
    new_range.__dict__.__setitem__('_%s' % key, range[key])

  return new_range

def ValidateMoney(amount, web_services):
  """Validate Money object.

  Args:
    amount: dict Money object.
    web_services: module for web services.

  Returns:
    Money instance.
  """
  if IsPyClass(amount):
    return amount

  glob_sanity_check.ValidateTypes(((amount, dict),))
  money = GetPyClass('Money', web_services)
  for key in amount:
    if amount[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((amount[key], (str, unicode)),))
    money.__dict__.__setitem__('_%s' % key, amount[key])

  return money


def ValidateBudget(budget, web_services):
  """Validate Budget object.

  Args:
    budget: dict Budget object.

  Returns:
    Budget instance.
  """
  if IsPyClass(budget):
    return budget

  glob_sanity_check.ValidateTypes(((budget, dict),))
  new_budget = GetPyClass('Budget', web_services)
  for key in budget:
    if budget[key] == 'None': continue
    if key in ('amount',):
      budget[key] = ValidateMoney(budget[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((budget[key], (str, unicode)),))
    new_budget.__dict__.__setitem__('_%s' % key, budget[key])

  return new_budget


def ValidateBid(bid, web_services):
  """Validate Bid object.

  Args:
    bid: dict Bid object.
    web_services: module for web services.

  Returns:
    Bid instance.
  """
  if IsPyClass(bid):
    return bid

  glob_sanity_check.ValidateTypes(((bid, dict),))
  new_bid = GetPyClass('Bid', web_services)
  for key in bid:
    if bid[key] == 'None': continue
    if key in ('amount',):
      data = ValidateMoney(bid[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((bid[key], (str, unicode)),))
      data = bid[key]
    new_bid.__dict__.__setitem__('_%s' % key, data)

  return new_bid


def ValidateBids(bids, web_services):
  """Validate Bids object.

  A Bids object is on of AdGroupBids, AdGroupCriterionBids,
  BudgetOptimizerAdGroupBids, BudgetOptimizerAdGroupCriterionBids,
  ConversionOptimizerAdGroupBids, ConversionOptimizerAdGroupCriterionBids,
  ManualCPCAdGroupBids, ManualCPCAdGroupCriterionBids, ManualCPMAdGroupBids,
  ManualCPMAdGroupCriterionBids, PositionPreferenceAdGroupCriterionBids.

  Args:
    bids: dict Bids object.
    web_services: module for web services.

  Returns:
    XxxBids instance.
  """
  if IsPyClass(bids):
    return bids

  glob_sanity_check.ValidateTypes(((bids, dict),))
  if 'type' in bids:
    new_bids = GetPyClass(bids['type'], web_services)
  elif 'AdGroupBids_Type' in bids:
    new_bids = GetPyClass(bids['AdGroupBids_Type'], web_services)
  elif 'AdGroupCriterionBids_Type' in bids:
    new_bids = GetPyClass(bids['AdGroupCriterionBids_Type'], web_services)
  else:
    msg = 'The \'type\' of the bid is missing.'
    raise ValidationError(msg)
  for key in bids:
    if bids[key] == 'None': continue
    if key in ('proxyBid', 'maxCpc', 'maxCpm', 'proxyMaxCpc',
               'proxyKeywordMaxCpc', 'proxySiteMaxCpc', 'targetCpa',
               'keywordMaxCpc', 'keywordContentMaxCpc', 'siteMaxCpc',
               'targetCpa'):
      data = ValidateBid(bids[key], web_services)
    elif key in ('positionPreferenceBids',):
      glob_sanity_check.ValidateTypes(((bids[key], dict),))
      new_bids = GetPyClass('PositionPreferenceAdGroupCriterionBids',
                            web_services)
      for sub_key in bids[key]:
        if sub_key in ('proxyMaxCpc',):
          data = ValidateBid(bids[key][sub_key], web_services)
        else:
          glob_sanity_check.ValidateTypes(((bids[key][sub_key],
                                            (str, unicode)),))
          data = bids[key][sub_key]
        new_bids.__dict__.__setitem__('_%s' % sub_key, data)
      data = new_bids
    else:
      glob_sanity_check.ValidateTypes(((bids[key], (str, unicode)),))
      data = bids[key]
    new_bids.__dict__.__setitem__('_%s' % key, data)

  return new_bids


def ValidateExemptionRequest(exemption):
  """Validate ExemptionRequest object.

  Args:
    exemption: dict ExemptionRequest object.
  """
  glob_sanity_check.ValidateTypes(((exemption, dict),))
  for key in exemption:
    if key in ('key',):
      glob_sanity_check.ValidateTypes(((exemption[key], dict),))
      for sub_key in exemption[key]:
        if (isinstance(exemption[key][sub_key], tuple) and
            not exemption[key][sub_key]):
          continue
        glob_sanity_check.ValidateTypes(((exemption[key][sub_key],
                                          (str, unicode)),))


def ValidateGeoPoint(geo_point, web_services):
  """Validate GeoPoint object.

  Args:
    geo_point: dict GeoPoint object.
    web_services: module for web services.

  Returns:
    GeoPoint instance.
  """
  if IsPyClass(geo_point):
    return geo_point

  glob_sanity_check.ValidateTypes(((geo_point, dict),))
  new_geo_point = GetPyClass('GeoPoint', web_services)
  for key in geo_point:
    if geo_point[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((geo_point[key], (str, unicode)),))
    new_geo_point.__dict__.__setitem__('_%s' % key, geo_point[key])

  return new_geo_point


def ValidateAddress(address, web_services):
  """Validate Address object.

  Args:
    address: dict Address object.
    web_services: module for web services.

  Returns:
    Address instance.
  """
  if IsPyClass(address):
    return address

  glob_sanity_check.ValidateTypes(((address, dict),))
  new_address = GetPyClass('Address', web_services)
  for key in address:
    if address[key] == 'None': continue
    if address[key]:
      glob_sanity_check.ValidateTypes(((address[key], (str, unicode)),))
      new_address.__dict__.__setitem__('_%s' % key, address[key])

  return new_address


def ValidateTarget(target, web_services):
  """Validate Target object.

  A Target object is one of AdScheduleTarget, AgeTarget, CityTarget,
  CountryTarget, DemographicTarget, GenderTarget, GeoTarget, LanguageTarget,
  MetroTarget, NetworkTarget, PlatformTarget, PolygonTarget, ProvinceTarget,
  ProximityTarget, Target.

  Args:
    target: list a target object.
    web_services: module for web services.

  Returns:
    XxxTarget instance.
  """
  if IsPyClass(target):
    return target

  glob_sanity_check.ValidateTypes(((target, dict),))
  if 'type' in target:
    new_target = GetPyClass(target['type'], web_services)
  elif 'Target_Type' in target:
    new_target = GetPyClass(target['Target_Type'], web_services)
  else:
    msg = 'The \'type\' of the target is missing.'
    raise ValidationError(msg)
  for key in target:
    if target[key] == 'None': continue
    if key in ('vertices',):
      glob_sanity_check.ValidateTypes(((target[key], list),))
      geo_points = []
      for item in target[key]:
        geo_points.append(ValidateGeoPoint(item, web_services))
      data = geo_points
    elif key in ('address',):
      data = ValidateAddress(target[key], web_services)
    elif key in ('geoPoint',):
      data = ValidateGeoPoint(target[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((target[key], (str, unicode)),))
      data = target[key]
    new_target.__dict__.__setitem__('_%s' % key, data)

  return new_target


def ValidateEntityId(id, type, web_services):
  """Validate XxxId object.

  The XxxId object is one of AdUnionId, EntityId, TempAdUnionId.

  Args:
    id: dict EntityId object.
    type: string desired type to set for this entity id.
    web_services: module for web services.

  Returns:
    XxxId instance.
  """
  if IsPyClass(id):
    return id

  glob_sanity_check.ValidateTypes(((id, dict),))
  new_id = GetPyClass(type, web_services)
  for key in id:
    if id[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((id[key], (str, unicode)),))
    new_id.__dict__.__setitem__('_%s' % key, id[key])

  return new_id


def ValidateJobOperation(operation, web_services):
  """Validate JobOperation object.

  Args:
    operation: dict JobOperation object.
    web_services: module for web services.

  Returns:
    JobOperation instance.
  """
  if IsPyClass(operation):
    return operation

  glob_sanity_check.ValidateTypes(((operation, dict),))
  if 'type' not in operation:
    msg = 'A job operation type is missing.'
    raise ValidationError(msg)
  operation_type = '%sOperation' % operation['type']
  new_operation = GetPyClass(operation_type, web_services)
  operation = ValidateOperation(operation, web_services)
  for key in operation:
    new_operation.__dict__.__setitem__('_%s' % key, operation[key])

  return new_operation


def ValidateOperationStream(stream, web_services):
  """Validate OperationStream object.

  Args:
    stream: dict OperationStream object.
    web_services: module for web services.

  Returns:
    OperationStream instance.
  """
  if IsPyClass(stream):
    return stream

  glob_sanity_check.ValidateTypes(((stream, dict),))
  new_stream = GetPyClass('OperationStream', web_services)
  for key in stream:
    if stream[key] == 'None': continue
    if key in ('operations',):
      glob_sanity_check.ValidateTypes(((stream[key], list),))
      ops = []
      for item in stream[key]:
        ops.append(ValidateJobOperation(item, web_services))
      data = ops
    elif key in ('scopingEntityId',):
      data = ValidateEntityId(stream[key], 'EntityId', web_services)
    else:
      glob_sanity_check.ValidateTypes(((stream[key], (str, unicode)),))
      data = stream[key]
    new_stream.__dict__.__setitem__('_%s' % key, data)

  return new_stream


def ValidateBulkMutateRequest(bmr, web_services):
  """Validate BulkMutateRequest object.

  Args:
    bmr: dict BulkMutateRequest object.
    web_services: module for web services.

  Returns:
    BulkMutateRequest instance.
  """
  if IsPyClass(bmr):
    return bmr

  glob_sanity_check.ValidateTypes(((bmr, dict),))
  new_bmr = GetPyClass('BulkMutateRequest', web_services)
  for key in bmr:
    if bmr[key] == 'None': continue
    if key in ('operationStreams',):
      glob_sanity_check.ValidateTypes(((bmr[key], list),))
      streams = []
      for item in bmr[key]:
        stream = ValidateOperationStream(item, web_services)
        streams.append(stream)
      data = streams
    else:
      glob_sanity_check.ValidateTypes(((bmr[key], (str, unicode)),))
      data = bmr[key]
    new_bmr.__dict__.__setitem__('_%s' % key, data)

  return new_bmr


def ValidateAdExtension(extension, web_services):
  """Validate AdExtension object.

  Args:
    extension: dict AdExtension object.
    web_services: module for web services.

  Returns:
    AdExtension instance.
  """
  if IsPyClass(extension):
    return extension

  glob_sanity_check.ValidateTypes(((extension, dict),))
  if 'type' in extension:
    new_extension = GetPyClass(extension['type'], web_services)
  else:
    new_extension = GetPyClass('AdExtension', web_services)
  for key in extension:
    if extension[key] == 'None': continue
    if key in ('address',):
      data = ValidateAddress(extension[key], web_services)
    elif key in ('geoPoint',):
      data = ValidateGeoPoint(extension[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((extension[key], (str, unicode)),))
      data = extension[key]
    new_extension.__dict__.__setitem__('_%s' % key, data)

  return new_extension


def ValidateOverrideInfo(info, web_services):
  """Validate OverrideInfo object.

  Args:
    info: dict OverrideInfo object.
    web_services: module for web services.

  Returns:
    OverrideInfo instance.
  """
  if IsPyClass(info):
    return info

  glob_sanity_check.ValidateTypes(((info, dict),))
  new_info = GetPyClass('OverrideInfo', web_services)
  for key in info:
    if info[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((info[key], (str, unicode)),))
    info.__dict__.__setitem__('_%s' % key, info[key])

  return new_info


def ValidateLongComparisonOperation(operation, web_services):
  """Validate LongComparisonOperation object.

  Args:
    operation: dict LongComparisonOperation object.
    web_services: module for web services.

  Returns:
    LongComparisonOperation instance.
  """
  if IsPyClass(operation):
    return operation

  glob_sanity_check.ValidateTypes(((operation, dict),))
  new_operation = GetPyClass('LongComparisonOperation', web_services)
  for key in operation:
    if operation[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((operation[key], (str, unicode)),))
    new_operation.__dict__.__setitem__('_%s' % key, operation[key])

  return new_operation


def ValidateKeyword(keyword, web_services):
  """Validate Keyword object.

  Args:
    keyword: dict Keyword object.
    web_services: module for web services.

  Returns:
    Keyword instance.
  """
  if IsPyClass(keyword):
    return keyword

  glob_sanity_check.ValidateTypes(((keyword, dict),))
  new_keyword = GetPyClass('Keyword', web_services)
  for key in keyword:
    if keyword[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((keyword[key], (str, unicode)),))
    new_keyword.__dict__.__setitem__('_%s' % key, keyword[key])

  return new_keyword


def ValidateCountryTarget(target, web_services):
  """Validate CountryTarget object.

  Args:
    target: dict CountryTarget object.
    web_services: module for web services.

  Returns:
    CountryTarget instance.
  """
  if IsPyClass(target):
    return target

  glob_sanity_check.ValidateTypes(((target, dict),))
  new_target = GetPyClass('CountryTarget', web_services)
  for key in target:
    if target[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((target[key], (str, unicode)),))
    new_target.__dict__.__setitem__('_%s' % key, target[key])

  return new_target


def ValidateLanguageTarget(target, web_services):
  """Validate LanguageTarget object.

  Args:
    target: dict LanguageTarget object.
    web_services: module for web services.

  Returns:
    LanguageTarget instance.
  """
  if IsPyClass(target):
    return target

  glob_sanity_check.ValidateTypes(((target, dict),))
  new_target = GetPyClass('LanguageTarget', web_services)
  for key in target:
    if target[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((target[key], (str, unicode)),))
    new_target.__dict__.__setitem__('_%s' % key, target[key])

  return new_target


def ValidatePaging(paging, web_services):
  """Validate Paging object.

  Args:
    paging: dict Paging object.
    web_services: module for web services.

  Returns:
    Paging instance.
  """
  if IsPyClass(paging):
    return paging

  glob_sanity_check.ValidateTypes(((paging, dict),))
  new_paging = GetPyClass('Paging', web_services)
  for key in paging:
    if paging[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((paging[key], (str, unicode)),))
    new_paging.__dict__.__setitem__('_%s' % key, paging[key])

  return new_paging


def ValidateSearchParameter(param, web_services):
  """Validate SearchParameter object.

  A SearchParameter is one of AdTypeSearchParameter,
  AverageTargetedMonthlySearchesSearchParameter, CompetitionSearchParameter,
  CountryTargetSearchParameter, ExcludedKeywordSearchParameter,
  GlobalMonthlySearchesSearchParameter, IncludeAdultContentSearchParameter,
  KeywordCategoryIdSearchParameter, KeywordMatchTypeSearchParameter,
  LanguageTargetSearchParameter, MobileSearchParameter,
  NgramGroupsSearchParameter, PlacementTypeSearchParameter,
  RelatedToKeywordSearchParameter, RelatedToUrlSearchParameter,
  SeedAdGroupIdSearchParameter

  Args:
    search_parameter: dict SearchParameter object.
    web_services: module for web services.

  Returns:
    XxxSearchParameter instance.
  """
  if IsPyClass(param):
    return param

  glob_sanity_check.ValidateTypes(((param, dict),))
  if 'type' in param:
    new_param = GetPyClass(param['type'], web_services)
  elif 'SearchParameter_Type' in param:
    new_param = GetPyClass('SearchParameter_Type', web_services)
  else:
    msg = 'The \'type\' of the search parameter is missing.'
    raise ValidationError(msg)
  for key in param:
    if param[key] == 'None': continue
    if key in ('adTypes', 'levels', 'keywordMatchTypes', 'ngramGroups',
               'categoryIds', 'placementTypes', 'urls', 'included', 'excluded'):
      glob_sanity_check.ValidateTypes(((param[key], list),))
      items = []
      for item in param[key]:
        glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
        items.append(item)
      data = items
    elif key in ('operation',):
      data = ValidateLongComparisonOperation(param[key], web_services)
    elif key in ('keywords',):
      glob_sanity_check.ValidateTypes(((param[key], list),))
      kws = []
      for item in param[key]:
        kws.append(ValidateKeyword(item, web_services))
      data = kws
    elif key in ('countryTargets',):
      glob_sanity_check.ValidateTypes(((param[key], list),))
      targets = []
      for item in param[key]:
        targets.append(ValidateCountryTarget(item, web_services))
      data = targets
    elif key in ('languageTargets',):
      glob_sanity_check.ValidateTypes(((param[key], list),))
      targets = []
      for item in param[key]:
        targets.append(ValidateLanguageTarget(item, web_services))
      data = targets
    else:
      glob_sanity_check.ValidateTypes(((param[key], (str, unicode)),))
      data = param[key]
    new_param.__dict__.__setitem__('_%s' % key, data)

  return new_param


def ValidateBiddingStrategy(strategy, web_services):
  """Validate BiddingStrategy object.

  A BiddingStrategy is one of BudgetOptimizer, ConversionOptimizer, ManualCPC,
  ManualCPM.

  Args:
    strategy: dict BiddingStrategy object.
    web_services: module for web services.

  Returns:
    BiddingStrategy instance.
  """
  if IsPyClass(strategy):
    return strategy

  glob_sanity_check.ValidateTypes(((strategy, dict),))
  if 'type' in strategy:
    new_strategy = GetPyClass(strategy['type'], web_services)
  elif 'BiddingStrategy_Type' in strategy:
    new_strategy = GetPyClass(strategy['BiddingStrategy_Type'], web_services)
  else:
    msg = 'The \'type\' of the bidding transition is missing.'
    raise ValidationError(msg)
  for key in strategy:
    if strategy[key] == 'None': continue
    if key in ('bidCeiling',):
      data = ValidateMoney(strategy[key], web_services)
    else:
      glob_sanity_check.ValidateTypes(((strategy[key], (str, unicode)),))
      data = strategy[key]
    new_strategy.__dict__.__setitem__('_%s' % key, data)

  return new_strategy


def ValidateFrequencyCap(cap, web_services):
  """Validate FrequencyCap object.

  Args:
    paging: dict frequency cap object.
    web_services: module for web services.

  Returns:
    FrequencyCap instance.
  """
  if IsPyClass(cap):
    return cap

  glob_sanity_check.ValidateTypes(((cap, dict),))
  new_cap = GetPyClass('FrequencyCap', web_services)
  for key in cap:
    if cap[key] == 'None': continue
    glob_sanity_check.ValidateTypes(((cap[key], (str, unicode)),))
    new_cap.__dict__.__setitem__('_%s' % key, cap[key])

  return new_cap


def ValidateBidLandscapeSelector(selector, web_services):
  """Validate BidLandscapeSelector object.

  Args:
    selector: dict selector object.
    web_services: module for web services.
  """
  if IsPyClass(selector):
    return selector

  glob_sanity_check.ValidateTypes(((selector, dict),))
  if 'type' in selector:
    new_selector = GetPyClass(selector['type'], web_services)
  elif 'BidLandscapeSelector_Type' in selector:
    new_selector = GetPyClass(selector['BidLandscapeSelector_Type'],
                              web_services)
  else:
    msg = 'The \'type\' of the bid landscape selector is missing.'
    raise ValidationError(msg)
  for key in selector:
    if key in ('idFilters',):
      glob_sanity_check.ValidateTypes(((selector[key], list),))
      filters = []
      for item in selector[key]:
        glob_sanity_check.ValidateTypes(((item, dict),))
        filter = GetPyClass('BidLandscapeIdFilter', web_services)
        for sub_key in item:
          glob_sanity_check.ValidateTypes(((item[sub_key], (str, unicode)),))
          filter.__dict__.__setitem__('_%s' % sub_key, item[sub_key])
        filters.append(filter)
      data = filters
    else:
      data = selector[key]
    new_selector.__dict__.__setitem__('_%s' % key, data)

  return new_selector


def ValidatePredicate(predicate, web_services):
  """Validate Predicate object.

  Args:
    predicate: dict predicate object.
    web_services: module for web services.
  """
  if IsPyClass(predicate):
    return predicate

  glob_sanity_check.ValidateTypes(((predicate, dict),))
  for key in predicate:
    if key in ('values',):
      glob_sanity_check.ValidateTypes(((predicate[key], list),))
      for item in predicate[key]:
        glob_sanity_check.ValidateTypes(((item, str),))
    else:
      glob_sanity_check.ValidateTypes(((predicate[key], str),))


def ValidateOperation(operation, web_services):
  """Validate Operation object.

  Args:
    operation: dict operation object.
    web_services: module for web services.

  Returns:
    dict updated Operation object.
  """
  if IsPyClass(operation):
    return operation

  glob_sanity_check.ValidateTypes(((operation, dict),))
  caller = {
    'name': web_services.__name__.split('.')[-1].split('Service')[0],
    'typed': False
  }
  if 'type' in operation: caller['name'] = operation['type']
  # Custom handler for services that require concrete types for ADD and SET
  # operators.
  if caller['name'] in ('AdGroupCriterion', 'BulkMutateJob',
                        'CampaignAdExtension', 'CampaignCriterion',
                        'CampaignTarget'):
    caller['typed'] = True
  operator = ''
  for key in operation:
    if key in ('operator',):
      glob_sanity_check.ValidateTypes(((operation[key], (str, unicode)),))
      operator = operation[key]
    elif key in ('operand',):
      glob_sanity_check.ValidateTypes(((operation[key], dict),))
      operand = operation[key]
      if (caller['typed'] and 'type' in operand) or 'type' in operation:
        caller['typed'] = True
        if 'type' in operation and 'type' in operand:
          type = operand['type']
        elif 'type' in operation:
          type = operation['type']
        else:
          type = operand['type']
        new_operand = GetPyClass(type, web_services)
      elif not caller['typed']:
        pass
      else:
        msg = 'The \'type\' of the operand is missing.'
        raise ValidationError(msg)
      for sub_key in operand:
        if sub_key in ('ad',):
          data = ValidateAd(operator, operand[sub_key], web_services)
        elif sub_key in ('bids',):
          data = ValidateBids(operand[sub_key], web_services)
        elif sub_key in ('criterion',):
          data = ValidateCriterion(operator, operand[sub_key], web_services)
        elif sub_key in ('minBids',):
          glob_sanity_check.ValidateTypes(((operand[sub_key], list),))
          bids = []
          for item in operand[sub_key]:
            bids.append(ValidateBid(item, web_services))
          data = bids
        elif sub_key in ('budget',):
          data = ValidateBudget(operand[sub_key], web_services)
        elif sub_key in ('biddingStrategy',):
          data = ValidateBiddingStrategy(operand[sub_key], web_services)
        elif sub_key in ('frequencyCap',):
          data = ValidateFrequencyCap(operand[sub_key], web_services)
        elif sub_key in ('targets',):
          glob_sanity_check.ValidateTypes(((operand[sub_key], list),))
          targets = []
          for item in operand[sub_key]:
            targets.append(ValidateTarget(item, web_services))
          data = targets
        elif sub_key in ('request',):
          data = ValidateBulkMutateRequest(operand[sub_key], web_services)
        elif sub_key in ('adExtension',):
          data = ValidateAdExtension(operand[sub_key], web_services)
        elif sub_key in ('overrideInfo',):
          data = ValidateOverrideInfo(operand[sub_key], web_services)
        elif sub_key in ('customerIds',):
          glob_sanity_check.ValidateTypes(((operand[sub_key], list),))
          for item in operand[sub_key]:
            glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
        elif sub_key in ('selector',):
          ValidateSelector(operand[sub_key], web_services)
          data = operand[sub_key]
        else:
          data = operand[sub_key]
        if caller['typed']:
          new_operand.__dict__.__setitem__('_%s' % sub_key, data)
        else:
          operand[sub_key] = data
      if caller['typed']:
        new_operand.__dict__.__setitem__('_%s' % key, operand)
        operation[key] = new_operand
    elif key in ('exemptionRequests',):
      glob_sanity_check.ValidateTypes(((operation[key], list),))
      for item in operation[key]:
        ValidateExemptionRequest(item)
      data = operation[key]
    elif key in ('biddingTransition',):
      glob_sanity_check.ValidateTypes(((operation[key], dict),))
      for sub_key in operation[key]:
        if sub_key in ('targetBiddingStrategy',):
          operation[key][sub_key] = \
              ValidateBiddingStrategy(operation[key][sub_key], web_services)
        elif sub_key in ('explicitAdGroupBids',):
          operation[key][sub_key] = \
              ValidateBids(operation[key][sub_key], web_services)
        else:
          glob_sanity_check.ValidateTypes(((operation[key][sub_key],
                                            (str, unicode)),))

  return operation


def ValidateSelector(selector, web_services):
  """Validate Selector object.

  Args:
    selector: dict selector object.
    web_services: module for web services.
  """
  glob_sanity_check.ValidateTypes(((selector, dict),))
  for key in selector:
    if key in ('idFilters',):
      glob_sanity_check.ValidateTypes(((selector[key], list),))
      for item in selector[key]:
        glob_sanity_check.ValidateTypes(((item, dict),))
        for sub_key in item:
          glob_sanity_check.ValidateTypes(((item[sub_key], (str, unicode)),))
    elif key in ('statsSelector',):
      glob_sanity_check.ValidateTypes(((selector[key], dict),))
      for sub_key in selector[key]:
        ValidateDateRange(selector[key][sub_key], web_services)
    elif key in ('dateRange',):
      ValidateDateRange(selector[key], web_services)
    elif key in ('adIds', 'adExtensionIds', 'adGroupIds', 'campaignIds',
                 'criteriaId', 'jobIds', 'ids', 'clientEmails',
                 'customerJobKeys', 'requestedAttributeTypes', 'jobStatuses',
                 'userStatuses', 'statuses', 'campaignStatuses', 'fields'):
      glob_sanity_check.ValidateTypes(((selector[key], list),))
      for item in selector[key]:
        glob_sanity_check.ValidateTypes(((item, (str, unicode)),))
    elif key in ('searchParameters'):
      glob_sanity_check.ValidateTypes(((selector[key], list),))
      params = []
      for item in selector[key]:
        params.append(ValidateSearchParameter(item, web_services))
      selector[key] = params
    elif key in ('paging',):
      ValidatePaging(selector[key], web_services)
    elif key in ('addresses',):
      glob_sanity_check.ValidateTypes(((selector[key], list),))
      addresses = []
      for item in selector[key]:
        addresses.append(ValidateAddress(item, web_services))
      selector[key] = addresses
    elif key in ('predicates',):
      glob_sanity_check.ValidateTypes(((selector[key], list),))
      for item in selector[key]:
        ValidatePredicate(item, web_services)
    else:
      glob_sanity_check.ValidateTypes(((selector[key], (str, unicode)),))
