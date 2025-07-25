#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2025, Roland Rickborn (r_2@gmx.net)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Revision history:
# 2022-12-20  Created
# 2022-12-29  Updated
# 2023-02-20  Extended
# 2025-07-24  Extended
#
# ---------------------------------------------------------------------------

import argparse
import sys

try:
    import src.ebm.bm2xls as bm2xls
    import src.ebm.utils as utils
    import src.ebm.xls2bm as xls2bm
except ModuleNotFoundError:
    import bm2xls
    import utils
    import xls2bm

__author__ = 'Roland Rickborn'
__copyright__ = 'Copyright (c) 2025 {}'.format(__author__)
__version__ = '2.2'
__url__ = 'https://github.com/gitRigge/EnterpriseBookmarksManager'
__license__ = 'MIT License (MIT)' + ', ' + __copyright__


def run_from_command_line(args):
    if args.countries:
        utils.print_countries()
        sys.exit(0)
    if args.variation:
        utils.print_variations()
        sys.exit(0)
    if args.devices:
        utils.print_devices()
        sys.exit(0)
    if args.status:
        utils.print_status()
        sys.exit(0)
    if args.license:
        utils.print_license(__license__)
        sys.exit(0)
    if args.inputfile is None:
        candidate = utils.get_most_possible_file()
        if candidate != '':
            user_input = input(
                'Do you want to continue with \'{}\' (yes/no): '.format(
                    candidate))
            if user_input.lower() == 'yes' or user_input.lower() == 'y':
                if candidate.endswith('.xlsx'):
                    filename = '{}'.format(candidate).split('.')[0]
                    output = xls2bm.convert_excel_to_csv(filename)
                else:
                    filename = '{}'.format(candidate).split('.')[0]
                    output = bm2xls.convert_csv_to_excel(filename)
            else:
                user_input = input('Enter the filename to read: ')
                if user_input.endswith('.xlsx'):
                    filename = '{}'.format(user_input).split('.')[0]
                    output = xls2bm.convert_excel_to_csv(filename)
                elif user_input.endswith('.csv'):
                    filename = '{}'.format(user_input).split('.')[0]
                    output = bm2xls.convert_csv_to_excel(filename)
                else:
                    print('Wrong file format - exit')
                    sys.exit(13)
        else:
            print('Run \'enterprise_bookmarks_manager --help\' to get help')
            sys.exit(0)
    elif args.inputfile.endswith('.xlsx'):
        filename = '{}'.format(args.inputfile).split('.')[0]
        output = xls2bm.convert_excel_to_csv(filename)
    elif args.inputfile.endswith('.csv'):
        filename = '{}'.format(args.inputfile).split('.')[0]
        output = bm2xls.convert_csv_to_excel(filename)
    print('Output file: {}'.format(output))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Manage SharePoint Enterprise Bookmarks',
        epilog='''For more help, see:
        https://github.com/gitRigge/EnterpriseBookmarksManager''')
    parser.add_argument(
        '-i', '--inputfile', action='store', type=str,
        help='Specify input file to read (Excel or CSV)')
    parser.add_argument(
        '-c', '--countries', action='store_true',
        help='Show list of ISO country codes and exit')
    parser.add_argument(
        '-v', '--variation', action='store_true',
        help='Show sample variation JSON and exit')
    parser.add_argument(
        '-d', '--devices', action='store_true',
        help='Show list of devices and exit')
    parser.add_argument(
        '-s', '--status', action='store_true',
        help='Show list of status and exit')
    parser.add_argument(
        '-l', '--license', action='store_true',
        help='Show license information and exit')
    parser.add_argument(
        '--version', action='version',
        version='version: {}'.format(__version__))
    args = parser.parse_args(argv)
    run_from_command_line(args)


if __name__ == "__main__":
    main()
