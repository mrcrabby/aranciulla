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

"""Unit tests to cover WSDL parsing scripts."""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import pickle
import sys
sys.path.append(os.path.join('..', '..', '..'))
import unittest

from scripts.adspygoogle.common import wsdl_auto_obj


class WsdlAutoObjTest(unittest.TestCase):

  """Unittest suite for wsdl_auto_obj."""

  WSDL_NAME = 'mock_wsdl.xml'
  DATA_LOCATION = os.path.abspath(os.path.join('data'))
  TYPES_FILENAME = 'test_wsdl_type_defs.pkl'
  OPS_FILENAME = 'test_wsdl_ops_defs.pkl'
  API_VERSION = 'v1234'
  API_SERVICE_NAME = 'example'
  API_TARGETS = [{
      'version': API_VERSION,
      'services': [API_SERVICE_NAME]
  }]

  CANONICAL_TYPES_MAP = {
      API_VERSION: {
          API_SERVICE_NAME: {
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
                                 ['includeObjectsWithOutGroupOnly',
                                  'xsd:boolean'],
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
      }
  }
  CANONICAL_OPERATIONS_MAP = {
      API_VERSION: {
          API_SERVICE_NAME: {
              'getObjects': ['ObjectRecordSet'],
              'get': ['PredicatePage']
          }
      }
  }

  def setUp(self):
    """Prepare unittest."""
    print self.id()

  def testWsdlAutoObj(self):
    """Test whether the wsdl_auto_obj script properly parses the test WSDL."""

    def MockWsdlInfoToUrl (wsdl_info, service):
      """Mock WSDL to URL function, which always points to the mock WSDL."""
      return 'file:%s' % os.path.join(self.__class__.DATA_LOCATION,
                                      self.__class__.WSDL_NAME)
    try:
      wsdl_auto_obj.main(self.__class__.DATA_LOCATION,
                         self.__class__.TYPES_FILENAME,
                         self.__class__.OPS_FILENAME,
                         self.__class__.API_TARGETS, MockWsdlInfoToUrl)

      types_map = pickle.load(open(os.path.join(
          self.__class__.DATA_LOCATION, self.__class__.TYPES_FILENAME), 'r'))
      operations_map = pickle.load(open(os.path.join(
          self.__class__.DATA_LOCATION, self.__class__.OPS_FILENAME), 'r'))

      self.assertTrue(types_map == self.__class__.CANONICAL_TYPES_MAP)
      self.assertTrue(operations_map == self.__class__.CANONICAL_OPERATIONS_MAP)

    finally:
      for filename in (self.__class__.TYPES_FILENAME,
                       self.__class__.OPS_FILENAME):
        if os.path.exists(os.path.join(self.__class__.DATA_LOCATION,
                                       filename)):
          os.unlink(os.path.join(self.__class__.DATA_LOCATION, filename))


def makeTestSuite():
  """Set up test suite.

  Returns:
    TestSuite test suite.
  """
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(WsdlAutoObjTest))
  return suite


if __name__ == '__main__':
  suite = makeTestSuite()
  alltests = unittest.TestSuite([suite])
  unittest.main(defaultTest='alltests')
