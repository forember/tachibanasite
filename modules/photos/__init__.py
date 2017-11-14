'''
    File:   ./modules/photos/__init__.py
    Author: Chris McKinney
    Edited: Aug 22 2016
    Editor: Chris McKinney

    Description:

    Provides utilities for creating thumbnails and displaying them.

    Edit History:

    0.6.20  - Created module.

    0.8.10  - Added TachibanaSite template library bindings.

    0.8.18  - Added more generic photo-and-link function.

    0.8.22  - Added caption and hover filter support.

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
MODULE_PATH = dirname(realpath(__file__))

# The relative path to the person template.
TWOCOL_THUMB_TEMPLATE_FILE = os.path.join(MODULE_PATH,
        'twocolumn_thumbnail.markdown.template')

def thumbnail_filename(photo_filename, maxdim=750):
    '''Generates and returns a thumbnail of an image with caching.'''
    import hashlib
    from os.path import isfile
    digestfile = photo_filename + '.md5'
    thumbfile = photo_filename + '.thumbnail.jpeg'
    with open(photo_filename, 'rb') as photo_file:
        photo_data = True
        md5_hash = hashlib.md5()
        while photo_data:
            photo_data = photo_file.read(0x1000)
            md5_hash.update(photo_data)
        digest = md5_hash.hexdigest().strip()
    if not (isfile(digestfile) and open(digestfile).read().strip() == digest):
        from PIL import Image
        photo = Image.open(photo_filename)
        photo.thumbnail((maxdim, maxdim), Image.ANTIALIAS)
        photo.save(thumbfile)
        with open(digestfile, 'w') as dfobj:
            dfobj.writelines([digest])
    return thumbfile

def twocolumn_thumbnail(photo_filename, columns=2, maxdim=750, link=None,
        caption=None, hover_filter=None):
    '''Generates markdown for inserting a thumbnail into a page.'''
    if link is None:
        link = photo_filename
    # Render the thumbnail template.
    from template import render_template_env
    return render_template_env(TWOCOL_THUMB_TEMPLATE_FILE,
            columns=columns, maxdim=maxdim, link=link,
            thumbnail=thumbnail_filename(photo_filename, maxdim),
            caption=caption, hover_filter=hover_filter)

TACHIBANASITE_TPL_LIB_BINDINGS = {
        'thumbnail_filename': thumbnail_filename,
        'twocolumn_thumbnail': twocolumn_thumbnail,
        }
