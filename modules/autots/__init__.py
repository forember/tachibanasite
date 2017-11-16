#!/usr/bin/env python

import argparse
import os
import os.path
from os.path import dirname
from os.path import join as pjoin
import re
import urllib

DIRNAME0 = dirname(os.path.realpath(__file__))
INSTALL_PATH = dirname(dirname(DIRNAME0))
SITE_PATH = dirname(INSTALL_PATH)

FORCE_TEMPLATES = True

def checkauto(filename):
    if not os.path.exists(filename):
        return True
    if not os.path.isfile(filename):
        return False
    with open(filename) as f:
        try:
            line = next(f)
            return '!!AUTOTS!!' in line
        except StopIteration:
            return True

def ask_yes_no(message, arg=None, default=None, interactive=True):
    if arg is not None:
        return arg
    if not interactive:
        return default
    message += ' ['
    message += 'Y' if default else 'y'
    message += '/'
    message += 'n' if default or default is None else 'N'
    message += ']'
    answer = None
    while answer is None:
        response = raw_input(message)
        if not response:
            answer = default
        elif response[0].lower() == 'y':
            answer = True
        elif response[0].lower() == 'n':
            answer = False
    return answer

def ask_string(message, arg=None, default=None, interactive=True):
    if arg is not None:
        return arg
    if not interactive:
        return default
    message += ' [{}]'.format(default)
    answer = None
    while answer is None:
        response = raw_input(message)
        if not response:
            answer = default
        else:
            answer = response
    return answer

def ask_choice(prelist, message, options, default=None, interactive=True):
    def interpret_answer(answer):
        if answer in options:
            return answer
        try:
            return options[int(answer)]
        except ValueError, IndexError:
            return None
    if not interactive:
        option = interpret_answer(default)
        if option is None:
            return default
        return option
    print prelist
    for i, option in enumerate(options):
        print '{: 2d}. {}'.format(i, option)
    option = None
    while option is None:
        try:
            option = interpret_answer(ask_string(message, None, default,
                interactive))
        except ValueError:
            pass
    return option

class Asker (object):
    def __init__(self, interactive=True):
        self.interactive = interactive

    def yes_no(self, message, arg=None, default=None):
        return ask_yes_no(message, arg, default, self.interactive)

    def string(self, message, arg=None, default=None):
        return ask_string(message, arg, default, self.interactive)

    def choice(self, prelist, message, options, default=None):
        return ask_choice(prelist, message, options, default, self.interactive)

def ini_quote_html(s):
    from xml.sax.saxutils import escape
    return (escape(s).replace('"', '&quot;').replace("'", '&apos;')
            .replace('\\', '&#92;').replace('$', '&#36;'))

def ini_unquote_html(s):
    from xml.sax.saxutils import unescape
    return unescape(s)

def ini_quote_path(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')

def ini_unquote_path(s):
    r = ''
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 != len(s):
            d = s[i + 1]
            if d in '\\"$':
                r += d
                i += 2
                continue
        r += c
        i += 1
    return r

def ini_quote_url(s):
    return urllib.quote(s)

def ini_unquote_url(s):
    return urllib.unquote(s)

def default_arg(source_arg, default=None):
    if source_arg is None:
        return default
    else:
        return source_arg

def read_existing(file_path, ask, force):
    # Check If Manual Mode
    if not checkauto(file_path):
        print '{} has already been manually created.'.format(file_path)
        if not ask.yes_no('Overwrite it?', force, False):
            print 'Aborting.'
            return None
    # Read Existing Config
    source_lines = []
    if os.path.isfile(config_ini):
        with open(config_ini) as f:
            source_lines = [line.strip() for line in f]
    return source_lines

def show_confirm_write(file_path, lines, ask):
    # Output Content to Be Written
    print 'The following will be output to {}:'.format(file_path)
    print
    for line in lines:
        print '    {}'.format(line)
    print
    # Ask to Write
    if not ask.yes_no('Continue (cannot be undone)?', None,
            None if ask.interactive else True):
        print 'Aborting.'
        return 1
    # Write Output
    page_path = os.path.dirname(file_path)
    if not os.path.isdir(page_path):
        os.makedirs(page_path, 0775)
    with open(file_path, 'w') as f:
        f.writelines([line + '\n' for line in lines])
    return 0

def config(args):
    ask = Asker(args.interactive)
    page_path = pjoin(SITE_PATH, args.page)
    config_ini = pjoin(page_path, 'config.ini')
    source_lines = read_existing(config_ini, ask, args.force)
    if source_lines is None:
        return 1
    # Parse Existing Config
    def match_source(pattern, group=0, filt=lambda s: s):
        for source_line in source_lines:
            m = re.match(pattern.replace(' ', '\\s*') + '$', source_line)
            if m:
                return m.group(group)
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
                ['default', 'coloredpencil', 'bootstrap', 'paper',
                    'barebones'], default_arg(source.theme, 'coloredpencil'))
    else:
        theme = ask.string('Theme name', args.theme,
                default_arg(source.theme, 'coloredpencil'))
    # Generate Config
    config_ini_lines = [
            '; !!AUTOTS!! Created by autots. Do not manually edit.',
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
    return show_confirm_write(config_ini, config_ini_lines, ask)

def copyright(args):
    import datetime
    ask = Asker(args.interactive)
    page_path = pjoin(SITE_PATH, args.page)
    copy_md = pjoin(page_path, 'copyright.markdown')
    source_lines = read_existing(copy_md, ask, args.force)
    if source_lines is None:
        return 1
    # Parse Existing
    source = argparse.Namespace()
    source.notice = None
    if len(source_lines) > 1:
        source.notice = source_lines[1]
        if source.notice.startswith('&copy;'):
            source.notice = source.notice[6:].strip()
    # Ask for Notice
    notice = ask.string('Copyright notice (c)', args.notice,
            default_arg(source.notice, str(datetime.date.today().year)))
    if notice:
        notice = '&copy; {}'.format(notice)
    # Generate
    copy_md_lines = [
            '<!-- !!AUTOTS!! Created by autots. Do not manually edit. -->',
            notice]
    return show_confirm_write(copy_md, copy_md_lines, ask)

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
    copyright_parser.add_argument('--notice',
            help='Copyright notice (e.g. 2017 Chris McKinney).')
    return parser

ARG_PARSER = _create_parser()

def main():
    # Parse and Execute
    args = ARG_PARSER.parse_args()
    print 'AUTOTS Alpha'
    if args.subcommand == 'config':
        status = config(args)
    elif args.subcommand == 'copyright':
        status = copyright(args)
    else:
        print 'Unknown subcommand.'
        status = 1
    raise SystemExit(status)

if __name__ == '__main__':
    main()
