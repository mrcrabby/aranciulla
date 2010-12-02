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

"""Methods to access ReportService service."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import gzip
import time
import urllib
# Is this running on Google's App Engine?
try:
  import google.appengine
  from _xmlplus.dom import minidom
except:
  from xml.dom import minidom
import StringIO

from aw_api import SanityCheck as glob_sanity_check
from aw_api import SOAPPY
from aw_api import ZSI
from aw_api import Utils
from aw_api.Errors import Error
from aw_api.Errors import ValidationError
from aw_api.WebService import WebService


class ReportService(object):

  """Wrapper for ReportService.

  The Report Service allows you to request a report about the performance of
  your AdWords campaigns.
  """

  def __init__(self, headers, config, op_config, lock, logger):
    """Inits ReportService.

    Args:
      headers: dict dictionary object with populated authentication
               credentials.
      config: dict dictionary object with populated configuration values.
      op_config: dict dictionary object with additional configuration values for
                 this operation.
      lock: thread.lock the thread lock.
      logger: Logger the instance of Logger
    """
    url = [op_config['server'], 'api/adwords', op_config['version'],
           self.__class__.__name__]
    if config['access']: url.insert(len(url) - 1, config['access'])
    self.__service = WebService(headers, config, op_config, '/'.join(url), lock,
                                logger)
    self.__config = config
    self.__op_config = op_config
    self.__name_space = 'https://adwords.google.com/api/adwords'
    if self.__config['soap_lib'] == SOAPPY:
      from aw_api.soappy_toolkit import SanityCheck
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

  def DeleteReport(self, report_job_id):
    """Delete a report job along with the report it produced, if any.

    Args:
      report_job_id: str ID of the report job.

        Ex:
          report_job_id = '1234567890'
    """
    glob_sanity_check.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'deleteReport'
    if self.__config['soap_lib'] == SOAPPY:
      report_job_id = self.__sanity_check.UnType(report_job_id)
      self.__service.CallMethod(method_name, (report_job_id))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      self.__service.CallMethod(method_name,
                                (({'reportJobId': report_job_id},)),
                                'Report', self.__loc, request)

  def GetAllJobs(self):
    """Return an array consisting of all jobs the user has scheduled.

    Returns:
      tuple response from the API method.
    """
    method_name = 'getAllJobs'
    if self.__config['soap_lib'] == SOAPPY:
      return self.__service.CallMethod(method_name, ())
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (), 'Report', self.__loc,
                                       request)

  def GetGzipReportDownloadUrl(self, report_job_id):
    """Return a URL for a compressed report.

    URL from which a compressed report with the given job ID can be downloaded
    (in Gzip format).

    Args:
      report_job_id: str ID of the report job.

        Ex:
          report_job_id = '1234567890'

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'getGzipReportDownloadUrl'
    if self.__config['soap_lib'] == SOAPPY:
      report_job_id = self.__sanity_check.UnType(report_job_id)
      return self.__service.CallMethod(method_name, (report_job_id))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},)),
                                       'Report', self.__loc, request)

  def GetReportDownloadUrl(self, report_job_id):
    """Return a URL for a report.

    URL from which the report with the given job ID can be downloaded.

    Args:
      report_job_id: str ID of the report job.

        Ex:
          report_job_id = '1234567890'

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'getReportDownloadUrl'
    if self.__config['soap_lib'] == SOAPPY:
      report_job_id = self.__sanity_check.UnType(report_job_id)
      return self.__service.CallMethod(method_name, (report_job_id))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},)),
                                       'Report', self.__loc, request)

  def GetReportJobStatus(self, report_job_id):
    """Return the status of the report job with the given report job ID.

    Args:
      report_job_id: str ID of the report job.

        Ex:
          report_job_id = '1234567890'

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((report_job_id, (str, unicode)),))

    method_name = 'getReportJobStatus'
    if self.__config['soap_lib'] == SOAPPY:
      report_job_id = self.__sanity_check.UnType(report_job_id)
      return self.__service.CallMethod(method_name, (report_job_id))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name,
                                       (({'reportJobId': report_job_id},)),
                                       'Report', self.__loc, request)

  def ScheduleDefinedReportJob(self, job):
    """Schedule a defined report job for execution.

    Args:
      job: dict report job object that defines the options for the report.

        Ex:
          job = {
            'adWordsType': 'SearchOnly',
            'aggregationTypes': ['Daily'],
            'campaigns': ['1234567890'],
            'campaignStatuses': ['Active', 'Paused'],
            'clientEmails': ['johndoe@example.com'],
            'crossClient': 'False',
            'endDay': '2007-11-30',
            'includeZeroImpression': 'False',
            'name': 'Test Report',
            'selectedColumns': ['Campaign', 'CampaignId', 'CPC', 'CTR'],
            'selectedReportType': 'Campaign',
            'startDay': '2007-11-01',
          }

    Returns:
      tuple response from the API method.
    """
    glob_sanity_check.ValidateTypes(((job, dict),))

    method_name = 'scheduleReportJob'
    if self.__config['soap_lib'] == SOAPPY:
      name_space = '/'.join([self.__name_space, self.__op_config['version'],
                             self.__config['access']]).strip('/')
      job = self.__sanity_check.ValidateDefinedReportJobV13(job, name_space)
      return self.__service.CallMethod(method_name, (job))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      job = self.__sanity_check.ValidateDefinedReportJobV13(job, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      return self.__service.CallMethod(method_name, (({'job': job},)),
                                       'Report', self.__loc, request)

  def ValidateReportJob(self, job):
    """This method takes a ReportJob and runs the validation logic against it.

    Args:
      job: dict report job object that defines the options for the report.

        Ex:
          job = {
            'adWordsType': 'SearchOnly',
            'aggregationTypes': ['Daily'],
            'campaigns': ['1234567890'],
            'campaignStatuses': ['Active', 'Paused'],
            'clientEmails': ['johndoe@example.com'],
            'crossClient': 'False',
            'endDay': '2007-11-30',
            'includeZeroImpression': 'False',
            'name': 'Test Report',
            'selectedColumns': ['Campaign', 'CampaignId', 'CPC', 'CTR'],
            'selectedReportType': 'Campaign',
            'startDay': '2007-11-01',
          }
    """
    glob_sanity_check.ValidateTypes(((job, dict),))

    method_name = 'validateReportJob'
    if self.__config['soap_lib'] == SOAPPY:
      name_space = '/'.join([self.__name_space, self.__op_config['version'],
                             self.__config['access']]).strip('/')
      job = self.__sanity_check.ValidateDefinedReportJobV13(job, name_space)
      self.__service.CallMethod(method_name, (job))
    elif self.__config['soap_lib'] == ZSI:
      web_services = self.__web_services
      job = self.__sanity_check.ValidateDefinedReportJobV13(job, web_services)
      request = eval('web_services.%sRequest()' % method_name)
      self.__service.CallMethod(method_name, (({'job': job},)), 'Report',
                                self.__loc, request)

  def DownloadXmlReport(self, report_job_id):
    """Download and return report data in XML format.

    Args:
      report_job_id: str ID of the report job.

        Ex:
          report_job_id = '1234567890'

    Returns:
      str report data or None if report failed.
    """
    glob_sanity_check.ValidateTypes(((report_job_id, (str, unicode)),))

    # Wait for report to finish.
    status = self.GetReportJobStatus(report_job_id)[0]
    while status != 'Completed' and status != 'Failed':
      if Utils.BoolTypeConvert(self.__config['debug']):
        print 'Report job status: %s' % status
      time.sleep(30)
      status = self.GetReportJobStatus(report_job_id)[0]

    if status == 'Failed':
      if Utils.BoolTypeConvert(self.__config['debug']):
        print 'Report process failed'
        return None

    if Utils.BoolTypeConvert(self.__config['debug']):
      print 'Report has completed successfully'

    # Download report.
    report_url = self.GetGzipReportDownloadUrl(report_job_id)[0]

    # Convert report into readable XML format.
    report_xml = urllib.urlopen(report_url).read()
    report_xml = gzip.GzipFile(fileobj=StringIO.StringIO(report_xml)).read()

    return report_xml

  def DownloadCsvReport(self, report_job_id, report_xml=''):
    """Download and return report data in CSV format.

    Args:
      report_job_id: str ID of the report job.
      report_xml: str Report in XML format. Used for testing and debugging.

        Ex:
          report_job_id = '1234567890'
          report_xml = '<report><table><columns>...</columns></table></report>'

    Returns:
      str report data if all data is in ASCII.
      unicode report data if report contains non-ASCII characters.
      None if report failed.
    """
    # Get XML report data.
    if not report_xml:
      report_xml = self.DownloadXmlReport(report_job_id)
    if report_xml is None:
      return None

    # Prepare XML for DOM construction.
    #
    # Report consists of two parts: table and totals. Table contains column
    # names and rows of data. The outgoing CSV will contain only columns and
    # data rows. The totals are not included, but can be easily calculated
    # from the CSV data.
    report_xml = report_xml.replace('<?xml version="1.0" standalone="yes"?>',
                                    '')

    items = []
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
      for column in columns:
        items.append('%s,' % column)
      items = [''.join(items).rstrip(','), '\n']
      for row in rows:
        sub_items = []
        for column in columns:
          sub_items.append('%s,' % row[column])
        items.append('%s\n' %  ''.join(sub_items).rstrip(','))
    except:
      msg = ('Unable to parse report\'s data. Please, file a bug at '
             'http://code.google.com/p/google-api-adwords-python-lib/'
             'issues/list.')
      raise Error(msg)

    # A workaround for reports that include non-ASCII characters (i.e. ø).
    try:
      report_csv = str(''.join(items))
    except (UnicodeEncodeError, Exception):
      report_csv = unicode(''.join(items))
    return report_csv
