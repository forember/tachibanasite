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

from .utils import *

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
            source.notice = ini_unquote_html(source.notice[6:].strip())
    # Ask for Notice
    notice = ask.string('Copyright notice (c)', args.notice,
            default_arg(source.notice, str(datetime.date.today().year)))
    if notice:
        notice = '&copy; {}'.format(ini_quote_html(notice))
    # Generate
    copy_md_lines = ['<!-- {} -->'.format(AUTOTS_NOTICE), notice]
    return show_confirm_write(copy_md, copy_md_lines, ask)

def header(args):
    ask = Asker(args.interactive)
    page_path = pjoin(SITE_PATH, args.page)
    head_md = pjoin(page_path, 'header.markdown.template')
    source_lines = read_existing(head_md, ask, args.force)
    if source_lines is None:
        return 1
    # Parse Existing
    source = argparse.Namespace()
    source.linked, source.header = match_line(source_lines,
            r'# (\[)?(.*)(?(1)\]\(\{\{base\}\}/\))',
            (1, 2), lambda s: None if s is None else ini_unquote_html(s))
    if source.header is not None:
        source.linked = bool(source.linked)
    # Ask for Header and Linked
    header = ask.string('Header text', args.header,
            default_arg(source.header, ''))
    linked = ask.yes_no('Should the header be a link home?', args.linked,
            default_arg(source.linked, True))
    # Generate
    head_md_lines = ['<!-- {} -->'.format(AUTOTS_NOTICE)]
    if linked:
        head_md_lines.extend([
            '<%', 'import os.path, configIniUtils',
            'base = os.path.dirname(configIniUtils.get_install_url())', '%>',
            '# [{}]({{{{base}}}}/)'.format(ini_quote_html(header))])
    else:
        head_md_lines.append('# {}'.format(ini_quote_html(header)))
    return show_confirm_write(head_md, head_md_lines, ask)
