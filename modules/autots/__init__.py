'''
    File:   ./modules/autots/__init__.py
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

from .arg_parser import ARG_PARSER
from .config import config
from .delete import delete
from .edit import create, edit
from .install import install, upgrade
from .overrides import copyright, header

def main():
    # Parse and Execute
    args = ARG_PARSER.parse_args()
    print 'AUTOTS Alpha'
    if args.subcommand == 'config':
        status = config(args)
    elif args.subcommand == 'copyright':
        status = copyright(args)
    elif args.subcommand == 'create':
        status = create(args)
    elif args.subcommand == 'edit':
        status = edit(args)
    elif args.subcommand == 'delete':
        status = delete(args)
    elif args.subcommand == 'header':
        status = header(args)
    elif args.subcommand == 'install':
        status = install(args)
    elif args.subcommand == 'upgrade':
        status = upgrade(args)
    else:
        print 'Unknown subcommand.'
        status = 1
    return status
