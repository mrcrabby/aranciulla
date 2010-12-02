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

"""Script to fetch codes used throughout the AdWords API web services.

See http://code.google.com/apis/adwords/docs/developer/adwords_api_codes.html.
"""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import os
import re
import sys
sys.path.append('..')
import urllib

from aw_api import Utils


URL = 'http://code.google.com/apis/adwords/docs/developer'
LOC = os.path.join('..', 'aw_api', 'data')
DATA_MAP = [
  {'csv': 'categories',
   'url': '/'.join([URL, 'adwords_api_categories.html']),
   're': ('<li><b>/(.*?)</b></li>|<li><span class="categorypath">(.*?)</span>'
          '<b>(.*?)</b></li>'),
   'cols': ['category', 'path']
  },
  {'csv': 'countries',
   'url': '/'.join([URL, 'adwords_api_countries.html']),
   're': '<tr><td>(.*?)</td><td>(.*?)</td></tr>',
   'cols': ['country', 'code']
  },
  {'csv': 'currencies',
   'url': '/'.join([URL, 'adwords_api_currency.html']),
   're': '<tr><td>(.*?)</td><td>(.*?)</td></tr>',
   'cols': ['code', 'currency']
  },
  {'csv': 'error_codes',
   'url': '/'.join([URL, 'adwords_api_error_codes.html']),
   're': ('<tr id=".*?" class="ShowHide"><td id=".*?"><code><span class="">'
          '(.*?)</span></code></td><td><span class=""> (.*?)</span></td></tr>'),
   'cols': ['code', 'message']
  },
  {'csv': 'languages',
   'url': '/'.join([URL, 'adwords_api_languages.html']),
   're': '<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',
   'cols': ['name', 'target', 'display']
  },
  {'csv': 'ops_rates',
   'url': '/'.join([URL, 'adwords_api_ratesheet.html']),
   're': ('<(?:tbody|table .*?)><tr.*?><td .*?><h4 class="normalsize">(.*?)'
          '</h4></td></tr>(.*?)</(?:tbody|table)>'),
   'cols': ['version', 'service', 'method', 'rate', 'per_item']
  },
  {'csv': 'timezones',
   'url': '/'.join([URL, 'adwords_api_timezones.html']),
   're': '<tr><td>(.*?)</td></tr>',
   'cols': ['timezone']
  },
  {'csv': 'us_cities',
   'url': '/'.join([URL, 'adwords_api_us_cities.html']),
   're': '<h2 id=".*?">(.*?)</h2><table.*?>(.*?)</table>',
   'cols': ['state', 'code']
  },
  {'csv': 'us_metros',
   'url': '/'.join([URL, 'adwords_api_us_metros.html']),
   're': '<table class="codes" summary="">.*?<h2>(.*?)</h2>(.*?)</table>',
   'cols': ['state', 'metro', 'code']
  },
  {'csv': 'world_cities',
   'url': '/'.join([URL, 'adwords_api_cities.html']),
   're': ('<h2 id=".*?">((?:\w+|\w+\s\w+))</h2><table class="codes" summary="" '
          'style="width: 100%"><tr>(.*?)(?:</ul></td>|)</tr></table>'),
   'cols': ['country', 'code']
  },
  {'csv': 'world_regions',
   'url': '/'.join([URL, 'adwords_api_regions.html']),
   're': ('<h2 id=".*?">((?:\w+|\w+\s\w+))</h2><table class="codes" '
          'summary="codes">(.*?)</table>'),
   'cols': ['country', 'code', 'region']
  }
]


if os.path.exists(os.path.abspath(LOC)):
  for f_name in os.listdir(os.path.abspath(LOC)):
    f_path = os.path.abspath(os.path.join(LOC, f_name))
    if f_name.split('.')[-1] == 'csv':
      os.unlink(f_path)
else:
  os.mkdir(os.path.abspath(LOC))

