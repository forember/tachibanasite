'''
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

import argparse
import os
import os.path
from os.path import dirname
from os.path import join as pjoin
import urllib

# Constants/Options

DIRNAME0 = dirname(os.path.realpath(__file__))
INSTALL_PATH = dirname(dirname(DIRNAME0))
SITE_PATH = dirname(INSTALL_PATH)

AUTOTS_NOTICE = '!!AUTOTS!! Created by autots. Do not manually edit.'

FORCE_TEMPLATES = True

# Asking

def ask_yes_no(message, arg=None, default=None, interactive=True):
    if arg is not None:
        return arg
    if not interactive:
        return default
    message += ' ['
    message += 'Y' if default else 'y'
    message += '/'
    message += 'n' if default or default is None else 'N'
    message += ']'
    answer = None
    while answer is None:
        response = raw_input(message)
        if not response:
            answer = default
        elif response[0].lower() == 'y':
            answer = True
        elif response[0].lower() == 'n':
            answer = False
    return answer

def ask_string(message, arg=None, default=None, interactive=True):
    if arg is not None:
        return arg
    if not interactive:
        return default
    message += ' [{}]'.format(default)
    answer = None
    while answer is None:
        response = raw_input(message)
        if not response:
            answer = default
        else:
            answer = response
    return answer

def ask_choice(prelist, message, options, default=None, interactive=True):
    def interpret_answer(answer):
        if answer in options:
            return answer
        try:
            return options[int(answer)]
        except ValueError, IndexError:
            return None
    if not interactive:
        option = interpret_answer(default)
        if option is None:
            return default
        return option
    print prelist
    for i, option in enumerate(options):
        print '{: 2d}. {}'.format(i, option)
    option = None
    while option is None:
        try:
            option = interpret_answer(ask_string(message, None, default,
                interactive))
        except ValueError:
            pass
    return option

class Asker (object):
    def __init__(self, interactive=True):
        self.interactive = interactive

    def yes_no(self, message, arg=None, default=None):
        return ask_yes_no(message, arg, default, self.interactive)

    def string(self, message, arg=None, default=None):
        return ask_string(message, arg, default, self.interactive)

    def choice(self, prelist, message, options, default=None):
        return ask_choice(prelist, message, options, default, self.interactive)

def default_arg(source_arg, default=None):
    if source_arg is None:
        return default
    else:
        return source_arg

# Quoting

def ini_quote_html(s):
    from xml.sax.saxutils import escape
    return (escape(s).replace('"', '&quot;').replace("'", '&apos;')
            .replace('\\', '&#92;').replace('$', '&#36;'))

def ini_unquote_html(s):
    from xml.sax.saxutils import unescape
    return unescape(s)

def ini_quote_path(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')

def ini_unquote_path(s):
    r = ''
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 != len(s):
            d = s[i + 1]
            if d in '\\"$':
                r += d
                i += 2
                continue
        r += c
        i += 1
    return r

def ini_quote_url(s):
    return urllib.quote(s)

def ini_unquote_url(s):
    return urllib.unquote(s)

# General for Commands

def checkauto(filename):
    if not os.path.exists(filename):
        return True
    if not os.path.isfile(filename):
        return False
    with open(filename) as f:
        try:
            line = next(f)
            return '!!AUTOTS!!' in line
        except StopIteration:
            return True

def read_existing(file_path, ask, force):
    # Check If Manual Mode
    if not checkauto(file_path):
        print '{} has already been manually created.'.format(file_path)
        if not ask.yes_no('Overwrite it?', force, False):
            print 'Aborting.'
            return None
    # Read Existing Config
    source_lines = []
    if os.path.isfile(file_path):
        with open(file_path) as f:
            source_lines = [line.strip() for line in f]
    return source_lines

def show_confirm_write(file_path, lines, ask):
    # Output Content to Be Written
    print 'The following will be output to {}:'.format(file_path)
    print
    for line in lines:
        print '    {}'.format(line)
    print
    # Ask to Write
    if not ask.yes_no('Continue (cannot be undone)?', None,
            None if ask.interactive else True):
        print 'Aborting.'
        return 1
    # Write Output
    page_path = os.path.dirname(file_path)
    if not os.path.isdir(page_path):
        os.makedirs(page_path, 0775)
    with open(file_path, 'w') as f:
        f.writelines([line + '\n' for line in lines])
    print 'Written.'
    return 0

def match_line(source_lines, pattern, group=0, filt=lambda s: s):
    import re
    for source_line in source_lines:
        m = re.match(pattern.replace(' ', '\\s*') + '$', source_line)
        if m:
            try:
                return [filt(g) for g in m.group(*group)]
            except TypeError:
                return filt(m.group(group))
    try:
        return [None] * len(group)
    except TypeError:
        return None
