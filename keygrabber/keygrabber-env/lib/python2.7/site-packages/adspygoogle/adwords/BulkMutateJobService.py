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

"""Methods to access BulkMutateJobService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import time

from adspygoogle.adwords import AdWordsUtils
from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsErrors import AdWordsError
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService


class BulkMutateJobService(ApiService):

  """Wrapper for BulkMutateJobService.

  The BulkMutateJobService service provides operations for submitting jobs to be
  executed asynchronously and get information about submitted jobs and their
  parts.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits BulkMutateJobService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger
    """
    # NOTE(api.sgrinberg): Custom handling for BulkMutateJobService, whose
    # group in URL is 'job/' which is different from its namespace 'cm/'.
    url = [op_config['server'], 'api/adwords', 'job',
           op_config['version'], self.__class__.__name__]
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(BulkMutateJobService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def DownloadBulkJob(self, job_id, wait_secs=30, max_polls=60):
    """Return results of the bulk mutate job or None if there was a failure.

    Args:
      job_id: str Bulk mutate job id.
      wait_secs: int Time in seconds to wait between each poll.
      max_polls: int Maximum number of polls to perform.

    Returns:
      list Results of the bulk mutate job or None if there was a failure.
    """
    SanityCheck.ValidateTypes(((job_id, (str, unicode)), (wait_secs, int),
                               (max_polls, int)))

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
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Bulk mutate job status: %s' % status
      time.sleep(wait_secs)
      status = self.Get(selector)[0]['status']
      num_polls += 1

    if status != 'COMPLETED' and status != 'FAILED' and num_polls >= max_polls:
      msg = ('The job with id \'%s\' has exceeded max_polls of \'%s\'.'
             % (job_id, max_polls))
      raise AdWordsError(msg)

    if status == 'FAILED':
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Bulk mutate job failed'
        return None

    if Utils.BoolTypeConvert(self._config['debug']):
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
      selector: dict Filter to run campaign criteria through.

    Returns:
      tuple List of bulk mutate jobs meeting all the criteria of the selector.
    """
    method_name = 'getBulkMutateJob'
    SanityCheck.NewSanityCheck(
        self._wsdl_types_map, selector, 'BulkMutateJobSelector')

    if self._config['soap_lib'] == SOAPPY:
      selector = self._message_handler.PackVarAsXml(
          selector, 'selector', self._wsdl_types_map, False,
          'BulkMutateJobSelector')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (selector))
    elif self._config['soap_lib'] == ZSI:
      selector = self._transformation.MakeZsiCompatible(
          selector, 'BulkMutateJobSelector', self._wsdl_types_map,
          self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'selector': selector},)),
                                       'BulkMutateJob', self._loc, request)

  def Mutate(self, op):
    """Add or update bulk mutate job.

    Args:
      op: dict Operation.

    Returns:
      tuple Mutated bulk mutate job.
    """
    method_name = 'mutateBulkMutateJob'
    AdWordsUtils.TransformJobOperationXsi(op)
    SanityCheck.NewSanityCheck(self._wsdl_types_map, op, 'JobOperation')

    if self._config['soap_lib'] == SOAPPY:
      op = self._message_handler.PackVarAsXml(
          op, 'operation', self._wsdl_types_map, False, 'JobOperation')
      return self.__service.CallMethod(
          method_name.split(self.__class__.__name__.split('Service')[0])[0],
          (op))
    elif self._config['soap_lib'] == ZSI:
      op = self._transformation.MakeZsiCompatible(
          op, 'JobOperation', self._wsdl_types_map, self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'operation': op},)),
                                       'BulkMutateJob', self._loc, request)
