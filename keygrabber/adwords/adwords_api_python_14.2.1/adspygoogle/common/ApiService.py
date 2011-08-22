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

"""Methods to access ApiService."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

from adspygoogle.common import SOAPPY
from adspygoogle.common import ZSI
from adspygoogle.common.Errors import ValidationError


class ApiService(object):

  """Wrapper for ApiService."""

  def __init__(self, headers, config, op_config, url, import_chain, lock,
               logger):
    """Inits ApiService.

    Args:
      headers: dict Dictionary object with populated authentication
               credentials.
      config: dict Dictionary object with populated configuration values.
      op_config: dict Dictionary object with additional configuration values for
                 this operation.
      url: str URL for the web service.
      import_chain: str Import chain of the wrapper for web service.
      lock: thread.lock Thread lock
      logger: Logger Instance of Logger

    Raises:
      ValidationError: The API version in op_config is not supported by the
                       ZSI-generated code for this product.
    """
    ToolkitSanityCheck = None
    API_VERSIONS = []
    self._config = config
    self._op_config = op_config
    if config['soap_lib'] == SOAPPY:
      from adspygoogle.common.soappy import MessageHandler
      self._message_handler = MessageHandler
      self._web_services = None
      # Attempt to import SOAPpy SanityCheck. Required for backwards
      # compatibility. Eventually, no library should have toolkit specific
      # sanity checks.
      try:
        exec ('from %s.soappy import SanityCheck as ToolkitSanityCheck'
              % import_chain)
      except ImportError, e:
        pass
    elif config['soap_lib'] == ZSI:
      from adspygoogle.common.zsi import Transformation
      self._transformation = Transformation
      # Attempt to import ZSI SanityCheck. Required for backwards
      # compatibility. Eventually, no library should have toolkit specific
      # sanity checks.
      try:
        exec ('from %s.zsi import SanityCheck as ToolkitSanityCheck'
              % import_chain)
      except ImportError, e:
        pass
      exec 'from %s import API_VERSIONS' % import_chain
      if op_config['version'] in API_VERSIONS:
        module = '%s_services' % self.__class__.__name__
        try:
          version = op_config['version']
          if version.find('.') > -1: version = version.replace('.', '_')
          web_services = __import__('%s.zsi.%s.%s'
                                    % (import_chain, version, module),
                                    globals(), locals(), [''])
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
      self._web_services = web_services
      self._loc = eval('web_services.%sLocator()' % self.__class__.__name__)
    self._sanity_check = ToolkitSanityCheck
