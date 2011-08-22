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

"""Unit tests to cover WSDL-based SanityCheck."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from adspygoogle.common import SanityCheck
from adspygoogle.common.Errors import ValidationError


class SanityCheckTest(unittest.TestCase):

  """Unittest suite for SanityCheck."""

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

  def testSimpleTypeIsCorrectDataType(self):
    """Test if Sanity Check enforces correct data types on simple types."""
    test_status = 25
    self.assertRaises(ValidationError, SanityCheck.NewSanityCheck,
                      self.__class__.TYPES_MAP, test_status, 'Test.Status')

  def testSimpleTypeIsNotAllowedValue(self):
    """Test if Sanity Check detects a simple type value that is not allowed."""
    test_status = 'DISABLED'
    self.assertRaises(ValidationError, SanityCheck.NewSanityCheck,
                      self.__class__.TYPES_MAP, test_status, 'Test.Status')

  def testAllowedSimpleTypeValuesSucceed(self):
    """Test that Sanity Check does not fail on allowed simple type values."""
    for enum in self.__class__.TYPES_MAP['Test.Status']['allowed_values']:
      SanityCheck.NewSanityCheck(self.__class__.TYPES_MAP, enum, 'Test.Status')

  def testSanityCheckArrayIsCorrectDataType(self):
    """Test whether Sanity Check enforces correct data types on array types."""
    test_array = 'test'
    self.assertRaises(ValidationError, SanityCheck.NewSanityCheck,
                      self.__class__.TYPES_MAP, test_array,
                      'ArrayOf_xsd_string')

  def testSanityCheckArrayContentsAreCorrectDataType(self):
    """Test if Sanity Check enforces correct data types on array contents."""
    test_array = ['Yes', 'No', 10]
    self.assertRaises(ValidationError, SanityCheck.NewSanityCheck,
                      self.__class__.TYPES_MAP, test_array,
                      'ArrayOf_xsd_string')

  def testAllowedArrayTypeValuesSucceed(self):
    """Test that Sanity Check does not fail on allowed array type values."""
    SanityCheck.NewSanityCheck(self.__class__.TYPES_MAP, ['1', '2'],
                               'ArrayOf_xsd_string')

    predicate = {
        'field': 'string',
        'type': 'ENABLED',
        'values': ['strings', '10', 'True']
    }
    SanityCheck.NewSanityCheck(self.__class__.TYPES_MAP, [predicate],
                               'ArrayOf_Predicate')

  def testSanityCheckComplexTypeIsCorrectDataType(self):
    """Test if Sanity Check enforces correct data types on complex types."""
    test_complex = [['field', 'string'], ['type', 'ENABLED'], ['values', []]]
    self.assertRaises(ValidationError, SanityCheck.NewSanityCheck,
                      self.__class__.TYPES_MAP, test_complex,
                      'PredicatePage')

  def testSanityCheckComplexContentIsCorrectDataType(self):
    """Test if Sanity Check enforces correct data types on complex contents."""
    pageable_search_criteria = {
        'pageNumber': 1
    }
    self.assertRaises(ValidationError, SanityCheck.NewSanityCheck,
                      self.__class__.TYPES_MAP, pageable_search_criteria,
                      'PageableSearchCriteriaBase')

  def testComplexTypeContainsNotAllowedField(self):
    """Test if Sanity Check detects a complex type field that is not allowed."""
    object_search_criteria = {
        'searchString': 'searching',
        'pageNumber': '1',
        'includeObjectsWithOutGroupOnly': 'True',
        'madeUpField': 'I\'m not real!'
    }
    self.assertRaises(ValidationError, SanityCheck.NewSanityCheck,
                      self.__class__.TYPES_MAP, object_search_criteria,
                      'ObjectSearchCriteria')

  def testSanityCheckComplexSuperTypes(self):
    """Test whether Sanity Check allows subtypes to use supertype fields."""
    object_search_criteria = {
        'searchString': 'searching',
        'pageNumber': '1',
        'includeObjectsWithOutGroupOnly': 'True'
    }
    SanityCheck.NewSanityCheck(self.__class__.TYPES_MAP, object_search_criteria,
                               'ObjectSearchCriteria')

  def testSanityCheckComplexWithExplcitType(self):
    """Test if Sanity Check recognizes an xsi type declared in an object."""
    object_search_criteria = {
        'searchString': 'searching',
        'pageNumber': '1',
        'includeObjectsWithOutGroupOnly': 'True',
        'xsi_type': 'ObjectSearchCriteria'
    }
    SanityCheck.NewSanityCheck(self.__class__.TYPES_MAP, object_search_criteria,
                               'PageableSearchCriteriaBase')

  def testAllowedComplexTypeValuesSucceed(self):
    """Test that Sanity Check does not fail on allowed complex type values."""
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
    SanityCheck.NewSanityCheck(self.__class__.TYPES_MAP, predicate_page,
                               'PredicatePage')


def makeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(SanityCheckTest))
  return suite


if __name__ == '__main__':
  suite = makeTestSuite()
  alltests = unittest.TestSuite([suite])
  unittest.main(defaultTest='alltests')
