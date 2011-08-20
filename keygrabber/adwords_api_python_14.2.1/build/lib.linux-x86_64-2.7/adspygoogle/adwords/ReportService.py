#!/usr/bin/python
# -*- coding: UTF-8 -*-
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

"""Methods to access ReportService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import cStringIO
import csv
import gzip
import StringIO
import time
import urllib
# Is this running on Google's App Engine?
try:
  import google.appengine
  from _xmlplus.dom import minidom
except:
  from xml.dom import minidom

from adspygoogle.adwords import WSDL_MAP
from adspygoogle.adwords.AdWordsWebService import AdWordsWebService
from adspygoogle.common import SanityCheck
from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common import Utils
from adspygoogle.common.ApiService import ApiService
from adspygoogle.common.Errors import Error


class ReportService(ApiService):

  """Wrapper for ReportService.

  The Report Service allows you to request a report about the performance of
  your AdWords campaigns.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits ReportService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock Thread lock.
      logger: Logger Instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['version'],
           self.__class__.__name__]
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__name_space = 'https://adwords.google.com/api/adwords'
    self.__service = AdWordsWebService(headers, config, op_config,
                                       '/'.join(url), lock, logger)
    self._wsdl_types_map = WSDL_MAP[op_config['version']][
        self.__service._GetServiceName()]
    super(ReportService, self).__init__(
        headers, config, op_config, url, 'adspygoogle.adwords', lock, logger)

  def DeleteReport(self, report_job_id):
    """Delete a report job along with the report it produced, if any.

    Args:
      report_job_id: str ID of the report job.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'deleteReport'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck
      report_job_id = SoappySanityCheck.UnType(report_job_id)
      self.__service.CallMethod(method_name, (report_job_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      self.__service.CallMethod(method_name,
                                (({'reportJobId': report_job_id},)),
                                'Report', self._loc, request)

  def GetAllJobs(self):
    """Return an array consisting of all jobs the user has scheduled.

    Returns:
      tuple Response from the API method.
    """
    method_name = 'getAllJobs'
    if self._config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Report', self._loc,
                                       request)

  def GetGzipReportDownloadUrl(self, report_job_id):
    """Return a URL for a compressed report.

    URL from which a compressed report with the given job ID can be downloaded
    (in Gzip format).

    Args:
      report_job_id: str ID of the report job.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'getGzipReportDownloadUrl'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck
      report_job_id = SoappySanityCheck.UnType(report_job_id)
      return self.__service.CallMethod(method_name, (report_job_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},)),
                                       'Report', self._loc, request)

  def GetReportDownloadUrl(self, report_job_id):
    """Return a URL for a report.

    URL from which the report with the given job ID can be downloaded.

    Args:
      report_job_id: str ID of the report job.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'getReportDownloadUrl'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck
      report_job_id = SoappySanityCheck.UnType(report_job_id)
      return self.__service.CallMethod(method_name, (report_job_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},)),
                                       'Report', self._loc, request)

  def GetReportJobStatus(self, report_job_id):
    """Return the status of the report job with the given report job ID.

    Args:
      report_job_id: str ID of the report job.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'getReportJobStatus'
    if self._config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import SanityCheck as SoappySanityCheck
      report_job_id = SoappySanityCheck.UnType(report_job_id)
      return self.__service.CallMethod(method_name, (report_job_id))
    elif self._config['soap_lib'] == ZSI:
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},)),
                                       'Report', self._loc, request)

  def ScheduleDefinedReportJob(self, job):
    """Schedule a defined report job for execution.

    Args:
      job: dict Report job object that defines the options for the report.

    Returns:
      tuple Response from the API method.
    """
    SanityCheck.ValidateTypes(((job, dict),))

    method_name = 'scheduleReportJob'
    if self._config['soap_lib'] == SOAPPY:
      name_space = '/'.join([self.__name_space, self._op_config['version'],
                             self._config['access']]).strip('/')
      job = self._sanity_check.ValidateDefinedReportJobV13(job, name_space)
      return self.__service.CallMethod(method_name, (job))
    elif self._config['soap_lib'] == ZSI:
      job = self._sanity_check.ValidateDefinedReportJobV13(job,
                                                           self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'job': job},)),
                                       'Report', self._loc, request)

  def ValidateReportJob(self, job):
    """This method takes a ReportJob and runs the validation logic against it.

    Args:
      job: dict Report job object that defines the options for the report.
    """
    SanityCheck.ValidateTypes(((job, dict),))

    method_name = 'validateReportJob'
    if self._config['soap_lib'] == SOAPPY:
      name_space = '/'.join([self.__name_space, self._op_config['version'],
                             self._config['access']]).strip('/')
      job = self._sanity_check.ValidateDefinedReportJobV13(job, name_space)
      self.__service.CallMethod(method_name, (job))
    elif self._config['soap_lib'] == ZSI:
      job = self._sanity_check.ValidateDefinedReportJobV13(job,
                                                           self._web_services)
      request = eval('self._web_services.%sRequest()' % method_name)
      self.__service.CallMethod(method_name, (({'job': job},)), 'Report',
                                self._loc, request)

  def DownloadXmlReport(self, report_job_id):
    """Download and return report data in XML format.

    Args:
      report_job_id: str ID of the report job.

    Returns:
      str Report data or None if report failed.
    """
    SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

    # Wait for report to finish.
    status = self.GetReportJobStatus(report_job_id)[0]
    while status != 'Completed' and status != 'Failed':
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Report job status: %s' % status
      time.sleep(30)
      status = self.GetReportJobStatus(report_job_id)[0]

    if status == 'Failed':
      if Utils.BoolTypeConvert(self._config['debug']):
        print 'Report process failed'
      return None

    if Utils.BoolTypeConvert(self._config['debug']):
      print 'Report has completed successfully'

    # Download report.
    report_url = self.GetGzipReportDownloadUrl(report_job_id)[0]

    # Convert report into readable XML format.
    report_xml = urllib.urlopen(report_url).read()
    return gzip.GzipFile(fileobj=StringIO.StringIO(report_xml)).read()

  def DownloadCsvReport(self, report_job_id=-1, report_xml=''):
    """Download and return report data in CSV format.

    Report consists of two parts: table and totals. Table contains column
    names and rows of data. The outgoing CSV will contain only columns and
    data rows. The totals are not included, but can be easily calculated from
    the CSV data.

    Args:
      [optional]
      report_job_id: str ID of the report job.
      report_xml: str Report in XML format. Used for testing and debugging.

    Returns:
      str Report data if all data is in ASCII.
      unicode Report data if report contains non-ASCII characters.
      None If report failed.
    """
    # Get XML report data.
    if not report_xml and report_job_id > -1:
      report_xml = self.DownloadXmlReport(report_job_id)
    if report_xml is None:
      return None

    # Prepare XML for DOM construction.
    report_xml = report_xml.replace('<?xml version="1.0" standalone="yes"?>',
                                    '')
    csv_rows = []
    try:
      # Construct DOM object.
      dom = minidom.parseString(report_xml)

      # Get data columns.
      columns = []
      column_dom = dom.getElementsByTagName('column')
      for column_item in column_dom:
        if column_item.hasAttributes():
          columns.append(column_item.attributes.item(0).value)

      # Get data rows.
      rows = []
      row_dom = dom.getElementsByTagName('row')
      for row_item in row_dom:
        if row_item.hasAttributes():
          attrs = row_item.attributes
          row = {}
          for index in range(attrs.length):
            row[attrs.item(index).name] = attrs.item(index).value
          rows.append(row)

      # Combine columns and rows into CSV format.
      csv_rows = [[column for column in columns]]
      for row in rows: csv_rows.append([row[column] for column in columns])
    except:
      msg = ('Unable to parse report\'s data. Please, file a bug at '
             'http://code.google.com/p/google-api-adwords-python-lib/'
             'issues/list.')
      raise Error(msg)

    buffer = cStringIO.StringIO()
    # A workaround for reports that include non-ASCII characters (i.e. ø).
    try:
      csv.writer(buffer).writerows(csv_rows)
    except (UnicodeEncodeError, Exception):
      unicode_csv_rows = []
      for row in csv_rows:
        unicode_csv_rows.append(
            ','.join([Utils.CsvEscape(item) for item in row]))
      return unicode('\n'.join(unicode_csv_rows))
    return buffer.getvalue().rstrip()
