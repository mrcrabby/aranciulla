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

"""Handler functions for outgoing and incoming messages."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import re
import types

from aw_api import SanityCheck as glob_sanity_check
from aw_api import Utils
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


def GetServiceConnection(headers, config, url, http_proxy, version):
  """Get SOAP service connection.

  Args:
    headers: dict dictionary object with populated authentication
             credentials.
    config: dict dictionary object with populated configuration values.
    url: str url of the web service to call.
    http_proxy: str HTTP proxy to use.
    version: str version of the API in use.

  Returns:
    instance SOAPpy.SOAPProxy with set headers.
  """
  # Catch empty SOAP header elements and exclude them from request.
  full_headers = {}
  for key in headers:
    if headers[key]: full_headers[key] = headers[key]

  if glob_sanity_check.IsNewApi(version):
    headers = SOAPpy.Types.headerType({config['ns_target'][1]: full_headers})
    headers._setAttr('xmlns', config['ns_target'][0])
  else:
    headers = SOAPpy.Types.headerType(full_headers)
  service = SOAPpy.SOAPProxy(url, http_proxy=http_proxy, header=headers)
  service.config.dumpHeadersIn = 1
  service.config.dumpHeadersOut = 1
  service.config.dumpSOAPIn = 1
  service.config.dumpSOAPOut = 1

  # Turn off type information, since SOAPpy usually gets the types wrong.
  service.config.typed = 0

  # Turn on noroot, to skip including "SOAP-ENC:root" as part of the request.
  service.noroot = 1

  # Explicitly set the style of the namespace, otherwise will default to 1999.
  service.config.namespaceStyle = '2001'

  return service


def SetRequestParams(config, method_name, params):
  """Set SOAP request parameters.

  Args:
    config: dict dictionary object with populated configuration values.
    method_name: str API method name.
    params: list list of parameters to send to the API method.

  Returns:
    instance SOAPpy.Types.bodyType with set parameters.
  """
  # Set namespace at method's level.
  params = SOAPpy.Types.untypedType(Utils.MakeTextXMLReady(params))
  params._setAttr('xmlns', config['ns_target'][0])

  # Set namespace at body's level.
  body = SOAPpy.Types.bodyType({method_name: params})
  body._setAttr('xmlns', config['ns_target'][0])

  return body


def UnpackResponseAsDict(response):
  """Unpack (recursively) SOAP data holder into a Python dict object.

   Args:
     response: instance of SOAP data holder object.

  Returns:
    dict unpacked SOAP data holder.
  """
  if (isinstance(response, types.InstanceType) and
      response.__dict__['_type'] == 'struct'):
    if not response.__dict__.keys():
      return (response.__dict__,)

    dct = {}
    for key in response.__dict__:
      if key[0] == '_':
        continue
      value = response.__dict__.get(key)
      if key == 'entries' and not isinstance(value, list):
        value = [value]
      data = UnpackResponseAsDict(value)
      if key == 'value' and isinstance(data, dict):
        data = [data]
      dct[str(key)] = data

    return dct
  elif (isinstance(response, list)):
    lst = []
    for item in response:
      lst.append(UnpackResponseAsDict(item))
    return lst
  else:
    return response


def GetKeyOrder(key, type):
  """Get order of sub keys for an object identified by a given key.

  For example, a dictionary that is identified by a key "dateRange" maps to an
  object DateRange (see http://code.google.com/apis/adwords/v2009/docs/reference/CampaignService.DateRange.html)
  and will return a tuple consisting of the object's name and its sub-keys,
  ('DateRange', ['min', 'max']).

  Args:
    key: str a key whose object to look up.
    type: str an xsi type to set.

  Returns:
    tuple a object's type and a list of keys in order.
  """
  order = ()
  if key in ('selector',):
    # AdExtensionOverrideSelector, AdGroupAdSelector, AdGroupCriterionSelector,
    # AdGroupSelector, AdParamSelector, CampaignAdExtensionSelector,
    # CampaignCriterionSelector, CampaignSelector, CampaignTargetSelector,
    # GeoLocationSelector, InfoSelector
    order = ('', ['ids','campaignId', 'campaignIds', 'adGroupIds', 'adIds',
                  'criteriaId', 'adExtensionIds',  'idFilters', 'criterionUse',
                  'campaignStatuses', 'userStatuses', 'addresses', 'statuses',
                  'serviceName', 'methodName', 'operator', 'fields',
                  'predicates', 'dateRange', 'clientEmails', 'apiUsageType',
                  'statsSelector', 'paging'])
  elif key in ('statsSelector',):
    order = ('StatsSelector', ['dateRange'])
  elif key in ('dateRange',):
    order = ('DateRange', ['min', 'max'])
  elif key in ('paging',):
    order = ('Paging', ['startIndex', 'numberResults'])
  elif key in ('operations',):
    # AdExtensionOverrideOperation, AdGroupAdOperation,
    # AdGroupCriterionOperation, AdGroupOperation, AdParamOperation,
    # CampaignAdExtensionOperation, CampaignCriterionOperation,
    # CampaignOperation, CampaignTargetOperation
    order = ('', ['operator', 'biddingTransition', 'operand',
                  'exemptionRequests'])
  elif key in ('biddingTransition',):
    order = ('BiddingTransition',
             ['targetBiddingStrategy', 'explicitAdGroupBids', 'useSavedBids'])
  elif key in ('targetBiddingStrategy', 'biddingStrategy'):
    # BiddingStrategy
    order = (type, ['bidCeiling', 'pricingModel'])
  elif key in ('amount', 'bidCeiling'):
    order = ('Money', ['microAmount'])
  elif key in ('explicitAdGroupBids', 'bids'):
    # AdGroupBids, ConversionOptimizerAdGroupCriterionBids,
    # BudgetOptimizerAdGroupCriterionBids, ManualCPMAdGroupCriterionBids,
    # ManualCPCAdGroupCriterionBids
    if type == 'ConversionOptimizerAdGroupCriterionBids':
      order = (type, [])
    elif type == 'BudgetOptimizerAdGroupCriterionBids':
      order = (type, ['proxyBid'])
    elif type == 'ManualCPMAdGroupCriterionBids':
      order = (type, ['maxCpm', 'bidSource'])
    elif type == 'ManualCPCAdGroupCriterionBids':
      order = (type, ['maxCpc', 'bidSource', 'positionPreferenceBids'])
    else:
      order = (type, ['proxyKeywordMaxCpc', 'proxySiteMaxCpc', 'targetCpa',
                      'keywordMaxCpc', 'keywordContentMaxCpc', 'siteMaxCpc',
                      'maxCpm'])
  elif key in ('proxyKeywordMaxCpc', 'proxySiteMaxCpc', 'targetCpa',
              'keywordMaxCpc', 'keywordContentMaxCpc', 'siteMaxCpc', 'maxCpm',
              'proxyBid', 'maxCpc'):
    order = ('Bid', ['amount'])
  elif key in ('operand',):
    # AdExtensionOverride, AdGroupAd, AdGroup, AdParam, AdScheduleTargetList,
    # BiddableAdGroupCriterion, Campaign, CampaignAdExtension,
    # DemographicTargetList, GeoTargetList, LanguageTargetList,
    # NegativeAdGroupCriterion, NegativeCampaignCriterion,  NetworkTargetList,
    # PlatformTargetList
    if type == 'BiddableAdGroupCriterion':
      order = (type, ['adGroupId', 'criterion', 'userStatus', 'destinationUrl',
                      'bids'])
    elif type == 'NegativeAdGroupCriterion':
      order = (type, ['adGroupId', 'criterion'])
    elif (type == 'AdScheduleTargetList' or type == 'DemographicTargetList' or
          type == 'GeoTargetList' or type == 'LanguageTargetList' or
          type == 'NetworkTargetList' or type == 'PlatformTargetList'):
      order = (type, ['campaignId', 'targets'])
    elif type == 'NegativeCampaignCriterion':
      order = (type, ['campaignId', 'criterion'])
    elif type == 'ReportDefinition':
      order = (type, ['id', 'selector', 'reportName', 'reportType',
                      'hasAttachment', 'dateRangeType', 'downloadFormat',
                      'customerIds'])
    else:
      order = ('', ['adGroupId', 'adId', 'id', 'campaignId', 'criterionId',
                    'campaignName', 'ad', 'adExtension', 'overrideInfo', 'name',
                    'status', 'startDate', 'endDate', 'budget',
                    'biddingStrategy', 'autoKeywordMatchingStatus',
                    'adServingOptimizationStatus', 'frequencyCap', 'bids',
                    'insertionText', 'paramIndex'])
  elif key in ('ad',):
    # DeprecatedAd, MobileAd, TextAd, MobileImageAd, ImageAd, LocalBusinessAd
    if type == 'MobileImageAd':
      order = (type, ['id', 'url', 'displayUrl', 'markupLanguages',
                      'mobileCarriers', 'image'])
    elif type == 'ImageAd':
      order = (type, ['id', 'url', 'displayUrl', 'image', 'name'])
    elif type == 'LocalBusinessAd':
      order = (type, ['id', 'url', 'displayUrl', 'fullBusinessName',
                      'phoneNumber', 'streetAddress', 'city', 'region',
                      'regionCode', 'postalCode', 'countryCode', 'businessName',
                      'description1', 'description2', 'target', 'businessImage',
                      'icon'])
    else:
      order = (type, ['id', 'url', 'displayUrl', 'templateId', 'adUnionId',
                      'templateElements', 'dimensions', 'name', 'type',
                      'headline', 'description', 'description1', 'description2',
                      'markupLanguages', 'mobileCarriers', 'image',
                      'businessName', 'countryCode', 'phoneNumber'])
  elif key in ('target',):
    order = ('ProximityTarget', ['excluded', 'geoPoint', 'radiusDistanceUnits',
                                 'radiusInUnits', 'address',
                                 'allowServiceOfAddress'])
  elif key in ('image', 'businessImage', 'icon'):
    order = ('Image', ['mediaId', 'dimensions', 'urls', 'name', 'data'])
  elif key in ('dimensions', 'urls', 'extendedCapabilities'):
    # Media_Size_DimensionsMapEntry, Media_Size_StringMapEntry,
    # Media_MediaExtendedCapabilityType_Media_MediaExtendedCapabilityStateMapEntry
    order = ('', ['key', 'value'])
  elif key in ('value', 'dimensions'):
    order = ('Dimensions', ['width', 'height'])
  elif key in ('budget',):
    order = ('Budget', ['period', 'amount', 'deliveryMethod'])
  elif key in ('frequencyCap',):
    order = ('FrequencyCap', ['impressions', 'timeUnit', 'level'])
  elif key in ('adExtension',):
    # LocationExtension
    order = (type, ['id', 'address', 'geoPoint', 'encodedLocation',
                    'companyName', 'phoneNumber', 'source', 'iconMediaId',
                    'imageMediaId'])
  elif key in ('address', 'addresses'):
    order = ('Address', ['streetAddress', 'streetAddress2', 'cityName',
                         'provinceCode', 'provinceName', 'postalCode',
                         'countryCode'])
  elif key in ('geoPoint', 'vertices'):
    order = ('GeoPoint', ['latitudeInMicroDegrees', 'longitudeInMicroDegrees'])
  elif key in ('overrideInfo',):
    order = ('LocationOverrideInfo', ['radius', 'radiusUnits'])
  elif key in ('exemptionRequests',):
    order = ('ExemptionRequest', ['key'])
  elif key in ('key',):
    order = ('PolicyViolationKey', ['policyName', 'violatingText'])
  elif key in ('adUnionId',):
    order = ('TempAdUnionId', ['id'])
  elif key in ('templateElements',):
    order = ('TemplateElement', ['uniqueName', 'fields'])
  elif key in ('fields',):
    order = ('TemplateElementField', ['name', 'type', 'fieldText',
                                      'fieldMedia'])
  elif key in ('fieldMedia',):
    # Audio, Image, Video
    order = (type, ['mediaId', 'dimensions', 'name', 'extendedCapabilities',
                    'durationMillis', 'streamingUrl', 'readyToPlayOnTheWeb',
                    'data', 'industryStandardCommercialIdentifier',
                    'advertisingId'])
  elif key in ('idFilters',):
    if type == 'AdGroupCriterionIdFilter':
      order = (type, ['campaignId', 'adGroupId', 'criterionId'])
    elif type == 'CampaignCriterionIdFilter':
      order = (type, ['campaignId', 'criterionId'])
    else:
      order = ('', ['campaignId', 'adGroupId', 'criterionId'])
  elif key in ('criterion',):
    if type == 'Keyword':
      order = (type, ['id', 'text', 'matchType'])
    elif type == 'Placement':
      order = (type, ['id', 'url'])
    elif type == 'ContentLabel':
      order = (type, ['id', 'contentLabelType'])
    else:
      order = ('', ['id', 'text', 'url', 'matchType', 'contentLabelType'])
  elif key in ('positionPreferenceBids',):
    order = ('PositionPreferenceAdGroupCriterionBids',
             ['proxyMaxCpc', 'preferredPosition', 'bottomPosition'])
  elif key in ('targets',):
    if type == 'AdScheduleTarget':
      order = (type, ['dayOfWeek', 'startHour', 'startMinute', 'endHour',
                      'endMinute', 'bidMultiplier'])
    elif type == 'AgeTarget':
      order = (type, ['bidModifier', 'age'])
    elif type == 'GenderTarget':
      order = (type, ['bidModifier', 'gender'])
    elif type == 'CityTarget':
      order = (type, ['excluded', 'cityName', 'provinceCode', 'countryCode'])
    elif type == 'CountryTarget':
      order = (type, ['excluded', 'countryCode'])
    elif type == 'MetroTarget':
      order = (type, ['excluded', 'metroCode'])
    elif type == 'PolygonTarget':
      order = (type, ['excluded', 'vertices'])
    elif type == 'ProvinceTarget':
      order = (type, ['excluded', 'provinceCode'])
    elif type == 'ProximityTarget':
      order = (type, ['excluded', 'geoPoint', 'radiusDistanceUnits',
                      'radiusInUnits', 'address', 'allowServiceOfAddress'])
    elif type == 'LanguageTarget':
      order = (type, ['languageCode'])
    elif type == 'NetworkTarget':
      order = (type, ['networkCoverageType'])
    elif type == 'PlatformTarget':
      order = (type, ['platformType'])
    else:
      order = ('', ['dayOfWeek', 'startHour', 'startMinute', 'endHour',
                    'endMinute', 'bidMultiplier', 'bidModifier', 'age',
                    'gender', 'excluded', 'cityName', 'provinceCode',
                    'countryCode', 'metroCode', 'vertices', 'provinceCode',
                    'geoPoint', 'radiusDistanceUnits', 'radiusInUnits',
                    'address', 'allowServiceOfAddress', 'languageCode',
                    'networkCoverageType', 'platformType'])
  elif key in ('media',):
    order = (type, ['mediaId', 'mediaTypeDb', 'dimensions', 'name',
                    'durationMillis', 'streamingUrl', 'readyToPlayOnTheWeb',
                    'data', 'industryStandardCommercialIdentifier',
                    'advertisingId'])
  elif key in ('predicates',):
    order = ('', ['field', 'operator', 'values'])

  return order


def PackDictAsXml(obj, key, order=[], xml=''):
  """Pack a Python dictionary object into an XML string.

  For example, an input in a form of "selector = {'ids': [12345, 67890]}", where
  "selector" is key and "{'ids': [12345, 67890]}" is obj, the output will be
  "<selector><ids>12345</ids><ids>67890</ids></selector>".

  Args:
    obj: dict a Python dictionary to pack.
    key: str a key that maps to this Python dictionary.
    [optional]
    order: list an optional order of sub keys for this Python dictionary.
    xml: str an optional XML snippet holder to store intermittent results.

  Returns:
    str an XML snippet.
  """
  buf = xsi_type = ''
  tmp_xsi_type = ''
  local_order = []
  if isinstance(obj, dict):
    # Determine if the object is typed.
    for item in obj.keys():
      if item == 'type' or item.find('.Type') > -1: xsi_type = obj[item]
    # Step through each key/value pair in the dictionary and pack it.
    for sub_key in obj:
      if sub_key == 'type' or sub_key.find('.Type') > -1: continue
      tmp_xsi_type, local_order = GetKeyOrder(key, xsi_type)
      buf += PackDictAsXml(obj[sub_key], sub_key, local_order, xml)
      if local_order and buf:
        pre_tags = re.split('(<.*?>)', buf)[1:-1]
        if not pre_tags: return '<%s/>' % key
        tag_name = pre_tags[0][1:-1]
        post_tags = []
        tag_buf = ''
        counter = 0
        for pre_tag in pre_tags:
          if not pre_tag: continue
          tag = ''
          if pre_tag[0] == '<' and pre_tag[-1] == '>':
            tag = re.findall('<(?:/|)(\w+).*(?:/|)>', pre_tag)
            if tag: tag = tag[0]
          if counter == 0: tag_name = tag
          tag_buf += pre_tag
          if tag and tag_name == tag:
            counter += 1
            if counter == 2 or pre_tag[-2] == '/':
              post_tags.append(tag_buf)
              tag_buf = ''
              counter = 0
        pre_tags = post_tags
        if (len(pre_tags) > 1 and len(local_order) > 1 and
            pre_tags[0][1:] != pre_tags[-1][1:-1]):
          tmp_buf = ''
          # TODO(api.sgrinberg): Improve perforamnce by only stepping through
          # those elements from local_order that show up in pre_tags.
          for tag_name in local_order:
            for pre_tag in pre_tags:
              if pre_tag[0] != '<': pre_tag = '<%s' % pre_tag
              if pre_tag[-1] != '>': pre_tag = '%s>' % pre_tag
              if (pre_tag.find(tag_name, 1, len(tag_name) + 1) > -1 and
                  (pre_tag[len(tag_name) + 1] == ' ' or
                   pre_tag[len(tag_name) + 1] == '>')):
                tmp_buf += pre_tag
          buf = tmp_buf
    if xsi_type and len(obj.keys()) == 1:
      data = '<%s xsi3:type="%s"/>' % (key, xsi_type)
    elif xsi_type:
      data = '<%s xsi3:type="%s">%s</%s>' % (key, xsi_type, buf, key)
    else:
      if tmp_xsi_type:
        tmp_xsi_type = ' xsi3:type="%s"' % (tmp_xsi_type)
      data = '<%s%s>%s</%s>' % (key, tmp_xsi_type, buf, key)
  elif isinstance(obj, list):
    for item in obj:
      buf += PackDictAsXml(item, key, order, xml)
    data = buf
  else:
    data = '<%s>%s</%s>' % (key, obj, key)

  return data
