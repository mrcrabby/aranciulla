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

"""Unit tests to cover UserListService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import time
import unittest

from adspygoogle.common import Utils
from tests.adspygoogle.adwords import HTTP_PROXY
from tests.adspygoogle.adwords import SERVER_V201008
from tests.adspygoogle.adwords import SERVER_V201101
from tests.adspygoogle.adwords import VERSION_V201008
from tests.adspygoogle.adwords import VERSION_V201101
from tests.adspygoogle.adwords import client


class UserListServiceTestV201008(unittest.TestCase):

  """Unittest suite for UserListService using v201008."""

  SERVER = SERVER_V201008
  VERSION = VERSION_V201008
  client.debug = False
  service = None
  user_list = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserListService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testAddLogicalUserList(self):
    """Test whether we can add a logical user list."""
    if self.__class__.user_list is None:
      self.testAddRemarketingUserList()
    operations = [
        {
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'LogicalUserList',
                'name': 'Mars cruise customers #%s' % Utils.GetUniqueName(),
                'description': 'A list of mars cruise customers in the last '
                               'year.',
                'membershipLifeSpan': '365',
                'rules': [
                    {
                        'operator': 'ALL',
                        'ruleOperands': [
                            {
                                'xsi_type': 'RemarketingUserList',
                                'id': self.__class__.user_list['id']
                            }
                        ]
                    }
                ]
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddRemarketingUserList(self):
    """Test whether we can add a remarketing user list."""
    operations = [
        {
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'RemarketingUserList',
                'name': 'Mars cruise customers #%s' % Utils.GetUniqueName(),
                'description': 'A list of mars cruise customers in the last '
                               'year.',
                'membershipLifeSpan': '365',
                'conversionTypes': [
                    {
                        'name': ('Mars cruise customers #%s'
                                 % Utils.GetUniqueName())
                    }
                ]
            }
        }
    ]
    user_lists = self.__class__.service.Mutate(operations)
    self.__class__.user_list = user_lists[0]['value'][0]
    self.assert_(isinstance(user_lists, tuple))

  def testDeleteUserList(self):
    """Test whether we can delete an existing user list."""
    if self.__class__.user_list is None:
      self.testAddRemarketingUserList()
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'xsi_type': 'RemarketingUserList',
                'id': self.__class__.user_list['id'],
                'status': 'CLOSED'
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testUpdateUserList(self):
    """Test whether we can update an existing user list."""
    if self.__class__.user_list is None:
      self.testAddRemarketingUserList()
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'xsi_type': 'RemarketingUserList',
                'id': self.__class__.user_list['id'],
                'description': 'Last updated at %s' % time.ctime(),
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testGetAllUserLists(self):
    """Test whether we can retrieve all user lists."""
    selector = {}
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))


class UserListServiceTestV201101(unittest.TestCase):

  """Unittest suite for UserListService using v201101."""

  SERVER = SERVER_V201101
  VERSION = VERSION_V201101
  client.debug = False
  service = None
  user_list = None

  def setUp(self):
    """Prepare unittest."""
    print self.id()
    if not self.__class__.service:
      self.__class__.service = client.GetUserListService(
          self.__class__.SERVER, self.__class__.VERSION, HTTP_PROXY)

  def testAddLogicalUserList(self):
    """Test whether we can add a logical user list."""
    if self.__class__.user_list is None:
      self.testAddRemarketingUserList()
    operations = [
        {
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'LogicalUserList',
                'name': 'Mars cruise customers #%s' % Utils.GetUniqueName(),
                'description': ('A list of mars cruise customers in the last ' +
                                'year.'),
                'membershipLifeSpan': '365',
                'rules': [
                    {
                        'operator': 'ALL',
                        'ruleOperands': [
                            {
                                'xsi_type': 'RemarketingUserList',
                                'id': self.__class__.user_list['id']
                            }
                        ]
                    }
                ]
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testAddRemarketingUserList(self):
    """Test whether we can add a remarketing user list."""
    operations = [
        {
            'operator': 'ADD',
            'operand': {
                'xsi_type': 'RemarketingUserList',
                'name': 'Mars cruise customers #%s' % Utils.GetUniqueName(),
                'description': ('A list of mars cruise customers in the last ' +
                                'year.'),
                'membershipLifeSpan': '365',
                'conversionTypes': [
                    {
                        'name': ('Mars cruise customers #%s'
                                 % Utils.GetUniqueName())
                    }
                ]
            }
        }
    ]
    user_lists = self.__class__.service.Mutate(operations)
    self.__class__.user_list = user_lists[0]['value'][0]
    self.assert_(isinstance(user_lists, tuple))

  def testDeleteUserList(self):
    """Test whether we can delete an existing user list."""
    if self.__class__.user_list is None:
      self.testAddRemarketingUserList()
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'xsi_type': 'RemarketingUserList',
                'id': self.__class__.user_list['id'],
                'status': 'CLOSED'
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testUpdateUserList(self):
    """Test whether we can update an existing user list."""
    if self.__class__.user_list is None:
      self.testAddRemarketingUserList()
    operations = [
        {
            'operator': 'SET',
            'operand': {
                'xsi_type': 'RemarketingUserList',
                'id': self.__class__.user_list['id'],
                'description': 'Last updated at %s' % time.ctime(),
            }
        }
    ]
    self.assert_(isinstance(self.__class__.service.Mutate(operations), tuple))

  def testGetAllUserLists(self):
    """Test whether we can retrieve all user lists."""
    selector = {
        'fields': ['Id', 'Name', 'Status']
    }
    self.assert_(isinstance(self.__class__.service.Get(selector), tuple))


def makeTestSuiteV201008():
  """Set up test suite using v201008.

  Returns:
    TestSuite test suite using v201008.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserListServiceTestV201008))
  return suite


def makeTestSuiteV201101():
  """Set up test suite using v201101.

  Returns:
    TestSuite test suite using v201101.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(UserListServiceTestV201101))
  return suite


if __name__ == '__main__':
  suite_v201008 = makeTestSuiteV201008()
  suite_v201101 = makeTestSuiteV201101()
  alltests = unittest.TestSuite([suite_v201008, suite_v201101])
  unittest.main(defaultTest='alltests')
