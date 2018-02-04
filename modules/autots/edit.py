'''
    File:   ./modules/autots/edit.py
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

from .arg_parser import ARG_PARSER, get_base_arg_list
from .utils import *

def create(args):
    ask = Asker(args.interactive)
    page = ask.string('Where do you want to create the page?',
            None if args.page == 'common' else args.page, 'home')
    page_path = pjoin(SITE_PATH, page)
    index_php = pjoin(page_path, 'index.php')
    source_lines = read_existing(index_php, ask, args.force)
    if source_lines is None:
        return 1
    # Get path to FindStandardPage.php
    fsp_path = os.path.relpath(pjoin(pjoin(INSTALL_PATH, 'utils'),
        'FindStandardPage.php'), page_path)
    # Generate
    index_php_lines = [
            '<?php // {}'.format(AUTOTS_NOTICE),
            "include '{}'; ?>".format(ini_quote_path(fsp_path))]
    return show_confirm_write(index_php, index_php_lines, ask)

def edit(args):
    import subprocess
    ask = Asker(args.interactive)
    page_path = pjoin(SITE_PATH, args.page)
    index_md = pjoin(page_path, 'index.markdown')
    index_md_tpl = pjoin(page_path, 'index.markdown.template')
    template = ask.yes_no('Enable embedded python in this file?',
            args.template, default_arg(not os.path.isfile(index_md), True))
    if template and os.path.isfile(index_md):
        os.rename(index_md, index_md_tpl)
    elif not template and os.path.isfile(index_md_tpl):
        os.rename(index_md_tpl, index_md)
    if template:
        index_md = index_md_tpl
    if (not os.path.isfile(pjoin(page_path, 'index.php')) and
            args.page != 'common'):
        base_arg_list = get_base_arg_list(args)
        create(ARG_PARSER.parse_args())
    if args.interactive:
        env_editor = os.getenv('EDITOR')
        if args.editor is not None:
            editor = args.editor
        elif env_editor:
            editor = env_editor
        else:
            editors = ['nano', 'nvim', 'vim', 'emacs', 'vi']
            for e in editors:
                if subprocess.call(['which', e]) == 0:
                    editor = e
                    break
            else:
                editor = 'nano'
        command = [editor]
        if 'vim' in command:
            command.append('+set ft=markdown nocp')
        command.append(index_md)
        subprocess.call(command)
    print 'Done.'
