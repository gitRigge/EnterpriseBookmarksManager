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
import locale
import pytest
import src.ebm.bm2xls as bm2xls

END_DATE = '2022-12-29T07:30:00+00'
LAST_MODIFIED = '12/28/2022'
CSV_FILE = 'Title,Url,Keywords,Match Similar Keywords,State,Description,'\
    'Reserved Keywords,Categories,Start Date,End Date,Country/Region,'\
    'Use AAD Location,Groups,Device & OS,Targeted Variations,Last Modified,'\
    'Last Modified By,Id\nTest,http://test-rr.de,test;testrr;test_rr,true,'\
    'published,Das ist nur ein Test von Roland,,,,,,False,,,,12/01/2022,'\
    'usr@test.com,dd8901da-7f6d-4c54-9251-a11a0ee48d52'


class TestBm2xlxReadInput(object):

    @pytest.fixture(scope='session')
    def input_filename(self, tmpdir_factory):
        fn = tmpdir_factory.mktemp('data').join('testfile.csv')
        f = open(fn, 'w')
        f.write(CSV_FILE)
        f.close()
        return str(fn)

    @pytest.mark.skip(reason='Need to fix this test')  # TODO
    def test_read_input(self, input_filename):
        bm2xls.read_input_file(input_filename)


class TestBm2xlxDates(object):

    def test_last_modified_date(self):
        my_date = bm2xls.get_date_by_str(LAST_MODIFIED)
        print(my_date)
        assert my_date == dt.datetime(2022, 12, 28, 0, 0)

    def test_start_end_date(self):
        my_date = bm2xls.get_date_by_str(END_DATE)
        assert my_date == dt.datetime(2022, 12, 29, 7, 30)

    def test_date_string(self):
        my_date = bm2xls.get_date_by_str('29-12-2022')
        assert my_date == '29-12-2022'

    def test_false_date_string(self):
        my_date = bm2xls.get_date_by_str('29-12-2022T07:30:00+00')
        assert my_date == '29-12-2022T07:30:00+00'


class TestBm2xlxFormats(object):

    def test_last_modified_format_de(self):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        my_format = bm2xls.get_date_format_by_str(LAST_MODIFIED)
        locale.setlocale(locale.LC_ALL, '')
        assert my_format == 'dd.mm.yyyy'

    def _last_modified_format_en(self):
        locale.setlocale(locale.LC_ALL, 'en_US')
        my_format = bm2xls.get_date_format_by_str(LAST_MODIFIED)
        locale.setlocale(locale.LC_ALL, '')
        assert my_format == 'mm/dd/yyyy'

    def test_start_end_format_de(self):
        locale.setlocale(locale.LC_ALL, 'de_AT')
        my_format = bm2xls.get_date_format_by_str(END_DATE)
        locale.setlocale(locale.LC_ALL, '')
        assert my_format == 'dd.mm.yyyy HH:MM:SS'

    def test_start_end_format_en(self):
        locale.setlocale(locale.LC_ALL, 'en_GB')
        my_format = bm2xls.get_date_format_by_str(END_DATE)
        locale.setlocale(locale.LC_ALL, '')
        assert my_format == 'mm/dd/yyyy HH:MM:SS'

    def test_not_date_format(self):
        my_format = bm2xls.get_date_format_by_str('test')
        assert my_format == ''