print 'Fetching codes ...'
for item in DATA_MAP:
  data = ''.join(urllib.urlopen(item['url']).read().split('\n'))

  # Remove weird unicode characters.
  for weird_char in ['\xa0', '\xc2']:
    if data.find(weird_char) > -1:
      data = data.replace(weird_char, '')

  pattern = re.compile(item['re'])
  groups = pattern.findall(data)
  lines = []
  for group in groups:
    if item['csv'] in ('categories',):
      group = [x for x in group if x != '']
      if len(group) == 1:
        category = ''.join(group)
        continue
      else:
        path = ''.join(group)
      lines.append('%s,%s'
                   % (Utils.CsvEscape(str(Utils.HtmlUnescape(category))),
                      Utils.CsvEscape(str(Utils.HtmlUnescape(path)))))
    elif item['csv'] in ('countries', 'currencies'):
      lines.append('%s,%s'
                   % (Utils.CsvEscape(str(Utils.HtmlUnescape(group[0]))),
                      Utils.CsvEscape(str(Utils.HtmlUnescape(group[1])))))
    elif item['csv'] in ('error_codes',):
      pattern = re.compile('<.*?>')
      message = list(group)[1]
      message = pattern.sub('', message)
      lines.append('%s,%s'
                   % (Utils.CsvEscape(str(Utils.HtmlUnescape(group[0]))),
                      Utils.CsvEscape(str(Utils.HtmlUnescape(message)))))
    elif item['csv'] in ('languages',):
      # Convert '-' into ''.
      new_group = []
      for sub_item in list(group):
        if sub_item == '-':
          new_group.append('')
        else:
          new_group.append(sub_item)
      lines.append('%s,%s,%s'
                   % (Utils.CsvEscape(str(Utils.HtmlUnescape(new_group[0]))),
                      Utils.CsvEscape(str(Utils.HtmlUnescape(new_group[1]))),
                      Utils.CsvEscape(str(Utils.HtmlUnescape(new_group[2])))))
    elif item['csv'] in ('ops_rates',):
      # TODO(api.sgrinberg): Implement scraping for v2009 rates.
      pattern = re.compile('<tr.*?><td>(.*?)</td><td>(.*?)</td></tr>')
      sub_groups = pattern.findall(group[1])
      for sub_group in sub_groups:
        method = sub_group[0].replace(' *', '')
        if sub_group[1].find(' per item') > -1:
          rate = sub_group[1].replace(' per item', '')
          per_item = 'true'
        else:
          rate = sub_group[1]
          per_item = 'false'
        lines.append('%s,%s,%s,%s,%s' % ('v13',
                                         Utils.CsvEscape(group[0]),
                                         Utils.CsvEscape(method),
                                         Utils.CsvEscape(rate),
                                         Utils.CsvEscape(per_item)))
    elif item['csv'] in ('timezones',):
      lines.append('%s' % str(Utils.HtmlUnescape(group)))
    elif item['csv'] in ('us_cities',):
      if group[0] != 'States':
        pattern = re.compile('<li>(.*?)</li>')
        sub_groups = pattern.findall(group[1])
        for sub_group in sub_groups:
          lines.append('%s,%s'
                       % (Utils.CsvEscape(str(Utils.HtmlUnescape(group[0]))),
                          Utils.CsvEscape(str(Utils.HtmlUnescape(sub_group)))))
    elif item['csv'] in ('us_metros',):
      pattern = re.compile('<tr><td>(.*?)</td><td>(.*?)</td></tr>')
      sub_groups = pattern.findall(group[1])
      for sub_group in sub_groups:
        lines.append('%s,%s,%s'
                     % (Utils.CsvEscape(str(Utils.HtmlUnescape(group[0]))),
                        Utils.CsvEscape(str(Utils.HtmlUnescape(sub_group[0]))),
                        Utils.CsvEscape(str(Utils.HtmlUnescape(sub_group[1])))))
    elif item['csv'] in ('world_cities',):
      pattern = re.compile('<li>(.*?)</li>')
      sub_groups = pattern.findall(group[1])
      for sub_group in sub_groups:
        lines.append('%s,%s'
                     % (Utils.CsvEscape(str(Utils.HtmlUnescape(group[0]))),
                        Utils.CsvEscape(str(Utils.HtmlUnescape(sub_group)))))
    elif item['csv'] in ('world_regions',):
      pattern = re.compile('<tr><td>(.*?)</td><td>(.*?)</td></tr>')
      sub_groups = pattern.findall(group[1])
      for sub_group in sub_groups:
        lines.append('%s,%s,%s'
                     % (Utils.CsvEscape(str(Utils.HtmlUnescape(group[0]))),
                        Utils.CsvEscape(str(Utils.HtmlUnescape(sub_group[0]))),
                        Utils.CsvEscape(str(Utils.HtmlUnescape(sub_group[1])))))

  # TODO(api.sgrinberg): Remove me, when automatic way of getting this data is
  # implemented.
  if item['csv'] in ('ops_rates',):
    lines.extend(['v200909,AdExtensionOverrideService,get,1,true',
                  'v200909,AdExtensionOverrideService,mutate.ADD,1,true',
                  'v200909,AdExtensionOverrideService,mutate.REMOVE,1,true',
                  'v200909,AdExtensionOverrideService,mutate.SET,1,true',
                  'v200909,AdGroupAdExtensionService,get,1,true',
                  'v200909,AdGroupAdExtensionService,mutate.ADD,1,true',
                  'v200909,AdGroupAdExtensionService,mutate.REMOVE,1,true',
                  'v200909,AdGroupAdService,get,1,true',
                  'v200909,AdGroupAdService,mutate.ADD,40,true',
                  'v200909,AdGroupAdService,mutate.REMOVE,1,true',
                  'v200909,AdGroupAdService,mutate.SET,1,true',
                  'v200909,AdGroupCriterionService,get,1,true',
                  'v200909,AdGroupCriterionService,mutate.ADD,15,true',
                  'v200909,AdGroupCriterionService,mutate.REMOVE,1,true',
                  'v200909,AdGroupCriterionService,mutate.SET,3,true',
                  'v200909,AdGroupService,get,1,true',
                  'v200909,AdGroupService,mutate.ADD,1,true',
                  'v200909,AdGroupService,mutate.SET,5,true',
                  'v200909,AdParamService,get,0.1,true',
                  'v200909,AdParamService,mutate.SET,0.1,true',
                  'v200909,AdParamService,mutate.REMOVE,0.1,true',
                  'v200909,BulkMutateJobService,get,1,true',
                  'v200909,BulkMutateJobService,mutate.ADD,1,true',
                  'v200909,BulkMutateJobService,mutate.SET,1,true',
                  'v200909,CampaignAdExtensionService,get,1,true',
                  'v200909,CampaignAdExtensionService,mutate.ADD,1,true',
                  'v200909,CampaignAdExtensionService,mutate.REMOVE,1,true',
                  'v200909,CampaignCriterionService,get,1,true',
                  'v200909,CampaignCriterionService,mutate.ADD,1,true',
                  'v200909,CampaignCriterionService,mutate.REMOVE,1,true',
                  'v200909,CampaignCriterionService,mutate.SET,1,true',
                  'v200909,CampaignService,get,1,true',
                  'v200909,CampaignService,mutate.ADD,1,true',
                  'v200909,CampaignService,mutate.SET,1,true',
                  'v200909,CampaignTargetService,get,1,true',
                  'v200909,CampaignTargetService,mutate.SET,1,true',
                  'v200909,GeoLocationService,get,1,true',
                  'v200909,InfoService,get,1,true',
                  'v200909,TargetingIdeaService,get,1,true',
                  'v200909,TargetingIdeaService,getBulkKeywordIdeas,1,true'])

  print '  [+] %s.csv' % item['csv']
  fh = open('%s.csv' % os.path.abspath(os.path.join(LOC, item['csv'])), 'w')
  try:
    lines.insert(0, ','.join(item['cols']))
    for line in lines:
      fh.write('%s\n' % line)
  finally:
    fh.close()

print '... done.'
