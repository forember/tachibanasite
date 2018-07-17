'''
    File:   ./modules/autots/config.py
    Author: Chris McKinney
    Edited: Dec 09 2017
    Editor: Chris McKinney

    Description:

    Manages common/config.ini.

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

from .utils import *

def parse_config(source_lines):
    '''Parse a TachibanaSite config.ini.

    :param source_lines: A sequence of lines from a config.ini.
    TODO
    '''
    def match_source(pattern, group=0, filt=lambda s: s):
        return match_line(source_lines, pattern, group, filt)
    source = argparse.Namespace()
    source.title = match_source('site_title = "(.*)"', 1, ini_unquote_html)
    source.local_host_path = match_source('local_host_path = "(.*)"', 1,
            ini_unquote_path)
    source.ssl = match_source('force_ssl = (yes|no)', 1, lambda a: a == 'yes')
    source.sender_email = match_source('sender_email = "(.*)"', 1,
            ini_unquote_path)
    source.domain_name = None
    if source.sender_email:
        source.domain_name = source.sender_email[
                source.sender_email.find('@') + 1:]
    source.install_url = match_source('install_url = "(.*)"', 1,
            ini_unquote_url)
    source.email = match_source('email = "(.*)"$', 1, ini_unquote_path)
    if not FORCE_TEMPLATES:
        source.templates = match_source('enable_templates = (yes|no)', 1,
                lambda a: a == 'yes')
    source.recursive = match_source('recursive_common_override = (yes|no)',
            1, lambda a: a == 'yes')
    source.theme = match_source('theme_name = "(.*)"', 1, ini_unquote_path)
    try:
        source.theme_ini = source_lines[source_lines.index('[Theme]') + 1:]
    except ValueError:
        source.theme_ini = []
    return source

def configure_theme(theme, config_ini_lines, args, source, ask):
    # Theme Compatibility
    if theme in ['coloredpencil', 'bootstrap']:
        config_ini_lines.extend(['', '[Modules]', 'mobiletext_disabled = yes'])
    if theme == 'coloredpencil':
        config_ini_lines.append('bootstrap4_disabled = no')
    elif theme == 'bootstrap':
        config_ini_lines.extend(['bootstrap_disabled = no',
            'bootstrapify_disabled = no'])
    # Additional Theme Configuration
    if args.theme_ini:
        config_ini_lines.extend(['', '[Theme]'])
        config_ini_lines.extend(args.theme_ini)
    elif source.theme_ini and not ask.yes_no(
            'Would you like to overwrite the theme configuration?', None,
            theme != source.theme):
        config_ini_lines.extend(['', '[Theme]'])
        config_ini_lines.extend(source.theme_ini)
    elif theme == 'default':
        preset = ask.choice('Available color schemes for default theme:',
                'Select a scheme', ['default', 'red', 'green', 'teal',
                    'blue', 'purple'], 'green')
        config_ini_lines.extend(['', '[Theme]',
            'preset = "{}"'.format(ini_quote_path(preset))])
    elif theme == 'coloredpencil':
        preset = ask.choice(
                'Available color schemes for colored pencil theme:',
                'Select a scheme', ['default', 'red', 'legal', 'celery',
                    'periwinkle', 'tapioca', 'salmon', 'colorful',
                    'custom'], 'default')
        caleb = ask.yes_no('Should headers be the same color as links?',
                None, False);
        if preset == 'custom':
            bg = ask.string('What color should the background be?', None,
                    '#eee')
            text = ask.string('What color should the text be?', None,
                    '#111')
            link = ask.string('What color should the links be?', None,
                    '#33c')
            config_ini_lines.extend(['', '[Theme]',
                'bg = "{}"'.format(ini_quote_path(bg)),
                'text = "{}"'.format(ini_quote_path(text)),
                'link = "{}"'.format(ini_quote_path(link))])
            if not caleb:
                head = ask.string('What color should the headers be?',
                        None, '#555')
                config_ini_lines.append('head = "{}"'.format(
                    ini_quote_path(head)))
        else:
            dark = ask.yes_no(
                    'Would you prefer the dark version of this scheme?',
                    None, False)
            config_ini_lines.extend(['', '[Theme]',
                'preset = "{}"'.format(ini_quote_path(preset)),
                'dark = {}'.format('yes' if dark else 'no')])
        if caleb:
            config_ini_lines.append('caleb = yes')

def config(args):
    ask = Asker(args.interactive)
    page_path = pjoin(SITE_PATH, args.page)
    config_ini = pjoin(page_path, 'config.ini')
    source_lines = read_existing(config_ini, ask, args.force)
    if source_lines is None:
        return 1
    # Parse Existing Config
    source = parse_config(source_lines)
    # Title
    title = ask.string('What is the title of your site?', args.title,
            default_arg(source.title, ''))
    # Local Host Path
    local_host_path = None
    while local_host_path is None or not os.path.isdir(local_host_path):
        if local_host_path is not None:
            print 'That path is not a real directory on disk.'
        local_host_path = os.path.realpath(
                ask.string('Where is the root for this domain on disk?',
                    args.local_host_path,
                    default_arg(source.local_host_path, SITE_PATH)))
        if ('"' in local_host_path or '\\' in local_host_path
                or '$' in local_host_path):
            print 'The path you provided contains a ", \\, or $ character.'
            print 'This may cause problems for some features of TachibanaSite.'
            if not ask.yes_no('Install here anyway?', args.local_host_path,
                    source.local_host_path is not None and
                    local_host_path == source.local_host_path):
                print 'Aborting.'
                return 1
    # Force SSL
    ssl = ask.yes_no('Force all traffic to SSL?', args.ssl,
            default_arg(source.ssl, False))
    # Domain Name
    domain_name = ask.string('What is your domain name?',
            args.domain_name, default_arg(source.domain_name, 'localhost'))
    # Verify Install URL
    install_url = '/' + os.path.relpath(INSTALL_PATH, local_host_path)
    print 'Based on what you have said, your site will be accessed at:'
    print '    http{}://{}{}{}'.format('s' if ssl else '',
            domain_name, dirname(install_url),
            '' if dirname(install_url)[-1] == '/' else '/')
    if not ask.yes_no('Is this correct?',
            False if args.install_url is not None else None,
            True if source.install_url is None else False):
        print 'Manually overriding the install URL. Do this at your own risk.'
        install_url = ask.string('Install URL', args.install_url,
                default_arg(source.install_url, install_url))
    # Email Address
    email = ask.string('What is your email address?', args.email,
            default_arg(source.email, ''))
    # Verify Sender Email Address
    sender_email = 'tachibanasite@{}'.format(domain_name)
    print 'Based on what you have said, your site will send mail as:'
    print '    {}'.format(sender_email)
    if not ask.yes_no('Is this okay?',
            False if args.sender_email is not None else None,
            True if source.sender_email is None else False):
        print 'Manually overriding the sender email. Do this at your own risk.'
        sender_email = ask.string('Sender Email', args.sender_email,
                default_arg(source.sender_email, sender_email))
    # Templates
    if not FORCE_TEMPLATES:
        templates = ask.yes_no('Enable templating?', args.templates,
                default_arg(source.templates, True))
    else:
        templates = True
    # Recursive common overrides
    recursive = ask.yes_no('Should subpages inherit common override files?',
            args.recursive, default_arg(source.recursive, False))
    # Theme
    if args.theme is None:
        theme = ask.choice('Available default themes:', 'Select a theme',
                ['coloredpencil', 'bold', 'barebones'],
                default_arg(source.theme, 'coloredpencil'))
    else:
        theme = ask.string('Theme name', args.theme,
                default_arg(source.theme, 'coloredpencil'))
    # Generate Config
    config_ini_lines = [
            '; {}'.format(AUTOTS_NOTICE),
            '[TachibanaSite]',
            'site_title = "{}"'.format(ini_quote_html(title)),
            'local_host_path = "{}"'.format(ini_quote_path(local_host_path)),
            'force_ssl = {}'.format('yes' if ssl else 'no'),
            'install_url = "{}"'.format(ini_quote_url(install_url)),
            'email = "{}"'.format(ini_quote_path(email)),
            'sender_email = "{}"'.format(ini_quote_path(sender_email)),
            'enable_templates = {}'.format('yes' if templates else 'no'),
            'recursive_common_override = {}'.format(
                'yes' if recursive else 'no'),
            'theme_name = "{}"'.format(ini_quote_path(theme))]
    configure_theme(theme, config_ini_lines, args, source, ask)
    return show_confirm_write(config_ini, config_ini_lines, ask)

