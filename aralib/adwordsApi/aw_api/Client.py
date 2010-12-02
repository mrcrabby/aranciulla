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

"""Interface for accessing all other services."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import pickle
import re
import thread
import time

from aw_api import PYXML
from aw_api import LIB_NAME
from aw_api import LIB_SHORT_NAME
from aw_api import LIB_VERSION
from aw_api import MIN_API_VERSION
from aw_api import ZSI
from aw_api import SanityCheck
from aw_api import Utils
from aw_api.AccountService import AccountService
from aw_api.AdExtensionOverrideService import AdExtensionOverrideService
from aw_api.AdGroupAdService import AdGroupAdService
from aw_api.AdGroupCriterionService import AdGroupCriterionService
from aw_api.AdGroupService import AdGroupService
from aw_api.AdParamService import AdParamService
from aw_api.BidLandscapeService import BidLandscapeService
from aw_api.BulkMutateJobService import BulkMutateJobService
from aw_api.CampaignAdExtensionService import CampaignAdExtensionService
from aw_api.CampaignCriterionService import CampaignCriterionService
from aw_api.CampaignService import CampaignService
from aw_api.CampaignTargetService import CampaignTargetService
from aw_api.Errors import AuthTokenError
from aw_api.Errors import ValidationError
from aw_api.GeoLocationService import GeoLocationService
from aw_api.InfoService import InfoService
from aw_api.Logger import Logger
from aw_api.MediaService import MediaService
from aw_api.ReportDefinitionService import ReportDefinitionService
from aw_api.ReportService import ReportService
from aw_api.TargetingIdeaService import TargetingIdeaService
from aw_api.TrafficEstimatorService import TrafficEstimatorService
from aw_api.WebService import WebService


class Client(object):

  """Provides entry point to all web services.

  Allows instantiation of every AdWords API web service.
  """

  home = os.getcwd()
  auth_pkl = os.path.join(home, 'auth.pkl')
  config_pkl = os.path.join(home, 'config.pkl')

  def __init__(self, headers=None, config=None, path=None, use_mcc=False,
               soap_lib=None):
    """Inits Client.

    Args:
      [optional]
      headers: dict object with populated authentication credentials.
      config: dict object with client configuration values.
      path: str relative or absolute path to home directory (i.e. location of
            pickles and logs/).
      use_mcc: bool state of the API request, whether to use MCC account.
      soap_lib: str soap library to use.

        Ex:
          headers = {
            'email': 'johndoe@example.com',
            'password': 'secret',
            'clientEmail': 'client_1+johndoe@example.com',
            'clientCustomerId': '1234567890',
            'userAgent': 'GoogleTest',
            'developerToken': 'johndoe@example.com++USD',
            'validateOnly': 'n'
          }
          config = {
            'home': '/path/to/home',
            'log_home': '/path/to/logs/home',
            'soap_lib': ZSI,
            'xml_parser': PYXML,
            'debug': 'n',
            'xml_log': 'y',
            'request_log': 'y',
            'raw_response': 'n',
            'use_strict': 'y',
            'use_auth_token': 'y',
            'use_pretty_xml': 'y',
            'access': ''
          }
          path = '/path/to/home'
          use_mcc = False
          soap_lib = SOAPPY
    """
    self.__lock = thread.allocate_lock()
    self.__loc = None

    self.__is_mcc = use_mcc
    if path is not None:
      # Update absolute path for a given instance of Client, based on provided
      # relative path.
      if os.path.isabs(path):
        Client.home = path
      else:
        # NOTE(api.sgrinberg): Keep first parameter of join() as os.getcwd(),
        # do not change it to Client.home. Otherwise, may break when multiple
        # instances of Client exist during program run.
        Client.home = os.path.join(os.getcwd(), path)
      # Update location for both pickles.
      Client.auth_pkl = os.path.join(Client.home, 'auth.pkl')
      Client.config_pkl = os.path.join(Client.home, 'config.pkl')

    # Only load from the pickle if config wasn't specified.
    self.__config = config or self.__LoadConfigValues()
    self.__SetMissingDefaultConfigValues(self.__config)
    self.__config['home'] = Client.home

    # Load the SOAP library to use.
    if soap_lib is not None:
      SanityCheck.ValidateConfigSoapLib(soap_lib)
      self.__config['soap_lib'] = soap_lib

    # Validate XML parser to use.
    SanityCheck.ValidateConfigXmlParser(self.__config['xml_parser'])

    # Initialize units and operations for current instance of Client object
    # (using list to take advantage of Python's pass-by-reference).
    self.__config['units'] = [0]
    self.__config['operations'] = [0]
    self.__config['last_units'] = [0]
    self.__config['last_operations'] = [0]

    # Only load from the pickle if 'headers' wasn't specified.
    if headers is None:
      self.__headers = self.__LoadAuthCredentials()
    else:
      self.__headers = headers
    # Internally, store user agent as 'userAgent'.
    if 'useragent' in self.__headers:
      self.__headers['userAgent'] = self.__headers['useragent']
      self.__headers = Utils.UnLoadDictKeys(self.__headers, ['useragent'])
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateRequiredHeaders(self.__headers)

    # Load validateOnly header, if one was set.
    if 'validateOnly' in self.__headers:
      self.__headers['validateOnly'] = str(Utils.BoolTypeConvert(
          self.__headers['validateOnly']))

    # Load/set authentication token.
    try:
      if Utils.BoolTypeConvert(self.__config['use_auth_token']):
        if headers and 'authToken' in headers and headers['authToken']:
          self.__headers['authToken'] = headers['authToken']
        elif 'email' in self.__headers and 'password' in self.__headers:
          self.__headers['authToken'] = Utils.GetAuthToken(
              self.__headers['email'], self.__headers['password'])
        else:
          msg = 'Authentication data, email or/and password, is missing.'
          raise ValidationError(msg)
        self.__config['auth_token_epoch'] = time.time()
    except AuthTokenError:
      # We would end up here if non-valid Google Account's credentials were
      # specified. This is useful for when dummy credentials are set in
      # unit tests and requests are being made against v13. If v200909 is being
      # used and invalid credentials specified, this will be caught in
      # aw_api.WebService.CallMethod().
      self.__headers['authToken'] = None
      self.__config['auth_token_epoch'] = 0

    # Insert library name and version into userAgent.
    if (self.__headers['userAgent'].rfind(
        '%s v%s' % (LIB_SHORT_NAME, LIB_VERSION)) == -1):
      # Make sure library name shows up only once.
      if (self.__headers['userAgent'].rfind(LIB_SHORT_NAME) > -1 or
          self.__headers['userAgent'].rfind(LIB_NAME) > -1):
        pattern = re.compile('.*?: ')
        self.__headers['userAgent'] = pattern.sub('',
                                                  self.__headers['userAgent'],
                                                  1)
      self.__headers['userAgent'] = ('%s v%s: %s'
                                     % (LIB_SHORT_NAME, LIB_VERSION,
                                        self.__headers['userAgent']))

      # Sync library's version in the new userAgent with the one in the pickle.
      if headers is None:
        self.__WriteUpdatedAuthValue('userAgent', self.__headers['userAgent'])

    # Initialize logger.
    self.__logger = Logger(self.__config['log_home'])

  def __LoadAuthCredentials(self):
    """Load existing authentication credentials from auth.pkl.

    Returns:
      dict dictionary object with populated authentication credentials.
    """
    auth = {}
    if os.path.exists(Client.auth_pkl):
      fh = open(Client.auth_pkl, 'r')
      try:
        auth = pickle.load(fh)
      finally:
        fh.close()

    if not auth:
      msg = 'Authentication data is missing.'
      raise ValidationError(msg)

    return auth

  def __WriteUpdatedAuthValue(self, key, new_value):
    """Write updated authentication value for a key in auth.pkl.

    Args:
      key: str a key to update.
      new_value: str a new value to update the key with.
    """
    auth = Client.__LoadAuthCredentials(self)
    auth[key] = new_value

    # Only write to an existing pickle.
    if os.path.exists(Client.auth_pkl):
      fh = open(Client.auth_pkl, 'w')
      try:
        pickle.dump(auth, fh)
      finally:
        fh.close()

  def __LoadConfigValues(self):
    """Load existing configuration values from config.pkl.

    Returns:
      dict dictionary object with populated configuration values.
    """
    config = {}
    if os.path.exists(Client.config_pkl):
      fh = open(Client.config_pkl, 'r')
      try:
        config = pickle.load(fh)
      finally:
        fh.close()

    if not config:
      # Proceed to set default config values.
      pass

    return config

  def __SetMissingDefaultConfigValues(self, config=None):
    """Set default configuration values for missing elements in the config dict.

    Args:
      config: dict object with client configuration values.
    """
    default_config = {
        'home': Client.home,
        'log_home': os.path.join(Client.home, 'logs'),
        'soap_lib': ZSI,
        'xml_parser': PYXML,
        'debug': 'n',
        'xml_log': 'y',
        'request_log': 'y',
        'raw_response': 'n',
        'use_strict': 'y',
        'use_auth_token': 'y',
        'auth_token_epoch': 0,
        'use_pretty_xml': 'y',
        'access': ''
    }
    for key in default_config:
      if key not in config:
        config[key] = default_config[key]

  def GetAuthCredentials(self):
    """Return authentication credentials.

    Returns:
      dict authentiaction credentials.
    """
    return self.__headers

  def GetConfigValues(self):
    """Return configuration values.

    Returns:
      dict configuration values.
    """
    return self.__config

  def GetUnits(self):
    """Return number of API units consumed by current instance of Client object.

    Returns:
      int number of API units.
    """
    return self.__config['units'][0]

  def GetOperations(self):
    """Return number of API ops performed by current instance of Client object.

    Returns:
      int number of API operations.
    """
    return self.__config['operations'][0]

  def GetLastUnits(self):
    """Return number of API units consumed by last API call.

    Returns:
      int number of API units.
    """
    return self.__config['last_units'][0]

  def GetLastOperations(self):
    """Return number of API ops performed by last API call.

    Returns:
      int number of API operations.
    """
    return self.__config['last_operations'][0]

  def UseMcc(self, state):
    """Choose to make an API request against MCC account or a sub-account.

    Args:
      state: bool state of the API request, whether to use MCC.
    """
    self.__is_mcc = False
    if state:
      self.__is_mcc = True

  def __GetUseMcc(self):
    """Return current state of the API request.

    Returns:
      bool state of the API request, whether to use MCC.
    """
    return self.__is_mcc

  def __SetUseMcc(self, state):
    """Chooses to make an API request against MCC account or a sub-account.

    Args:
      state: bool state of the API request, whether to use MCC.
    """
    self.__is_mcc = state

  use_mcc = property(__GetUseMcc, __SetUseMcc)

  def __GetSoapLlib(self):
    """Return current value of the SOAP library in use.

    Returns:
      str value of the SOAP library in use.
    """
    return self.__config['soap_lib']

  def __SetSoapLib(self, soap_lib):
    """Change the SOAP library to use.

    Args:
      soap_lib: str value of the SOAP library to use.
    """
    SanityCheck.ValidateConfigSoapLib(soap_lib)
    self.__config['soap_lib'] = soap_lib

  soap_lib = property(__GetSoapLlib, __SetSoapLib)

  def SetClientEmail(self, client_email):
    """Temporarily change client email for a given Client instance.

    Args:
      client_email: str new client email to use.
    """
    if ('clientEmail' not in self.__headers or
        self.__headers['clientEmail'] != client_email):
      self.__headers['clientEmail'] = client_email
      self.__headers['clientCustomerId'] = ''

  def SetClientCustomerId(self, client_customer_id):
    """Temporarily change client customer id for a given Client instance.

    Args:
      client_customer_id: str new client customer id to use.
    """
    if ('clientCustomerId' not in self.__headers or
        self.__headers['clientCustomerId'] != client_customer_id):
      self.__headers['clientCustomerId'] = client_customer_id
      self.__headers['clientEmail'] = ''

  def SetDebug(self, new_state):
    """Temporarily change debug mode for a given Client instance.

    Args:
      new_state: bool new state of the debug mode.
    """
    self.__config['debug'] = Utils.BoolTypeConvert(new_state)

  def __GetDebug(self):
    """Return current state of the debug mode.

    Returns:
      bool state of the debug mode.
    """
    return self.__config['debug']

  def __SetDebug(self, new_state):
    """Temporarily change debug mode for a given Client instance.

    Args:
      new_state: bool new state of the debug mode.
    """
    self.__config['debug'] = Utils.BoolTypeConvert(new_state)

  debug = property(__GetDebug, __SetDebug)

  def __GetUseStrict(self):
    """Return current state of the strictness mode.

    Returns:
      str state of the strictness mode.
    """
    return self.__config['use_strict']

  def __SetUseStrict(self, new_state):
    """Temporarily change strictness mode for a given Client instance.

    Args:
      new_state: bool new state of the strictness mode.
    """
    self.__config['use_strict'] = Utils.BoolTypeConvert(new_state)

  use_strict = property(__GetUseStrict, __SetUseStrict)

  def __GetValidateOnly(self):
    """Return current state of the validation mode.

    Returns:
      bool state of the validation mode.
    """
    return self.__headers['validateOnly']

  def __SetValidateOnly(self, new_state):
    """Temporarily change validation mode for a given Client instance.

    Args:
      new_state: bool new state of the validation mode.
    """
    self.__headers['validateOnly'] = str(new_state)

  validate_only = property(__GetValidateOnly, __SetValidateOnly)

  def __GetXmlParser(self):
    """Return current state of the xml parser in use.

    Returns:
      bool state of the xml parser in use.
    """
    return self.__config['xml_parser']

  def __SetXmlParser(self, new_state):
    """Temporarily change xml parser in use for a given Client instance.

    Args:
      new_state: bool new state of the xml parser to use.
    """
    self.__config['xml_parser'] = Utils.BoolTypeConvert(new_state)

  xml_parser = property(__GetXmlParser, __SetXmlParser)

  def __GetAuthCredentialsForAccessLevel(self):
    """Return auth credentials based on the access level of the request.

    Request can have an MCC level access or a sub account level access.

    Returns:
      dict authentiaction credentials.
    """
    old_headers = self.GetAuthCredentials()
    new_headers = {}
    is_mcc = self.__is_mcc

    for key, value in old_headers.iteritems():
      new_headers[key] = value
      if key == 'clientEmail' or key == 'clientCustomerId':
        if is_mcc and 'email' in old_headers:
          new_headers[key] = None

    if (('clientEmail' in new_headers and 'clientCustomerId' in new_headers) and
        new_headers['clientEmail'] == new_headers['clientCustomerId']):
      new_headers['clientCustomerId'] = None

    return new_headers

  def CallRawMethod(self, soap_message, url, http_proxy):
    """Call API method directly, using raw SOAP message.

    For API calls performed with this method, outgoing data is not run through
    library's validation logic.

    Args:
      soap_message: str SOAP XML message.
      url: str URL of the API service for the method to call.
      http_proxy: str HTTP proxy to use for this API call.

    Returns:
      tuple response from the API method (SOAP XML response message).
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    # Load additional configuration data.
    op_config = {'http_proxy': http_proxy}

    service = WebService(headers, self.__config, op_config, url, self.__lock,
                         self.__logger)
    return service.CallRawMethod(soap_message)

  def CallMethod(self, url, method, params, http_proxy):
    """Call API method directly, using its service's URL.

    For API calls performed with this method, outgoing data is not run through
    library's validation logic.

    Args:
      url: str URL of the API service for the method to call.
      method: str name of the API method to call.
      params: list list of parameters to send to the API method.
      http_proxy: str HTTP proxy to use for this API call.

    Returns:
      tuple response from the API method.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    # Load additional configuration data.
    op_config = {
      'server': Utils.GetServerFromUrl(url),
      'version': Utils.GetVersionFromUrl(url),
      'http_proxy': http_proxy
    }

    service = WebService(headers, self.__config, op_config, url, self.__lock,
                         self.__logger)

    if self.__config['soap_lib'] == ZSI:
      # Check format of parameters. Example of valid formats,
      # - ()
      # - ({'dummy': 0},)
      # - ({'campaignIds': ['11111']},
      #    {'startDay': '2008-07-01'},
      #    {'endDay': '2008-07-31'})
      #
      # TODO(api.sgrinberg: Figure out how to match the order of params with
      # those in Holder object below. Then, we don't need to require client code
      # to provide key/value pairs, just values will be enough (see, issue# 31).
      try:
        SanityCheck.ValidateTypes(((params, tuple),))
        for item in params:
          SanityCheck.ValidateTypes(((item, dict),))
      except ValidationError:
        msg = 'Invalid format of parameters, expecting a tuple of dicts.'
        raise ValidationError(msg)

      # From the URL, get service being accessed and version used.
      url_parts = url.split('/')
      service_name = url_parts[len(url_parts) - 1].split('Service')[0]
      version = url_parts[len(url_parts) - 2]

      from aw_api import API_VERSIONS
      if version in API_VERSIONS:
        web_services = __import__('aw_api.zsi_toolkit.%s.%sService_services'
                                  % (version, service_name), globals(),
                                  locals(), [''])
      else:
        msg = 'Invalid API version, not one of %s.' % str(list(API_VERSIONS))
        raise ValidationError(msg)
      eval('%sService' % service_name).web_services = web_services
      self.__loc = eval(('%sService.web_services.%sServiceLocator()'
                         % (service_name, service_name)))
      request = eval('%sService.web_services.%sRequest()' % (service_name,
                                                             method))
      return service.CallMethod(method, (params), service_name, self.__loc,
                                request)
    else:
      return service.CallMethod(method, (params))

  def GetAccountService(self, server='https://adwords.google.com',
                        version=None, http_proxy=None):
    """Call API method in AccountService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AccountService new instance of AccountService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return AccountService(headers, self.__config, op_config, self.__lock,
                          self.__logger)

  def GetAdExtensionOverrideService(self, server='https://adwords.google.com',
                                    version=None, http_proxy=None):
    """Call API method in AdExtensionOverrideService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdExtensionOverrideService new instance of AdExtensionOverrideService
                                 object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return AdExtensionOverrideService(headers, self.__config, op_config,
                                      self.__lock, self.__logger)

  def GetAdGroupAdService(self, server='https://adwords.google.com',
                          version=None, http_proxy=None):
    """Call API method in AdGroupAdService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdGroupAdService new instance of AdGroupAdService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return AdGroupAdService(headers, self.__config, op_config, self.__lock,
                            self.__logger)

  def GetAdGroupCriterionService(self, server='https://adwords.google.com',
                                 version=None, http_proxy=None):
    """Call API method in AdGroupCriterionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdGroupCriterionService new instance of AdGroupCriterionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return AdGroupCriterionService(headers, self.__config, op_config,
                                   self.__lock, self.__logger)

  def GetAdGroupService(self, server='https://adwords.google.com',
                        version=None, http_proxy=None):
    """Call API method in AdGroupService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdGroupService new instance of AdGroupService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return AdGroupService(headers, self.__config, op_config, self.__lock,
                          self.__logger)

  def GetAdParamService(self, server='https://adwords.google.com',
                      version=None, http_proxy=None):
    """Call API method in AdParamService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      AdParamService new instance of AdParamService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return AdParamService(headers, self.__config, op_config, self.__lock,
                          self.__logger)

  def GetBidLandscapeService(self, server='https://adwords.google.com',
                             version=None, http_proxy=None):
    """Call API method in BidLandscapeService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      BidLandscapeService new instance of BidLandscapeService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return BidLandscapeService(headers, self.__config, op_config, self.__lock,
                               self.__logger)

  def GetBulkMutateJobService(self, server='https://adwords.google.com',
                           version=None, http_proxy=None):
    """Call API method in BulkMutateJobService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      BulkMutateJobService new instance of BulkMutateJobService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return BulkMutateJobService(headers, self.__config, op_config, self.__lock,
                                self.__logger)

  def GetCampaignAdExtensionService(self, server='https://adwords.google.com',
                                    version=None, http_proxy=None):
    """Call API method in CampaignAdExtensionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CampaignAdExtensionService new instance of CampaignAdExtensionService
                                 object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return CampaignAdExtensionService(headers, self.__config, op_config,
                                      self.__lock, self.__logger)

  def GetCampaignCriterionService(self, server='https://adwords.google.com',
                                  version=None, http_proxy=None):
    """Call API method in CampaignCriterionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CampaignCriterionService new instance of CampaignCriterionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return CampaignCriterionService(headers, self.__config, op_config,
                                    self.__lock, self.__logger)

  def GetCampaignService(self, server='https://adwords.google.com',
                         version=None, http_proxy=None):
    """Call API method in CampaignService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CampaignService new instance of CampaignService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return CampaignService(headers, self.__config, op_config, self.__lock,
                           self.__logger)

  def GetCampaignTargetService(self, server='https://adwords.google.com',
                               version=None, http_proxy=None):
    """Call API method in CampaignTargetService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      CampaignTargetService new instance of CampaignTargetService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return CampaignTargetService(headers, self.__config, op_config, self.__lock,
                                 self.__logger)

  def GetGeoLocationService(self, server='https://adwords.google.com',
                            version=None, http_proxy=None):
    """Call API method in GeoLocationService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      GeoLocationService new instance of GeoLocationService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return GeoLocationService(headers, self.__config, op_config, self.__lock,
                              self.__logger)

  def GetInfoService(self, server='https://adwords.google.com', version=None,
                     http_proxy=None):
    """Call API method in InfoService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      InfoService new instance of InfoService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'info',
      'http_proxy': http_proxy
    }

    return InfoService(headers, self.__config, op_config, self.__lock,
                       self.__logger)

  def GetMediaService(self, server='https://adwords.google.com', version=None,
                      http_proxy=None):
    """Call API method in MediaService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      MediaService new instance of MediaService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return MediaService(headers, self.__config, op_config, self.__lock,
                        self.__logger)

  def GetReportDefinitionService(self, server='https://adwords.google.com',
                                 version=None, http_proxy=None):
    """Call API method in ReportDefinitionService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' or
              'https://adwords-sandbox.google.com' for sandbox. The default
              behavior is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ReportDefinitionService new instance of ReportDefinitionService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'cm',
      'http_proxy': http_proxy
    }

    return ReportDefinitionService(headers, self.__config, op_config,
                                   self.__lock, self.__logger)

  def GetReportService(self, server='https://adwords.google.com', version=None,
                       http_proxy=None):
    """Call API method in ReportService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      ReportService new instance of ReportService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return ReportService(headers, self.__config, op_config, self.__lock,
                         self.__logger)

  def GetTargetingIdeaService(self, server='https://adwords.google.com',
                              version=None, http_proxy=None):
    """Call API method in TargetingIdeaService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      TargetingIdeaService new instance of TargetingIdeaService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'group': 'o',
      'http_proxy': http_proxy
    }

    return TargetingIdeaService(headers, self.__config, op_config,
                                self.__lock, self.__logger)

  def GetTrafficEstimatorService(self, server='https://adwords.google.com',
                                 version=None, http_proxy=None):
    """Call API method in TrafficEstimatorService.

    Args:
      [optional]
      server: str API server to access for this API call. Possible
              values are: 'https://adwords.google.com' for live site and
              'https://sandbox.google.com' for sandbox. The default behavior
              is to access live site.
      version: str API version to use.
      http_proxy: str HTTP proxy to use.

    Returns:
      TrafficEstimatorService new instance of TrafficEstimatorService object.
    """
    headers = self.__GetAuthCredentialsForAccessLevel()

    if version is None:
      version = MIN_API_VERSION
    if Utils.BoolTypeConvert(self.__config['use_strict']):
      SanityCheck.ValidateServer(server, version)

    # Load additional configuration data.
    op_config = {
      'server': server,
      'version': version,
      'http_proxy': http_proxy
    }

    return TrafficEstimatorService(headers, self.__config, op_config,
                                   self.__lock, self.__logger)
