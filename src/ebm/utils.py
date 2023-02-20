#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2023, Roland Rickborn (r_2@gmx.net)
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
# ---------------------------------------------------------------------------

import glob
import os
from os.path import exists

import src.ebm.enums as enums


def get_save_filename(suggested_filename: str):
    retval = ''
    filename_exists = True
    counter = 1
    _sfname = suggested_filename.split('.')[0]
    _sfext = suggested_filename.split('.')[1]
    while filename_exists:
        if not exists(suggested_filename):
            retval = suggested_filename
            filename_exists = exists(suggested_filename)
        elif not exists('{}_({}).{}'.format(_sfname, counter, _sfext)):
            retval = '{}_({}).{}'.format(_sfname, counter, _sfext)
            filename_exists = exists('{}_({}).{}'.format(
                _sfname, counter, _sfext))
        counter += 1
    return retval


def get_most_possible_file():
    retval = ''
    types = ('*.xlsx', '*.csv')
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    retval = max(files_grabbed, key=os.path.getctime)
    return retval


def print_devices():
    print('Allowed Devices are:')
    print(', '.join(list(enums.Enums().devices.values())))


def print_status():
    print('Allowed Status are:')
    print(', '.join(list(enums.Enums().status.values())))


def print_countries():
    print('Allowed Country Codes are:')
    print(', '.join(list(enums.Enums().countries.keys())))


def print_variations():
    print('Sample Variation:')
    print('[{},{{...}}]'.format(enums.Enums().variations))
