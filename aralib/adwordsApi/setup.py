#!/usr/bin/python
#
# Copyright 2010 Google Inc.
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

"""Setup script for the AdWords API Python Client Library."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
from distutils.core import setup

from aw_api import LIB_AUTHOR
from aw_api import LIB_AUTHOR_EMAIL
from aw_api import LIB_NAME
from aw_api import LIB_URL
from aw_api import LIB_VERSION


PACKAGES = ['aw_api', 'aw_api.soappy_toolkit', 'aw_api.zsi_toolkit',
            'aw_api.zsi_toolkit.v13', 'aw_api.zsi_toolkit.v200909',
            'aw_api.zsi_toolkit.v201003']
PACKAGE_DATA = {'aw_api': [os.path.join('data', '*.csv')]}


setup(name='aw_api',
      version=LIB_VERSION,
      description=LIB_NAME,
      author=LIB_AUTHOR,
      author_email=LIB_AUTHOR_EMAIL,
      maintainer=LIB_AUTHOR,
      maintainer_email=LIB_AUTHOR_EMAIL,
      url=LIB_URL,
      license='Apache License 2.0',
      long_description='For additional information, please see %s' % LIB_URL,
      packages=PACKAGES,
      package_data=PACKAGE_DATA)
