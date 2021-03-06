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

"""Script to pack the AdWords API Python client library into a .tar.gz ball."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import shutil
import sys
sys.path.append('..')

from aw_api import LIB_VERSION


LIB_DIR = os.path.abspath('..')
LIB_TAG = 'awapi_python_lib_%s' % LIB_VERSION
TARGET_DIR = '/usr/local/lib/py/%s' % LIB_TAG

# If there is an existing copy of the target directory, remove it.
if os.path.exists(os.path.abspath(TARGET_DIR)):
  shutil.rmtree(os.path.abspath(TARGET_DIR))

# Recursively copy client library code into target directory.
shutil.copytree(LIB_DIR, TARGET_DIR)

# Perform clean up, generated docs, and adjust permissions.
os.chdir(TARGET_DIR)
os.system('find docs \( -not -name \'docs\' -and -not -name \'README\' \) | '
          'xargs rm')
os.system('epydoc -q --name "AdWords API Python Client Library" --url '
          '"http://code.google.com/p/google-api-adwords-python-lib/" '
          '--html aw_api --exclude=_services -o docs')
os.system('perl -pi -e \'s/Generated by Epydoc (\d+\.\d+\.\d+) .*/Generated '
          'by Epydoc $1/\' docs/*')
os.system('find . \( -name \'*.pkl\' -or -name \'*.log\' -or -name \'*.pyc\' '
          '-or -name \'.project\' -or -name \'.pydevproject\' -or -name '
          '\'.settings\' \) | xargs rm -fr')

# Package target directory into .tar.gz and adjust permissions.
os.chdir(os.path.abspath(os.path.join(TARGET_DIR, '..')))
os.system('tar -cf %s.tar %s/' % (LIB_TAG, LIB_TAG))
os.system('gzip %s.tar' % LIB_TAG)
