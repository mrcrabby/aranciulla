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

"""Settings and configuration for the client library."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os


LIB_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LIB_NAME = 'AdWords API Python Client Library'
LIB_SHORT_NAME = 'AWAPI PyLib'
LIB_URL = 'http://code.google.com/p/google-api-adwords-python-lib'
LIB_AUTHOR = 'Stan Grinberg'
LIB_AUTHOR_EMAIL = 'api.sgrinberg@gmail.com'
LIB_VERSION = '11.1.1'

API_VERSIONS = ('v13', 'v200909', 'v201003')
MIN_API_VERSION = API_VERSIONS[0]
SOAPPY = '1'
ZSI = '2'

MIN_PY_VERSION = '2.4.4'
PYXML_NAME = 'PyXML'
ETREE_NAME = 'ElementTree'
MIN_PYXML_VERSION = '0.8.3'
MIN_ETREE_VERSION = '1.2.6'
PYXML = '1'
ETREE = '2'

AUTH_TOKEN_SERVICE = 'adwords'
AUTH_TOKEN_EXPIRE = 60 * 60 * 23

# Maximum limit for the number of allowed target namespaces in a single service.
MAX_TARGET_NAMESPACE = 3
