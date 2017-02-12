'''
    File:   modules/people/__init__.py
    Author: Chris McKinney
    Edited: Aug 10 2016
    Editor: Chris McKinney

    Description:

    Provides person objects and utilities.

    Edit History:

    0.5.21  - Added email obfuscation.

    0.8.10  - Added TachibanaSite template library bindings.
            - Screwed with localhost stuff to make it work for now.

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
INSTALL_PATH = dirname(dirname(dirname(realpath(__file__))))
import configIniUtils
import re
import sys

# File extensions. Revisit these periodically to sort common extensions first.
ABOUTME_EXTENSIONS = ['.markdown', '', '.mdown', '.md', '.text', '.txt',
                      '.html']
PHOTO_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.ico']

# Available hosts.
HOST_TACHIBANA = 'tachibanatech.com'
HOST_AFRL = 'afrl.cse.sc.edu'
HOST_CSE = 'cse.sc.edu'

# Default request protocol. Should probably stay HTTP or HTTPS.
DEFAULT_PROTOCOL = 'http'
# Status codes
STATUS_OK = 200
STATUS_NOT_FOUND = 404

# Local file protocol. "file" is standard.
LOCAL_PROTOCOL = 'file'
# The host the site is installed on.
LOCAL_HOST = ''#HOST_TACHIBANA
# The path on the local host that is root for DEFAULT_PROTOCOL requests.
LOCAL_HOST_PATH = configIniUtils.get_local_host_path()

DEFAULT_CSS_CLASSES = 'person'
def _make_clear_default():
    '''Adds "clear" to the default CSS classes for person entries.'''
    globals()['DEFAULT_CSS_CLASSES'] = 'person clear'

# The relative path to the person template.
PERSON_TEMPLATE_FILE = os.path.join(INSTALL_PATH,
        'modules/people/person.markdown.template')

class LocalResponse(object):
    '''A protocol response for local files. Defaults to file not existing.'''
    status = STATUS_NOT_FOUND
    read = lambda: ''
    text = ''

def request_get(url):
    '''Request a URL.'''
    if url.startswith(LOCAL_PROTOCOL + '://'):
        # Local file
        from os.path import isabs, isfile
        # Remove the protocol prefix.
        path = url[len(LOCAL_PROTOCOL) + 3:]
        # Construct the response.
        response = LocalResponse()
        if isabs(path) and isfile(path):
            # File exists; populate the response.
            response.status = STATUS_OK
            response.read = open(path).read
    else:
        # Remote file
        import requests
        # Request the file
        response = requests.get(url)
        # Populate the response
        response.status = response.status_code
        response.read = lambda: response.text
    # Return the response
    return response

def make_person_url(host, about_loc, protocol=DEFAULT_PROTOCOL,
        local_access=False):
    '''Get the directory URL for a person.'''
    protocol_sep = '://'
    if host == LOCAL_HOST:
        if local_access:
            # Switch to local protocol.
            protocol = LOCAL_PROTOCOL
            host = LOCAL_HOST_PATH
        else:
            # Bodge. Ugh.
            protocol = protocol_sep = ''
    if '/' in about_loc or '~' in about_loc:
        # about_loc is a path.
        return '{}{}{}/{}/'.format(protocol, protocol_sep, host,
                about_loc.strip('/'))
    else:
        # about_loc is a username.
        return '{}{}{}/~{}/afrl/'.format(protocol, protocol_sep, host,
                about_loc)

EMAIL_OBFUSCATION_COUNTER = 1024
EMAIL_RE = re.compile(r'(mailto:)?[a-zA-Z0-9._\-]+@[a-zA-Z0-9._\-]+')

def obfuscate_email(email_string):
    '''Obfuscate a string.'''
    global EMAIL_OBFUSCATION_COUNTER
    import urllib
    EMAIL_OBFUSCATION_COUNTER += 15
    obfct = lambda: ''.join([chr((ord(c) + 32) ^ 0x3a)
        for c in str(EMAIL_OBFUSCATION_COUNTER)])
    return ('@@' + obfct() + '``'
            + urllib.quote(''.join([chr(ord(c) ^ 0x1f) for c in email_string]))
            + '``' + obfct() + '@@')

def obfuscate_emails(page_seg):
    '''Obfuscate the email addresses in a string.'''
    output = ""
    prev_end = 0
    for match in EMAIL_RE.finditer(page_seg):
        output += page_seg[prev_end:match.start()]
        output += obfuscate_email(match.group())
        prev_end = match.end()
    output += page_seg[prev_end:]
    return output

def person(name, about_loc, host=LOCAL_HOST, title=None, website=None,
        do_obfuscate_emails=True, css_classes=None):
    '''Generate the markdown for a person entry on a page.'''
    if css_classes is None:
        css_classes = DEFAULT_CSS_CLASSES
    # Get the person's directory URL, possibly switching to the local protocol.
    base_url = make_person_url(host, about_loc, local_access=True)
    # Probe for the about me file.
    for extension in ABOUTME_EXTENSIONS:
        aboutme_response = request_get(base_url + 'aboutme' + extension)
        if aboutme_response.status == 200:
            aboutme = aboutme_response.read()
            break
    else:
        aboutme = None
    # Probe for the photo.
    for extension in PHOTO_EXTENSIONS:
        photo_url = base_url + 'photo' + extension
        if request_get(photo_url).status == 200:
            if host == LOCAL_HOST:
                # Make the photo URL remote.
                photo_url = make_person_url(host, about_loc) + 'photo' \
                        + extension
            break
    else:
        photo_url = None
    # Render the person template.
    from template import render_template_env
    rendered = render_template_env(PERSON_TEMPLATE_FILE, name=name,
            title=title, aboutme=aboutme, photo_url=photo_url, website=website,
            css_classes=css_classes)
    if do_obfuscate_emails:
        return obfuscate_emails(rendered)
    return rendered

class Person(object):
    '''Convenience class for building up values to pass to `person`.'''

    def __init__(self, name, about_loc, host=LOCAL_HOST, title=None,
            website=None, css_classes=None):
        '''Arguments are the same as for `person`.'''
        if css_classes is None:
            css_classes = DEFAULT_CSS_CLASSES
        self.name = name
        self.about_loc = about_loc
        self.host = host
        self.title = title
        self.website = website
        self.css_classes = css_classes

    def person(self):
        '''Calls `person`.'''
        return person(self.name, self.about_loc, self.host, self.title,
                self.website, self.css_classes)

TACHIBANASITE_TPL_LIB_BINDINGS = {
        'people': sys.modules[__name__],
        'person': person,
        'Person': Person,
        'TACHIBANA': HOST_TACHIBANA,
        'CSE': HOST_CSE
        }
