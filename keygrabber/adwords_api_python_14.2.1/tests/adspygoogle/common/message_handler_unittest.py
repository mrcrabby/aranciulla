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

"""Unit tests to cover message handler."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common.soappy import MessageHandler as SoappyMessageHandler
from adspygoogle.common.zsi import MessageHandler as ZsiMessageHandler
from tests.adspygoogle.common import client


class MessageHandlerTest(unittest.TestCase):

  """Unittest suite for MessageHandler."""

  client.debug = False
  TYPES_MAP = {
      'Predicate': {
          'has_native_type': True,
          'base_type': '',
          'soap_type': 'complex',
          'parameters': (['field', 'xsd:string'],
                         ['type', 'Test.Status'],
                         ['values', 'ArrayOf_xsd_string'])
      },
      'ObjectSearchCriteria': {
          'has_native_type': False,
          'base_type': 'PageableSearchCriteriaBase',
          'soap_type': 'complex',
          'parameters': (['objectGroupIds', 'ArrayOf_xsd_long'],
                         ['includeObjectsWithOutGroupOnly', 'xsd:boolean'],
                         ['spotIds', 'ArrayOf_xsd_long'],
                         ['subnetworkId', 'xsd:long'])
      },
      'PredicatePage': {
          'has_native_type': False,
          'base_type': 'Page',
          'soap_type': 'complex',
          'parameters': (['entries', 'ArrayOf_Predicate'],)
      },
      'Test.Status': {
          'base_type': 'xsd:string',
          'soap_type': 'simple',
          'allowed_values': ('ENABLED', 'PAUSED', 'DELETED')
      },
      'ArrayOf_xsd_string': {
          'base_type': 'xsd:string',
          'soap_type': 'array'
      },
      'ArrayOf_Predicate': {
          'base_type': 'Predicate',
          'soap_type': 'array'
      },
      'ObjectRecordSet': {
          'has_native_type': False,
          'base_type': 'PagedRecordSet',
          'soap_type': 'complex',
          'parameters': (['records', 'ArrayOfObject'],)
      },
      'PageableSearchCriteriaBase': {
          'has_native_type': False,
          'base_type': 'SearchCriteriaBase',
          'soap_type': 'complex',
          'parameters': (['pageNumber', 'xsd:int'],
                         ['pageSize', 'xsd:int'])
      },
      'ArrayOf_xsd_long': {
          'base_type': 'xsd:long',
          'soap_type': 'array'
      },
      'PagedRecordSet': {
          'has_native_type': False,
          'base_type': '',
          'soap_type': 'complex',
          'parameters': (['pageNumber', 'xsd:int'],
                         ['totalNumberOfPages', 'xsd:int'],
                         ['totalNumberOfRecords', 'xsd:int'])
      },
      'Page': {
          'has_native_type': False,
          'base_type': '',
          'soap_type': 'complex',
          'parameters': (['totalNumEntries', 'xsd:int'],
                         ['Page.Type', 'xsd:string'])
      },
      'SearchCriteriaBase': {
          'has_native_type': False,
          'base_type': '',
          'soap_type': 'complex',
          'parameters': (['ids', 'ArrayOf_xsd_long'],
                         ['searchString', 'soapenc:string'])
      }
  }

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testCustomPackListEmptyList(self):
    """Test whether function can handle an empty list."""
    obj = ZsiMessageHandler.CustomPackList([])
    self.assert_(isinstance(obj, dict))

  def testCustomPackList(self):
    """Test whether function can handle a list."""
    lst = [{'languages': 'en'}, {'languages': 'iw'}]
    obj = ZsiMessageHandler.CustomPackList(lst)
    self.assert_(isinstance(obj, dict))
    self.assertEqual(len(obj.keys()), 1)
    self.assert_('languages' in obj)
    self.assertEqual(len(obj['languages']), 2)

  def testRestoreListTypesWithWsdl(self):
    """Test whether list types are properly restored using WSDL definitions."""
    response = ({
        'entries': {
            'field': 'fieldval',
            'type': 'PAUSED',
            'values': 'values'
        }
    },)
    expected_output = ({
        'entries': [{
            'field': 'fieldval',
            'type': 'PAUSED',
            'values': ['values']
        }]
    },)
    self.assertEqual(SoappyMessageHandler.RestoreListTypeWithWsdl(
        response, self.__class__.TYPES_MAP, ['PredicatePage']), expected_output)

  def testPackVarAsXml(self):
    """Test the functionality of WSDL-based SOAPpy object packing."""
    predicate_page = {
        'entries': [
            {
                'field': 'Any string works.',
                'type': 'PAUSED',
                'values': ['1', 'True', 'str'],
            },
            {
                'field': '1234567890',
                'type': 'DELETED',
                'values': []
            }
        ]
    }
    expected_output = ('<predicatePages xsi3:type="PredicatePage"><entries '
                       'xsi3:type="Predicate"><field>Any string works.</field>'
                       '<type>PAUSED</type><values>1</values><values>True'
                       '</values><values>str</values></entries><entries '
                       'xsi3:type="Predicate"><field>1234567890</field><type>'
                       'DELETED</type></entries></predicatePages>')
    self.assertEqual(SoappyMessageHandler.PackVarAsXml(
        predicate_page, 'predicatePages', self.__class__.TYPES_MAP, False,
        'PredicatePage'), expected_output)

    object_search_critera = {
        'xsi_type': 'ObjectSearchCriteria',
        'objectGroupIds': ['1', '2'],
        'searchString': 'What is this?',
        'includeObjectsWithOutGroupOnly': 'True'
    }
    expected_output = ('<searchCriteria xsi3:type="ObjectSearchCriteria">'
                       '<searchString>What is this?</searchString>'
                       '<objectGroupIds xsi3:type="ArrayOf_xsd_long">'
                       '<objectGroupIds>1</objectGroupIds><objectGroupIds>2'
                       '</objectGroupIds></objectGroupIds>'
                       '<includeObjectsWithOutGroupOnly>True'
                       '</includeObjectsWithOutGroupOnly></searchCriteria>')
    self.assertEqual(SoappyMessageHandler.PackVarAsXml(
        object_search_critera, 'searchCriteria', self.__class__.TYPES_MAP,
        True, 'PageableSearchCriteriaBase'), expected_output)

  def testPackVarAsXmlNoWsdl(self):
    """Test the functionality of new SOAPpy object packing with no WSDL."""
    object_search_critera = {
        'xsi_type': 'ObjectSearchCriteria',
        'objectGroupIds': ['1', '2'],
        'searchString': 'What is this?',
        'includeObjectsWithOutGroupOnly': 'True'
    }
    expected_output = ('<searchCriteria xsi3:type="ObjectSearchCriteria">'
                       '<searchString>What is this?</searchString>'
                       '<includeObjectsWithOutGroupOnly>True'
                       '</includeObjectsWithOutGroupOnly><objectGroupIds>1'
                       '</objectGroupIds><objectGroupIds>2</objectGroupIds>'
                       '</searchCriteria>')
    self.assertEqual(SoappyMessageHandler.PackVarAsXml(
        object_search_critera, 'searchCriteria'), expected_output)

    del object_search_critera['xsi_type']
    expected_output = ('<searchCriteria><searchString>What is this?'
                       '</searchString><includeObjectsWithOutGroupOnly>True'
                       '</includeObjectsWithOutGroupOnly><objectGroupIds>1'
                       '</objectGroupIds><objectGroupIds>2</objectGroupIds>'
                       '</searchCriteria>')
    self.assertEqual(SoappyMessageHandler.PackVarAsXml(
        object_search_critera, 'searchCriteria'), expected_output)


def makeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(MessageHandlerTest))
  return suite


if __name__ == '__main__':
  suite = makeTestSuite()
  alltests = unittest.TestSuite([suite])
  unittest.main(defaultTest='alltests')
