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

"""Classes for handling errors."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'


class Error(Exception):

  """Implements Error.

  Responsible for handling exceptions.
  """

  def __init__(self, msg):
    self.message = msg

  def __str__(self):
    return str(self.message)

  def __call__(self):
    return (self.message,)


class DetailError(object):

  """Implements DetailError.

  Responsible for handling details of a user error.  Thrown as part of an
  ApiException.
  """

  def __init__(self, index=0, code=-1, isExemptable='false', detail='',
               field='', trigger='', textIndex=0, textLength=0, stacktrace='',
               stackTrace='', fieldPath='', reason='', type='',
               isRuntimeException='', enclosingId='', limit=0, limitType='',
               key={}, externalPolicyName='', externalPolicyUrl='',
               externalPolicyDescription='', violatingParts=[], errorString=''):
    self.index = int(index)
    self.code = int(code)
    self.exemptable = isExemptable == 'true'
    self.detail = detail
    self.field = field
    self.trigger = trigger
    self.text_index = int(textIndex)
    self.text_length = int(textLength)
    if stacktrace:
      self.stack_trace = stacktrace
    else:
      self.stack_trace = stackTrace
    self.is_runtime_exception = isRuntimeException
    self.field_path = fieldPath
    self.reason = reason
    self.type = type
    self.enclosing_id = enclosingId
    self.limit = limit
    self.limit_type = limitType
    self.key = key
    self.external_policy_name = externalPolicyName
    self.external_policy_url = externalPolicyUrl
    self.external_policy_description = externalPolicyDescription
    self.violating_parts = violatingParts
    self.error_string = errorString

  def __call__(self):
    return (self.index, self.code, self.exemptable, self.detail, self.field,
            self.trigger, self.text_index, self.text_length, self.stack_trace,
            self.is_runtime_exception, self.field_path, self.reason, self.type,
            self.enclosing_id, self.limit, self.limit_type, self.key,
            self.external_policy_name, self.external_policy_url,
            self.external_policy_description, self.violating_parts,
            self.error_string)


class ApiError(Error):

  """Implements ApiException.

  Responsible for handling AdWords API exceptions.
  """

  def __init__(self, fault):
    (self.fault_code, self.fault_string) = ('', '')
    if 'faultcode' in fault:
      self.fault_code = fault['faultcode']
    if 'faultstring' in fault:
      self.fault_string = fault['faultstring']

    (self.code, self.message, self.trigger) = (-1, '', '')
    if 'detail' in fault and 'code' in fault['detail']:
      self.code = int(fault['detail']['code'])
    if 'detail' in fault and 'message' in fault['detail']:
      self.message = fault['detail']['message']
    elif not self.message:
      self.message = self.fault_string
    if 'detail' in fault and 'trigger' in fault['detail']:
      self.trigger = fault['detail']['trigger']

    self.errors = []
    errors = [None]
    if 'detail' in fault and 'errors' in fault['detail']:
      errors = fault['detail']['errors']
    elif 'detail' not in fault:
      errors[0] = {}
    else:
      errors[0] = fault['detail']
    for error in errors:
      # Keys need to be of type str not unicode.
      error_dct = dict([(str(key), value) for key, value in error.items()])
      if 'message' in error_dct:
        error_dct['detail'] = error_dct['message']
        del error_dct['message']
      # TODO(api.sgrinberg): Rework to get rid of the ** magic.
      self.errors.append(DetailError(**error_dct))

  def __str__(self):
    if self.code > -1:
      return 'Code %s: %s' % (self.code, self.message)
    else:
      return self.fault_string

  def __call__(self):
    return (self.fault,)


class ApiAsStrError(Error):

  """Implements ApiAsStrError.

  Responsible for handling AdWords API exceptions that come in a form of a
  string.
  """

  def __init__(self, msg):
    lines = msg.split('\n')
    fault = {}
    for line in lines:
      if not line or line == 'Error:':
        continue
      try:
        (key, value) = line.split(': ', 1)
        fault[key] = value
      except:
        continue
    try:
      self.code = fault['code']
      self.msg = fault['message']
    except:
      # Unknown error code, likely a stackTrace was returned (see SOAP XML log).
      self.code = -1
      self.msg = fault['faultstring']

  def __str__(self):
    return 'Code %s: %s' % (self.code, self.msg)

  def __call__(self):
    return (self.code, self.msg,)


class InvalidInputError(Error):

  """Implements InvalidInputError.

  Responsible for handling invalid local input errors.
  """

  pass


class ValidationError(Error):

  """Implements ValidationError.

  Responsible for handling validation errors that are caught locally by the
  client library.
  """

  pass


class ApiVersionNotSupportedError(Error):

  """Implements ApiVersionNotSupportedError.

  Responsible for handling errors due to unsupported version of API.
  """

  pass


class MissingPackageError(Error):

  """Implements MissingPackageError.

  Responsible for handling missing package errors.
  """

  pass


class MalformedBufferError(Error):

  """Implements MalformedBufferError.

  Responsible for handling malformaed SOAP buffer errors.
  """

  pass


class AuthTokenError(Error):

  """Implements AuthTokenError.

  Responsible for handling auth token errors.
  """

  pass


class RequestError(ApiError):

  """Implements RequestError.

  Responsible for handling AdWords API errors
  Code: 1-10, 12-17, 19-42, 44-49, 51, 54, 57-59, 61-63, 70-83, 87-94, 96, 97,
  99, 112, 115, 116, 120-125, 127, 128, 131, 133, 134, 137, 138, 140-142,
  144-147, 149, 153, 156-158, 170-174, 176, 177, 186, 188, 190, 206, 207
  Type: 'AdError', 'AdGroupAdError', 'AdGroupCriterionError',
  'AdGroupServiceError', 'ApiError', 'AuthenticationError',
  'AuthorizationError', 'BiddingError', 'BiddingTransitionError', 'BudgetError',
  'CampaignCriterionError', 'CampaignError', 'ClientTermsError',
  'CriterionPolicyError', 'DatabaseError', 'DateError', 'DistinctError',
  'IdError', 'ImageError', 'InternalApiError', 'LoasAuthenticationError',
  'MediaError', 'NewEntityCreationError', 'NotEmptyError',
  'NotWhitelistedError', 'NullError', 'OperatorError', 'PagingError',
  'PolicyViolationError', 'QuotaCheckError', 'QuotaError', 'RangeError',
  'ReadOnlyError', 'RegionCodeError', 'RequiredError', 'SizeLimitError',
  'StatsQueryError', 'StringLengthError', 'TargetError'
  """

  pass


class GoogleInternalError(ApiError):

  """Implements GoogleInternalError.

  Responsible for handling AdWords API errors
  Code: 0, 18, 55, 60, 95, 98, 117, 143, 155
  Type: 'DatabaseError', 'InternalApiError'
  """

  pass


class AccountError(ApiError):

  """Implements AccountError.

  Responsible for handling AdWords API errors
  Code: 84-86, 111, 119, 129, 139, 162-165, 183, 189
  Type: 'ClientTermsError', 'NotWhitelistedError'
  """

  pass


class WebpageError(ApiError):

  """Implements WebpageError.

  Responsible for handling AdWords API errors
  Code: 100-105
  """

  pass


class BillingError(ApiError):

  """Implements BillingError.

  Responsible for handling AdWords API errors
  Code: 50, 52, 53, 106, 107, 109, 110, 114, 118, 130, 132
  """

  pass


class AuthenticationError(ApiError):

  """Implements AuthenticationError.

  Responsible for handling AdWords API errors
  Code: 166, 184
  Type: 'AuthenticationError', 'LoasAuthenticationError'
  """

  pass


# Map error codes and types to their corresponding classes.
ERRORS = {}
ERROR_CODES = [x for x in xrange(0, 208)]
ERROR_TYPES = ['AdError', 'AdExtensionError', 'AdExtensionOverrideError',
               'AdGroupAdError', 'AdGroupCriterionError', 'AdGroupServiceError',
               'AdParamError', 'AdParamPolicyError', 'ApiError',
               'ApiUsageError', 'AudioError', 'AuthenticationError',
               'AuthorizationError', 'BidLandscapeServiceError', 'BiddingError',
               'BiddingTransitionError', 'BudgetError', 'BulkMutateJobError',
               'CampaignAdExtensionError', 'CampaignCriterionError',
               'CampaignError', 'ClientTermsError', 'CollectionSizeError',
               'CriterionPolicyError', 'DatabaseError', 'DateError',
               'DistinctError', 'GeoLocationError', 'IdError', 'ImageError',
               'InternalApiError', 'JobError', 'MediaError',
               'NewEntityCreationError', 'NotEmptyError', 'NotWhitelistedError',
               'NullError', 'OperatorError', 'PagingError',
               'PolicyViolationError', 'QuotaCheckError', 'QuotaError',
               'QuotaExceededError', 'RangeError', 'RateExceededError',
               'ReadOnlyError', 'RegionCodeError', 'RejectedError',
               'ReportDefinitionError', 'RequestError', 'RequiredError',
               'SizeLimitError', 'StatsQueryError', 'StringLengthError',
               'TargetError', 'TargetingIdeaError', 'VideoError']
for index in ERROR_CODES+ERROR_TYPES:
  if (((index >= 1 and index <= 10) or (index >= 12 and index <= 17) or
       (index >= 19 and index <= 42) or (index >= 43 and index <= 49) or
       index == 51 or index == 54 or (index >= 57 and index <= 59) or
       (index >= 61 and index <= 63) or (index >= 70 and index <= 83) or
       (index >= 87 and index <= 94) or index == 96 or index == 97 or
       index == 99 or index == 112 or index == 115 or index == 116 or
       (index >= 120 and index <= 125) or index == 127 or index == 128 or
       index == 131 or index == 133 or index == 134 or index == 137 or
       index == 138 or (index >= 140 and index <= 142) or
       (index >= 144 and index <= 147) or index == 149 or index == 153 or
       (index >= 156 and index <= 158) or (index >= 170 and index <= 174) or
       index == 176 or index == 177 or index == 186 or index == 188 or
       index == 190 or index == 206 or index == 207) or
      (index in ('AdError', 'AdExtensionError', 'AdExtensionOverrideError',
                 'AdGroupAdError', 'AdGroupCriterionError',
                 'AdGroupServiceError', 'AdParamError', 'AdParamPolicyError',
                 'ApiError', 'ApiUsageError', 'AudioError',
                 'AuthorizationError', 'BidLandscapeServiceError',
                 'BiddingError', 'BiddingTransitionError', 'BudgetError',
                 'BulkMutateJobError', 'CampaignAdExtensionError',
                 'CampaignCriterionError', 'CampaignError',
                 'CollectionSizeError', 'CriterionPolicyError', 'DateError',
                 'DistinctError', 'GeoLocationError', 'IdError', 'ImageError',
                 'JobError', 'MediaError', 'NewEntityCreationError',
                 'NotEmptyError',  'NullError', 'OperatorError', 'PagingError',
                 'PolicyViolationError', 'QuotaCheckError', 'QuotaError',
                 'QuotaExceededError', 'RangeError', 'RateExceededError',
                 'ReadOnlyError', 'RegionCodeError', 'RejectedError',
                 'ReportDefinitionError', 'RequestError', 'RequiredError',
                 'SizeLimitError', 'StatsQueryError', 'StringLengthError',
                 'TargetError', 'TargetingIdeaError', 'VideoError'))):
    ERRORS[index] = RequestError
  elif ((index == 0 or index == 18 or index == 55 or index == 60 or
         index == 95 or index == 98 or index == 117 or index == 143 or
         index == 155) or
        (index in ('InternalApiError', 'DatabaseError'))):
    ERRORS[index] = GoogleInternalError
  elif (((index >= 84 and index <= 86) or index == 111 or index == 119 or
         index == 129 or index == 139 or (index >= 162 and index <= 165) or
         index == 183 or index == 189) or
        (index in ('ClientTermsError', 'NotWhitelistedError'))):
    ERRORS[index] = AccountError
  elif ((index >= 100 and index <= 105)):
    ERRORS[index] = WebpageError
  elif ((index == 50 or index == 52 or index == 53 or index == 106 or
         index == 107 or index == 109 or index == 110 or index == 114 or
         index == 118 or index == 130 or index == 132)):
    ERRORS[index] = BillingError
  elif ((index == 166 or index == 184) or
        (index in ('AuthenticationError',))):
    ERRORS[index] = AuthenticationError
