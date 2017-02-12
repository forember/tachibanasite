'''
    File:   utils/configIniUtils.py
    Author: Chris McKinney
    Edited: Aug 10 2016
    Editor: Chris McKinney

    Description:

    Utilities for working with the config.ini files.

    Edit History:

    0.8.10  - Added function for install URL.

    License:

    Copyright 2016 Chris McKinney

    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License.  You may obtain a copy
    of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''

import os
from os.path import dirname, realpath
INSTALL_PATH = dirname(dirname(realpath(__file__)))
CONFIG_PATHS = [os.path.join(INSTALL_PATH, 'common/config.ini'),
        realpath(os.path.join(INSTALL_PATH, '../common/config.ini')),
        'config.ini']

def get_config():
    '''Get configuration object.'''
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_PATHS)
    return config

def get_local_host_path():
    '''Parse local host path.'''
    config = get_config()
    lhp = config.get('TachibanaSite', 'local_host_path')
    if lhp.startswith('"') and lhp.endswith('"'):
        lhp = lhp[1:-1]
    return lhp

def get_install_url():
    '''Parse install url.'''
    config = get_config()
    url = config.get('TachibanaSite', 'install_url')
    if url.startswith('"') and url.endswith('"'):
        url = url[1:-1]
    return url

