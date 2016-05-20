'''
    File:   utils/people.py
    Author: Chris McKinney
    Edited: Mar 01 2016
    Editor: Chris McKinney

    Description:

    Provides person objects and utilities.

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
installPath = dirname(dirname(realpath(__file__)))
import configIniUtils

# File extensions. Revisit these periodically to sort common extensions first.
ABOUTME_EXTENSIONS = ['.markdown', '', '.mdown', '.md', '.text', '.txt', '.html']
PHOTO_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.ico']

# Available hosts.
HOST_TACHIBANA = 'tachibanatech.com'
HOST_AFRL = 'afrl.cse.sc.edu'
HOST_CSE = 'cse.sc.edu'

# Default request protocol. Should probably stay HTTP or HTTPS.
DEFAULT_PROTOCOL = 'https'
# Status codes
STATUS_OK = 200
STATUS_NOT_FOUND = 404

# Local file protocol. "file" is standard.
LOCAL_PROTOCOL = 'file'
# The host the site is installed on.
LOCAL_HOST = HOST_TACHIBANA
# The path on the local host that is root for DEFAULT_PROTOCOL requests.
LOCAL_HOST_PATH = configIniUtils.get_local_host_path()

# The relative path to the person template.
PERSON_TEMPLATE_FILE = os.path.join(installPath,
        'utils/person.markdown.template')

# A protocol response for local files. Defaults to file not existing.
class LocalResponse (object):
    status = STATUS_NOT_FOUND
    read = lambda: ''

# Request a URL.
def request_get(url):
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

# Get the directory URL for a person.
def make_person_url(host, about_loc, protocol=DEFAULT_PROTOCOL,
        local_access=False):
    if local_access and host == LOCAL_HOST:
        # Switch to local protocol.
        protocol = LOCAL_PROTOCOL
        host = LOCAL_HOST_PATH
    if '/' in about_loc or '~' in about_loc:
        # about_loc is a path.
        return '{}://{}/{}/'.format(protocol, host, about_loc.strip('/'))
    else:
        # about_loc is a username.
        return '{}://{}/~{}/afrl/'.format(protocol, host, about_loc)

def person(name, about_loc, host=HOST_TACHIBANA, title=None, website=None):
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
    return render_template_env(PERSON_TEMPLATE_FILE, name=name, title=title,
            aboutme=aboutme, photo_url=photo_url, website=website)

class Person (object):
    def __init__(self, name, about_loc, host=HOST_TACHIBANA, title=None,
            website=None):
        self.name = name
        self.about_loc = about_loc
        self.host = host
        self.title = title
        self.website = website

    def person(self):
        return person(self.name, self.about_loc, self.host, self.title,
                self.website)