#!/usr/bin/env python
'''
    File:   utils/template.py
    Author: Chris McKinney
    Edited: Mar 01 2016
    Editor: Chris McKinney

    Description:

    Utilities for working with template files.

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

# Render the template in the given environment.
def render_template_env(filename, **environment):
    from bottle import SimpleTemplate
    with open(filename) as f:
        return SimpleTemplate(f, name=filename).render(**environment)

# Render the template in the default environment, with additional values.
def render_template(filename, **environment):
    env = DEFAULT_TEMPLATE_ENV.copy()
    env.update(environment)
    return render_template_env(filename, **env)

import people

# The default environment for render_template.
DEFAULT_TEMPLATE_ENV = {
        '_GET': {},
        'render_template_env': render_template_env,
        'render_template': render_template,
        'people': people,
        'person': people.person,
        'Person': people.Person,
        'TACHIBANA': people.HOST_TACHIBANA,
        'CSE':  people.HOST_CSE,
        }

# Render each template file provided to the script.
def main():
    import sys, json
    _GET = json.loads(sys.argv[1])
    for filename in sys.argv[2:]:
        print(render_template(filename, _GET=_GET))

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
