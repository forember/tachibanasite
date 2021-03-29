#!/usr/bin/env python2
'''
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

import sys

def render_template_env(filename, **environment):
    '''Render the template in the given environment.'''
    from bottle import SimpleTemplate
    with open(filename) as fileobj:
        return SimpleTemplate(fileobj, name=filename).render(**environment)

def render_template(filename, **environment):
    '''Render the template in the default environment with additional values.'''
    env = DEFAULT_TEMPLATE_ENV.copy()
    env.update(environment)
    return render_template_env(filename, **env)

def _get_tpl_lib_bindings():
    '''Gets bindings from modules.'''
    import importlib
    import os
    from os.path import dirname, realpath
    import ConfigParser
    from configIniUtils import get_config
    install_path = dirname(dirname(realpath(__file__)))
    modules_path = os.path.join(install_path, 'modules')
    if os.path.isdir(modules_path):
        sys.path.append(modules_path)
        module_names = os.listdir(modules_path)
    else:
        module_names = []
    module_names.sort()
    bindings = []
    for name in module_names:
        if '.' in name:
            continue
        try:
            if get_config().get('Modules', '{}_disabled'.format(name)
                    ).lower() == 'yes':
                continue
        except ConfigParser.NoOptionError:
            pass
        module_init = os.path.join(os.path.join(modules_path, name),
                '__init__.py')
        if not os.path.isfile(module_init):
            continue
        try:
            module = importlib.import_module(name)
            bindings.append(module.TACHIBANASITE_TPL_LIB_BINDINGS)
        except ImportError:
            continue
        except AttributeError:
            continue
    return bindings

class FormEmu:
    def __init__(self, _GET):
        self._GET = _GET

    def getlist(self, key):
        if key.endswith("[]"):
            return self._GET[key[:-2]]
        if key not in self._GET:
            return []
        else:
            return [self._GET[key]]

# The default environment for render_template.
DEFAULT_TEMPLATE_ENV = {
        '_GET': {},
        '_FORM': FormEmu({}),
        'render_template_env': render_template_env,
        'render_template': render_template,
        }

for lib_bindings in _get_tpl_lib_bindings():
    DEFAULT_TEMPLATE_ENV.update(lib_bindings)

def main():
    '''Render each template file provided to the script.'''
    import json
    get_list = json.loads(sys.argv[1])
    for filename in sys.argv[2:]:
        print render_template(filename, _GET=get_list, _FORM=FormEmu(get_list))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
