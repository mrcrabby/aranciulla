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

"""Settings and configuration for the SOAPpy toolkit."""

import os

from adspygoogle.common import Utils
from adspygoogle.adwords import LIB_HOME


SERVICE_TYPES = []
for item in Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                                  'service_types.csv')):
  (group, ns, type, attr) = (item[0], item[1], item[2], item[3])
  SERVICE_TYPES.append({'group': group, 'ns': ns, 'type': type, 'attr': attr})
