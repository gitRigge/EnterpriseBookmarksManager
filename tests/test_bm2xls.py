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

import datetime as dt

import bm2xls

END_DATE = '2022-12-29T07:30:00+00'
LAST_MODIFIED = '12/28/2022'


class TestBm2xlxDates(object):

    def test_last_modified_date(self):
        my_date = bm2xls.get_date_by_str(LAST_MODIFIED)
        print(my_date)
        assert my_date == dt.datetime(2022, 12, 28, 0, 0)

    def test_start_end_date(self):
        my_date = bm2xls.get_date_by_str(END_DATE)
        assert my_date == dt.datetime(2022, 12, 29, 7, 30)

    def test_not_date(self):
        my_date = bm2xls.get_date_by_str('test')
        assert my_date == 'test'


class TestBm2xlxFormats(object):

    def test_last_modified_format_de(self):
        my_format = bm2xls.get_date_format_by_str(LAST_MODIFIED)
        assert my_format in ['dd.mm.yyyy', 'mm/dd/yyyy']

    def test_start_end_format(self):
        my_format = bm2xls.get_date_format_by_str(END_DATE)
        assert my_format in ['dd.mm.yyyy HH:MM:SS', 'mm/dd/yyyy HH:MM:SS']

    def test_not_date_format(self):
        my_format = bm2xls.get_date_format_by_str('test')
        assert my_format == ''
