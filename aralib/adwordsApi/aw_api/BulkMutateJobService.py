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

"""Methods to access BulkMutateJobService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import time

from aw_api import SanityCheck as glob_sanity_check
from aw_api import SOAPPY
from aw_api import ZSI
from aw_api import Utils
from aw_api.Errors import ApiVersionNotSupportedError
from aw_api.Errors import Error
from aw_api.Errors import ValidationError
from aw_api.WebService import WebService


class BulkMutateJobService(object):

  """Wrapper for BulkMutateJobService.

  The BulkMutateJob Service provides operations for submitting jobs to be
  executed asynchronously and get information about submitted jobs and their
  parts.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits BulkMutateJobService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock the thread lock.
      logger: Logger the instance of Logger
    """
    # NOTE(api.sgrinberg): Custom handling for BulkMutateJobService, whose
    # group in URL is 'job/' which is different from its namespace 'cm/'.
    url = [op_config['server'], 'api/adwords', 'job',
           op_config['version'], self.__class__.__name__]
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = WebService(headers, config, op_config, '/'.join(url), lock,
                                logger)
    self.__config = config
    self.__op_config = op_config
    if self.__config['soap_lib'] == SOAPPY:
      from aw_api.soappy_toolkit import SanityCheck
      self.__web_services = None
    elif self.__config['soap_lib'] == ZSI:
      from aw_api import API_VERSIONS
      from aw_api.zsi_toolkit import SanityCheck
      if op_config['version'] in API_VERSIONS:
        module = '%s_services' % self.__class__.__name__
        try:
          web_services = __import__('aw_api.zsi_toolkit.%s.%s'
                                    % (op_config['version'], module), globals(),
                                    locals(), [''])
        except ImportError, e:
          # If one of library's required modules is missing, re raise exception.
          if str(e).find(module) < 0:
            raise ImportError(e)
          msg = ('The version \'%s\' is not compatible with \'%s\'.'
                 % (op_config['version'], self.__class__.__name__))
          raise ValidationError(msg)
      else:
        msg = 'Invalid API version, not one of %s.' % str(list(API_VERSIONS))
        raise ValidationError(msg)
      self.__web_services = web_services
      self.__loc = eval('web_services.%sLocator()' % self.__class__.__name__)
    self.__sanity_check = SanityCheck

  def DownloadBulkJob(self, job_id, wait_secs=30, max_polls=60):
    """Return results of the bulk mutate job or None if there was a failure.

    Args:
      job_id: str a bulk mutate job id.
      wait_secs: int the time in seconds to wait between each poll.
      max_polls: int the maximum number of polls to perform.

    Returns:
      list results of the bulk mutate job or None if there was a failure.
    """
    glob_sanity_check.ValidateTypes(((job_id, (str, unicode)),
                                     (wait_secs, int), (max_polls, int)))

    # Wait for bulk muate job to complete.
    selector = {
        'jobIds': [job_id]
    }
    job = self.Get(selector)[0]
    status = job['status']
    num_parts = job['numRequestParts']
    num_parts_recieved = job['numRequestPartsReceived']

    # Were all parts of the job uploaded?
    if num_parts != num_parts_recieved:
      return None

    num_polls = 1
    while (status != 'COMPLETED' and status != 'FAILED' and
           num_polls < max_polls):
      if Utils.BoolTypeConvert(self.__config['debug']):
        print 'Bulk mutate job status: %s' % status
      time.sleep(wait_secs)
      status = self.Get(selector)[0]['status']
      num_polls += 1

    if status != 'COMPLETED' and status != 'FAILED' and num_polls >= max_polls:
      msg = ('The job with id \'%s\' has exceeded max_polls of \'%s\'.'
             % (job_id, max_polls))
      raise Error(msg)

    if status == 'FAILED':
      if Utils.BoolTypeConvert(self.__config['debug']):
        print 'Bulk mutate job failed'
        return None

    if Utils.BoolTypeConvert(self.__config['debug']):
      print 'Bulk mutate job completed successfully'

    # Get results for each part of the job.
    res = []
    for part in xrange(int(num_parts)):
      selector = {
          'jobIds': [job_id],
          'resultPartIndex': str(part)
      }
      res.append(self.Get(selector)[0])
    return res

  def Get(self, selector):
    """Return a list of bulk mutate jobs.

    List of bulk mutate jobs specified by a job selector.

    Args:
      selector: dict filter to run campaign criteria through.

    Returns:
      tuple list of bulk mutate jobs meeting all the criteria of the selector.
    """
    method_name = 'getBulkMutateJob'
    if self.__config['soap_lib'] == SOAPPY:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with SOAPpy toolkit.' % (Utils.GetCurrentFuncName(),
                                           self.__op_config['version']))
      raise ApiVersionNotSupportedError(msg)
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      self.__sanity_check.ValidateSelector(selector, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'BulkMutateJob', self.__loc, request)

  def Mutate(self, op):
    """Add or update bulk mutate job.

    Args:
      op: dict operation.

    Returns:
      tuple mutated bulk mutate job.
    """
    method_name = 'mutateBulkMutateJob'
    if self.__config['soap_lib'] == SOAPPY:
      msg = ('The \'%s\' request via %s is currently not supported for '
             'use with SOAPpy toolkit.' % (Utils.GetCurrentFuncName(),
                                           self.__op_config['version']))
      raise ApiVersionNotSupportedError(msg)
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      op = self.__sanity_check.ValidateOperation(op, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'operation': op},)),
                                       'BulkMutateJob', self.__loc, request)
