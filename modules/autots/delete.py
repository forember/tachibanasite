'''
    File:   ./modules/autots/delete.py
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
import shutil

from .utils import Asker, SITE_PATH

def get_page_erasure(page_path):
    files_to_delete = []
    dirs_to_delete = []
    for root, dirnames, filenames in os.walk(page_path):
        if root == page_path:
            files_to_delete.extend(filenames)
        elif 'index.php' in filenames:
            del dirnames[:]
            ancestor = os.path.dirname(root)
            while ancestor != page_path:
                try:
                    dirs_to_delete.remove(ancestor)
                except ValueError:
                    print 'ERROR: Could not whitelist:'
                    print '    {}'.format(ancestor)
                    print '  Ancestor of:'
                    print '    {}'.format(root)
                    print 'It is recommended you do not proceed.'
                next_ancestor = os.path.dirname(page_path)
                if next_ancestor == ancestor:
                    break
                ancestor = next_ancestor
        else:
            dirs_to_delete.append(root)
    files_to_delete.sort()
    dirs_to_delete.sort()
    print 'The following files will be deleted:'
    for filename in files_to_delete:
        print '  {}'.format(filename)
    print 'The following directories will be deleted:'
    for dirname in dirs_to_delete:
        print '  {}'.format(dirname)
    return files_to_delete, dirs_to_delete

def delete(args):
    ask = Asker(args.interactive)
    page = ask.string('What page do you want to delete?',
            None if args.page == 'common' else args.page, 'common')
    if page == 'common':
        print 'Refusing to delete the common directory. If you want to'
        print 'remove TachibanaSite, you can just delete the site directory.'
        print 'Aborting.'
        return 1
    page_path = pjoin(SITE_PATH, page)
    if not os.path.lexists(page_path):
        print 'There is no such page: {}. Aborting.'.format(page)
        return 1
    do_deletion = None
    if os.path.islink(page_path):
        old_page_path = page_path
        def ask_delete_link():
            if ask.yes_no('Do you want to delete the link?',
                    args.recursive, False):
                print 'The link {} will be deleted.'.format(old_page_path)
                return lambda: os.remove(old_page_path)
            else:
                print 'Refusing to delete symlinked page. Aborting.'
                return None
        if ask.yes_no('{} is a link. Follow it?'.format(page),
                args.follow_link, False):
            page_path = os.path.realpath(page_path)
            if not os.path.isdir(page_path):
                print 'No such directory: {}'.format(page_path)
                do_deletion = ask_delete_link()
                if do_deletion is None:
                    return 1
        else:
            do_deletion = ask_delete_link()
            if do_deletion is None:
                return 1
    else:
        page_path = os.path.realpath(page_path)
    if not os.path.isdir(page_path):
        print 'No such directory: {}'.format(page_path)
        print 'Aborting.'
        return 1
    if do_deletion is None:
        has_subpages = False
        for root, dirnames, filenames in os.walk(page_path):
            if 'index.php' in filenames and root != page_path:
                has_subpages = True
                break
        recursive = True
        erase = False
        if has_subpages:
            recursive = ask.yes_no('Do you also want to delete subpages?',
                    args.recursive, False)
            if not recursive:
                erase = ask.yes_no(('Erase all non-subpage content that may be'
                    + ' used by subpages?'), args.erase, False)
        if recursive:
            print 'The directory {} will be deleted.'.format(page_path)
            do_deletion = lambda: shutil.rmtree(page_path)
        elif erase:
            files_to_delete, dirs_to_delete = get_page_erasure(page_path)
            def do_deletion():
                for filename in files_to_delete:
                    os.remove(filename)
                for dirname in dirs_to_delete:
                    shutil.rmtree(dirname)
        else:
            index_php = pjoin(page_path, 'index.php')
            print 'The file {} will be deleted.'.format(index.php)
            do_deletion = lambda: os.remove(index_php)
    if not ask.yes_no('Are you sure you want to do this?', None,
            not args.interactive):
        print 'Aborting.'
        return 1
    do_deletion()
    print 'Deleted.'
