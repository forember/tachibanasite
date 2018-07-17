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

def main():
    '''Entry point for autots.

    Reads arguments from sys.argv. Run `python2 -m autots -h` for usage.

    Returns a status code to be passed to `raise SystemExit()`.
    '''
    # Importing in the function prevents polluting the package namespace
    from .arg_parser import ARG_PARSER
    from .config import config
    from .delete import delete
    from .edit import create, edit
    from .install import install, upgrade
    from .lists import navlist, sidebar
    from .overrides import copyright, header
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
    elif args.subcommand == 'navlist':
        status = navlist(args)
    elif args.subcommand == 'upgrade':
        status = upgrade(args)
    elif args.subcommand == 'sidebar':
        status = sidebar(args)
    else:
        print 'Unknown subcommand.'
        status = 1
    return status
