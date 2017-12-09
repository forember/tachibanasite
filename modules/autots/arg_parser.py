'''
    File:   ./modules/autots/arg_parser.py
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

import argparse
from .utils import FORCE_TEMPLATES

def get_base_arg_list(args):
    base_arg_list = ['--page', args.page]
    if args.force:
        base_arg_list.append('--force')
    if not args.interactive:
        base_arg_list.append('--non-interactive')
    return base_arg_list

def _create_parser():
    parser = argparse.ArgumentParser(
            description='Manage a TachibanaSite install.')
    parser.add_argument('-f', '--force', action='store_const', const=True,
            help='Overwrite manually created files.')
    parser.add_argument('-n', '--non-interactive', action='store_false',
            dest='interactive', help="Don't display interactive prompts")
    parser.add_argument('-p', '--page', '--page-directory', default='common',
            help='Page directory to operate on (relative to site directory).' +
            ' If not specified, defaults to site-global.')
    subparsers = parser.add_subparsers(dest='subcommand', metavar='subcommand')
    # Config Subcommand
    config_parser = subparsers.add_parser('config',
            help='Do basic setup for TachibanaSite.')
    config_parser.add_argument('-d', '--domain-name', '--domain',
            help='Domain name.')
    config_parser.add_argument('-e', '--email', help='Your email address.')
    config_parser.add_argument('-i', '--title', '--site-title',
            help='Title of the site.')
    config_parser.add_argument('-l', '--local-host-path', '--lhp',
            help='Path on disk for the root of this domain.')
    if not FORCE_TEMPLATES:
        config_parser.add_argument('-m', '--no-templates',
                '--disable-templates', action='store_const', const=False,
                dest='templates', help='Disable templating.')
    config_parser.add_argument('-r', '--recursive',
            '--recursive-common-overrides', action='store_const', const=True,
            help='Subpages inherit common override files.')
    config_parser.add_argument('-s', '--ssl', '--force-ssl',
            action='store_const', const=True,
            help='Redirect all traffic to use SSL.')
    config_parser.add_argument('-t', '--theme', '--theme-name',
            help='Theme for the site.')
    config_parser.add_argument('--install-url',
            help='Absolute URL path part to TS install directory.')
    config_parser.add_argument('--no-recursive', action='store_const',
            const=True, dest='recursive',
            help='Subpages do not inherit common override files.')
    config_parser.add_argument('--no-ssl', '--no-force-ssl',
            action='store_const', const=False, dest='ssl',
            help='Do not redirect traffic to use SSL.')
    config_parser.add_argument('--sender-email', help='Sender email address.')
    if not FORCE_TEMPLATES:
        config_parser.add_argument('--templates', '--enable-templates',
                action='store_const', const=True, help='Enable templating.')
    config_parser.add_argument('--theme-ini', nargs='*',
            help='Additional lines of INI after [Theme].')
    # Copyright Subcommand
    copyright_parser = subparsers.add_parser('copyright',
            help='Set copyright information.')
    copyright_parser.add_argument('-c', '--notice',
            help='Copyright notice (e.g. 2017 Chris McKinney).')
    # Create Subcommand
    create_parser = subparsers.add_parser('create', help=('Create a page.' +
        ' Note: Attempting to create page "common" will create page "home."'))
    # Edit Subcommand
    edit_parser = subparsers.add_parser('edit',
            help='Edit a page, creating it if it does not exist.')
    edit_parser.add_argument('-e', '--editor',
            help='The editor to use (e.g. nano, vim, emacs).')
    edit_parser.add_argument('-m', '--no-template', action='store_const',
            const=False, dest='template', help='Disable embedded python.')
    edit_parser.add_argument('-t', '--template', action='store_const',
            const=True, help='Use SimpleTemplate syntax to embed python.')
    # Delete Subcommand
    delete_parser = subparsers.add_parser('delete', help='Delete a page.')
    delete_parser.add_argument('-e', '--erase', '--always-erase',
            action='store_const', const=True,
            help=('Fully erase all non-subpage content even if there are' +
                ' subpages that may use it.'))
    delete_parser.add_argument('-l', '--follow-link', action='store_const',
            const=True, help='Follow if the page directory is a symlink.')
    delete_parser.add_argument('-r', '--recursive', action='store_const',
            const=True, help='Also delete subpages. Implies -e.')
    # Header Subcommand
    header_parser = subparsers.add_parser('header', help='Set header.')
    header_parser.add_argument('-l', '--linked', action='store_const',
            const=True, help='Header is a link to home.')
    header_parser.add_argument('-m', '--not-linked', action='store_const',
            const=False, dest='linked', help='Header is plain text.')
    header_parser.add_argument('-t', '--header', '--text',
            help='Header text to go at the top of pages (markdown template).')
    # Install Subcommand
    install_parser = subparsers.add_parser('install',
            help='Install TachibanaSite.')
    install_parser.add_argument('-m', '--no-deps', action='store_false',
            dest='deps', help="Don't attempt to install dependencies.")
    # Upgrade Subcommand
    upgrade_parser = subparsers.add_parser('upgrade',
            help='Upgrade TachibanaSite.')
    upgrade_parser.add_argument('-m', '--no-deps', action='store_false',
            dest='deps', help="Don't attempt to install dependencies.")
    return parser

ARG_PARSER = _create_parser()
