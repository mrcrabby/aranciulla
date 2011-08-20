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

"""This example gets all geo location information for a given list of
addresses.

Tags: GeoLocationService.get
"""

__author__ = 'api.kwinter@gmail.com (Kevin Winter)'

import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle.adwords.AdWordsClient import AdWordsClient


# Initialize client object.
client = AdWordsClient(path=os.path.join('..', '..', '..', '..'))

# Initialize appropriate service.
geo_location_service = client.GetGeoLocationService(
    'https://adwords-sandbox.google.com', 'v201101')

# Construct selector and get all geo location info.
selector = {
    'addresses': [
        {
            'streetAddress': '1600 Amphitheatre Parkway',
            'cityName': 'Mountain View',
            'provinceCode': 'US-CA',
            'provinceName': 'California',
            'postalCode': '94043',
            'countryCode': 'US'
        },
        {
            'streetAddress': '76 Ninth Avenue',
            'cityName': 'New York',
            'provinceCode': 'US-NY',
            'provinceName': 'New York',
            'postalCode': '10011',
            'countryCode': 'US'
        },
        {
            'streetAddress': '五四大街1号, Beijing东城区',
            'countryCode': 'CN'
        }
    ]
}
geo_locations = geo_location_service.Get(selector)

# Display results.
if geo_locations:
  for geo_location in geo_locations:
    if geo_location['GeoLocation_Type'] != 'InvalidGeoLocation':
      print ('Address \'%s\' has latitude \'%s\' and longitude \'%s\'.'
             % (geo_location['address']['streetAddress'],
                geo_location['geoPoint']['latitudeInMicroDegrees'],
                geo_location['geoPoint']['longitudeInMicroDegrees']))
    else:
      print 'Invalid geo location was found.'
else:
  print 'No geo locations were found.'

print
print ('Usage: %s units, %s operations' % (client.GetUnits(),
                                           client.GetOperations()))
