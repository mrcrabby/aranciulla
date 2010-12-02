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
#

"""Handler functions for outgoing and incoming messages."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import inspect
import sys
import types

from aw_api import SanityCheck
from aw_api.Errors import MissingPackageError
from aw_api.Errors import ValidationError
from aw_api.zsi_toolkit import MAX_ZSI_VERSION
from aw_api.zsi_toolkit import MIN_ZSI_VERSION
from aw_api.zsi_toolkit.HttpConnectionHandler import HttpConnectionHandler
from aw_api.zsi_toolkit.SigHandler import SigHandler
try:
  import ZSI
  from ZSI.version import Version as ZSI_VERSION
except ImportError:
  msg = 'ZSI v%s or newer is required.' % MIN_ZSI_VERSION
  raise MissingPackageError(msg)
else:
  if list(ZSI.version.Version) < (list(map(eval, MIN_ZSI_VERSION.split('.')))):
    msg = 'ZSI v%s or newer is required.' % MIN_ZSI_VERSION
    raise MissingPackageError(msg)
  # NOTE(api.sgrinberg): Keep this check until ZSI version higher than 2.0.0
  # fixes known bug with bad NS (see issue# 84).
  elif list(ZSI.version.Version) > (list(map(eval,
                                             MAX_ZSI_VERSION.split('.')))):
    msg = ('ZSI v%s is not supported. Please use v%s.'
           % ('.'.join(map(str, ZSI.version.Version)), MIN_ZSI_VERSION))
    raise ValidationError(msg)


def GetServiceConnection(headers, config, url, http_proxy, service_name, loc):
  """Get SOAP service connection.

  Args:
    headers: dict dictionary object with populated authentication
             credentials.
    config: dict dictionary object with populated configuration values.
    url: str url of the web service to call.
    http_proxy: str HTTP proxy to use for this API call.
    service_name: str API service name.
    loc: service locator.

  Returns:
    instance of SoapBindingSOAP interface with set headers.
  """
  kw = {'tracefile': sys.stdout}
  if http_proxy:
    HttpConnectionHandler.http_proxy = http_proxy
    kw['transport'] = HttpConnectionHandler
  if 'ns_target' in config: service_name += 'Service'
  port_type = eval('loc.get%sInterface(url=url, **kw)' % service_name)
  port_type.binding.sig_handler = SigHandler(headers, config)

  # Set custom HTTP headers.
  user_agent = 'ZSI %s'  % '.'.join(map(str, ZSI_VERSION))
  port_type.binding.AddHeader('User-Agent', user_agent)

  return port_type


def SetRequestParams(op_config, request, params):
  """Set SOAP request parameters.

  Args:
    op_config: dict dictionary object with populated configuration values for
               this operation.
    request: instance holder of the SOAP request.
    params: list list of parameters to send to the API method.

  Returns:
    instance holder of the SOAP request with set parameters.
  """
  if (not isinstance(request, types.InstanceType) or
      not isinstance(params, tuple)):
    return request
  for param in params:
    request.__dict__.__setitem__(
        '_%s' % param.keys()[0],
        PackRequestAsComplexType(param.get(param.keys()[0]),
                                 op_config['version']))

  return request


def UnpackResponseAsTuple(response):
  """Unpack (recursively) SOAP data holder into a Python tuple object.

   Args:
     response: instance of SOAP data holder object.

  Returns:
    tuple unpacked SOAP data holder.
  """
  if (isinstance(response, (types.InstanceType, ZSI.TCcompound.ComplexType)) or
      inspect.isclass(response)):
    if not response.__dict__.keys():
      return (response.__dict__,)
    if (response.__dict__.keys()[0].find('Return') >= 0 or
        response.__dict__.keys()[0].find('fault') >= 0 or
        response.__dict__.keys()[0] == '_rval'):
      tpl = ()
      data = UnpackResponseAsTuple(response.__dict__.get(
          response.__dict__.keys()[0]))
      tpl = (data,)
      return tpl

    dct = {}
    for key in response.__dict__:
      # Prevent from hitting maximum recursion depth.
      if key == 'type':
        return dct
      value = response.__dict__.get(key)
      data = UnpackResponseAsTuple(value)
      dct[key.strip('_')] = data
    return dct
  elif isinstance(response, list):
    lst = []
    if len(response) < 1:
      return lst
    else:
      for item in response:
        data = UnpackResponseAsTuple(item)
        lst.append(data)
      return lst
  elif isinstance(response, tuple):
    # Tuple is returned for startDate and endDate in a format of
    # (2008, 6, 11, 0, 0, 0, 0, 0, 0), convert to a human readable string
    # (e.g., 2008-6-11). Or tuple can be returned as part of fault element.
    if len(response) != 9:
      lst = []
      for item in response:
        data = UnpackResponseAsTuple(item)
        lst.append(data)
      return lst

    items = []
    for item in response[:3]:
      items.append('%s-' % str(item))
    return ''.join(items).strip('-')
  else:
    # Workaround for string with non-ASCII characters.
    try:
      return str(response)
    except UnicodeEncodeError:
      return response


def PackRequestAsComplexType(request, version):
  """Pack (recursively) a Python tuple object into a SOAP data holder.

   Args:
     request: instance of Python tuple object.
     version: str the API version being used.

  Returns:
    ZSI.TCcompound.ComplexType packed Python data.
  """
  if isinstance(request, dict):
    cpl = ZSI.TCcompound.ComplexType(ZSI.TCcompound.ComplexType, [])
    for key in request:
      value = request.get(key)
      data = PackRequestAsComplexType(value, version)
      if data and data != 'None':
        cpl.__dict__.__setitem__('_%s' % key, data)
    return cpl
  elif isinstance(request, list):
    if not SanityCheck.IsNewApi(version):
      request = CustomPackList(request)
    if isinstance(request, dict):
      return PackRequestAsComplexType(request, version)
    lst = []
    for item in request:
      data = PackRequestAsComplexType(item, version)
      lst.append(data)
    return lst
  elif isinstance(request, tuple):
    return request
  else:
    return request


def CustomPackList(lst):
  """Custom pack a list into a format acceptable by ZSI client.

  Args:
    lst: list of Python objects.

  Returns:
    Custom packed list of Python objects.
  """
  if not lst:
    return {}
  new_lst = []
  keys = []
  key = ''
  for item in lst:
    if isinstance(item, dict):
      # If all dicts have same keys, repack. E.g.,
      #   input: [{'languages': 'en'}, {'langauges': 'iw'}]
      #   output: {'langauges': ['en', 'iw']}
      if len(set(item.keys())) > 1:
        return lst
      else:
        keys.append(item.keys()[0])
        for key in item:
          value = item.get(key)
          new_lst.append(value)
    else:
      return lst

  return {key: new_lst}
