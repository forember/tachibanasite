'''
    File:   ./modules/autots/install.py
    Author: Chris McKinney
    Edited: Nov 17 2017
    Editor: Chris McKinney

    Description:

    Script for managing a TachibanaSite install.

    Edit History:

    1.9.0   - Created module.

    License:

    Copyright 2017 Chris McKinney

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
import os.path
from os.path import join as pjoin
import subprocess

from .arg_parser import ARG_PARSER, get_base_arg_list
from .config import config
from .edit import create
from .overrides import copyright, header
from .utils import INSTALL_PATH, SITE_PATH

def check_python_deps():
    failures = []
    try:
        import bottle
    except ImportError:
        failures.append('bottle')
    try:
        from PIL import Image
    except ImportError:
        failures.append('Pillow')
    try:
        import requests
    except ImportError:
        failures.append('requests')
    return failures

def install_python_deps():
    print 'install: Installing dependencies.'
    try:
        from setuptools.command import easy_install
        have_easy_install = True
    except ImportError:
        have_easy_install = False
    print 'install: easy_install: {}present'.format(
            '' if have_easy_install else 'not ')
    try:
        import pip
        have_pip = True
    except ImportError:
        try:
            import ensurepip
            ensurepip.bootstrap()
            import pip
            have_pip = True
        except ImportError:
            have_pip = False
    print 'install: pip: {}present'.format('' if have_pip else 'not ')
    had_pip = have_pip
    pip_via_ei = False
    for x in xrange(2):
        if have_easy_install and not have_pip and not pip_via_ei:
            print 'install: Installing pip via easy_install...'
            easy_install.main(['--user', '--upgrade', 'pip'])
            try:
                import pip
                have_pip = True
                pip_via_ei = True
                print 'install: Successful.'
            except ImportError:
                have_pip = False
                print 'install: Not successful.'
        if have_pip and (x == 0 or (pip_via_ei and not had_pip)):
            print 'install: Installing dependencies via pip...'
            if pip.main(['install', '--user', '--upgrade',
                'bottle', 'Pillow', 'requests']) != 0:
                have_pip = False
                print 'install: Not successful.'
            else:
                print 'install: Successful'
    if have_easy_install and (not have_pip or check_python_deps()):
        print 'install: Installing dependencies via easy_install...'
        easy_install.main(['--user', '--upgrade',
            'bottle', 'Pillow', 'requests'])
    failures = check_python_deps()
    if failures:
        print 'install: Some dependencies are still not installed.'
    else:
        print 'install: All dependencies installed.'
    if 'bottle' in failures:
        print 'install: Source-installing bottle.'
        import urllib2
        open(pjoin(pjoin(INSTALL_PATH, 'utils'), 'bottle.py'), 'w').write(
                urllib2.urlopen('https://bottlepy.org/bottle.py').read())
    if 'Pillow' in failures:
        print ('install: Warning: Could not install Pillow. Some modules'
                + ' will not work.')
    if 'requests' in failures:
        print ('install: Warning: Could not install requests. Some modules'
                + ' will not work.')

def install(args):
    if args.deps:
        install_python_deps()
    base_arg_list = get_base_arg_list(args)
    def do_subcommand(func, name):
        return func(ARG_PARSER.parse_args(base_arg_list + [name]))
    status = do_subcommand(config, 'config')
    if status:
        return status
    status = do_subcommand(copyright, 'copyright')
    if status:
        return status
    status = do_subcommand(header, 'header')
    if status:
        return status
    status = do_subcommand(create, 'create')
    if status:
        return status
    return 0

def upgrade(args):
    command = ['sh', os.path.realpath(pjoin(INSTALL_PATH, '_install_ts.sh'))]
    command.extend(get_base_arg_list(args))
    command.append('install')
    if not args.deps:
        command.append('--no-deps')
    if subprocess.call(['which', 'git']) == 0:
        git = 'git'
    else:
        git = os.path.expanduser('~/bin/git')
    status = subprocess.call([git, 'pull'], cwd=INSTALL_PATH)
    if status == 0:
        print 'Running install for new version.'
        return subprocess.call(command, cwd=SITE_PATH)
    else:
        return status

