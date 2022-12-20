#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
# 
# Copyright (c) 2022, Roland Rickborn (r_2@gmx.net)
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
#
# ---------------------------------------------------------------------------

import argparse
import sys

import bm2xls
import utils
import xls2bm

__author__ = 'Roland Rickborn'
__copyright__ = 'Copyright (c) 2022 {}'.format(__author__)
__version__ = '1.0'
__url__ = 'https://github.com/gitRigge/EnterpriseBookmarksManager'
__license__ = 'MIT License (MIT)'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( 'inputfile', nargs='?', action = 'store', type = str,
        help = 'Specify input file to read (Excel or CSV)' )
    args = parser.parse_args()
    if args.inputfile == None:
        candidate = utils.get_most_possible_file()
        user_input = input('Do you want to continue with \'{}\' (yes/no): '.format(candidate))
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
            else:
                filename = '{}'.format(user_input).split('.')[0]
                output = bm2xls.convert_csv_to_excel(filename)
    elif args.inputfile.endswith('.xlsx'):
        filename = '{}'.format(args.inputfile).split('.')[0]
        output = xls2bm.convert_excel_to_csv(filename)
    elif args.inputfile.endswith('.csv'):
        filename = '{}'.format(args.inputfile).split('.')[0]
        output = bm2xls.convert_csv_to_excel(filename)
    sys.exit()
