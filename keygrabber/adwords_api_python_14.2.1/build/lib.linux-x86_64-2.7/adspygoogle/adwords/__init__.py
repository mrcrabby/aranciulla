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

"""Settings and configurations for the client library."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import pickle

from adspygoogle.common import Utils
from adspygoogle.common import VERSION
from adspygoogle.common.Errors import MissingPackageError


LIB_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LIB_NAME = 'AdWords API Python Client Library'
LIB_SHORT_NAME = 'AwApi-Python'
LIB_URL = 'http://code.google.com/p/google-api-adwords-python-lib'
LIB_AUTHOR = 'Stan Grinberg'
LIB_AUTHOR_EMAIL = 'api.sgrinberg@gmail.com'
LIB_VERSION = '14.2.1'
LIB_MIN_COMMON_VERSION = '2.0.0'
LIB_SIG = '%s-%s' % (LIB_SHORT_NAME, LIB_VERSION)

if VERSION > LIB_MIN_COMMON_VERSION:
  msg = ('Unsupported version of the core module is detected. Please download '
         'the latest version of client library at %s.' % LIB_URL)
  raise MissingPackageError(msg)

# Tuple of tuples representing API versions, where each inner tuple is a
# combination of the API vesrion and whether API used JAXB.
API_VERSIONS_MAP = (('v13', False), ('v200909', True), ('v201003', True),
                    ('v201008', True), ('v201101', True))
API_VERSIONS = [version for version, is_jaxb_api in API_VERSIONS_MAP]
MIN_API_VERSION = API_VERSIONS[4]

# Accepted combinations of headers which user has to provide. Either one of
# these is required in order to make a succesful API request.
REQUIRED_SOAP_HEADERS = (('email', 'password', 'useragent', 'developerToken'),
                         ('email', 'password', 'userAgent', 'developerToken'),
                         ('authToken', 'userAgent', 'developerToken'),
                         ('userAgent', 'developerToken'))

AUTH_TOKEN_SERVICE = 'adwords'
AUTH_TOKEN_EXPIRE = 60 * 60 * 23

ERROR_TYPES = []
for item in Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                                  'error_types.csv')):
  ERROR_TYPES.append(item[0])

# Read the defintions from the WSDL.
WSDL_MAP = pickle.load(open(os.path.join(LIB_HOME, 'data',
                                         'wsdl_type_defs.pkl'), 'r'))
OPERATIONS_MAP = pickle.load(open(os.path.join(LIB_HOME, 'data',
                                               'wsdl_ops_defs.pkl'), 'r'))

