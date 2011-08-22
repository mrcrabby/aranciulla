#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Settings and configuration for the unit tests."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))

from adspygoogle.adwords.AdWordsClient import AdWordsClient
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI


HTTP_PROXY = None
SERVER_V13 = 'https://sandbox.google.com'
SERVER_V200909 = 'https://adwords-sandbox.google.com'
SERVER_V201003 = 'https://adwords-sandbox.google.com'
SERVER_V201008 = 'https://adwords-sandbox.google.com'
SERVER_V201101 = 'https://adwords-sandbox.google.com'
VERSION_V13 = 'v13'
VERSION_V200909 = 'v200909'
VERSION_V201003 = 'v201003'
VERSION_V201008 = 'v201008'
VERSION_V201101 = 'v201101'
client = AdWordsClient(path=os.path.join('..', '..', '..'))
