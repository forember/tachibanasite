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

import csv, sys

def parse_csv(csv_path, default=''):
    '''Convert CSV header row and data rows.'''
    with open(csv_path) as csv_file:
        headers = next(csv.reader(iter([next(csv_file)])))
        reader = csv.DictReader(csv_file, fieldnames=headers, restval=default)
        rows = list(reader)
    return headers, rows

def parse_decimal(*args, **kwargs):
    '''Calls decimal.Decimal and raises a ValueError on InvalidOperation.'''
    import decimal
    try:
        return decimal.Decimal(*args, **kwargs)
    except decimal.InvalidOperation:
        raise ValueError

def csv2table(csv_path, default='', sort_func=None, sort_reverse=False,
        date_conversion=None, parse_number=parse_decimal, active=None):
    headers, rows = parse_csv(csv_path, default=default)
    if callable(parse_number):
        for row in rows:
            for key, val in row.items():
                try:
                    row[key] = parse_number(val)
                except ValueError:
                    pass
    if callable(sort_func):
        rows.sort(key=sort_func, reverse=sort_reverse)
    if date_conversion:
        in_format, out_format = date_conversion
        import time
        for row in rows:
            for key, val in row.items():
                try:
                    date = time.strptime(val, in_format)
                    row[key] = time.strftime(out_format, date)
                except TypeError:
                    pass
                except ValueError:
                    pass
    try:
        from urllib.parse import quote_plus
    except ImportError:
        from urllib import quote_plus
    header_markdown_list = ['[{}](?sortby={}&reverse={})'.format(
        '*{}*'.format(header) if header == active else header,
        quote_plus(header), int(header == active and not sort_reverse))
        for header in headers]
    table = ' | '.join(header_markdown_list) + '\n'
    table += ' | '.join('-'*len(headers)) + '\n'
    for row in rows:
        table += ' | '.join([str(row[field]) for field in headers]) + '\n'
    return table

def _get_sort_func_by_field(field_name):
    '''Return a function that accesses a item from its argument.'''
    def sort_func(dictionary):
        '''Returns a particular item from its argument.'''
        return dictionary[field_name]
    return sort_func

TACHIBANASITE_TPL_LIB_BINDINGS = {
        'csv2table': sys.modules[__name__]
        }
