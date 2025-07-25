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
# ---------------------------------------------------------------------------

import pytest

import src.ebm.xls2bm as xls2bm
import tests.ebm_fixtures as fix


@pytest.fixture(scope='session')
def output_filename(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('{}.csv'.format(fix.FILENAME))
    f = open(fn, 'w')
    f.close()
    return str(fn)


class TestXlsx2bmWriteOutput(object):

    @pytest.mark.skip()  # TODO Need to fix this test
    def test_write_init_output_file(self, output_filename):
        output = xls2bm.write_init_output_file(
            output_filename, fix.HEADER_GOOD.split(','))
        f = open(output, 'r')
        lines = f.readlines()
        assert output.endswith('.csv')
        assert lines[0].split(',')[1:-1] == fix.HEADER_GOOD.split(',')[1:-1]
        _first = lines[0].split(',')[0]
        _last = lines[0].split(',')[-1].replace('\n', '')
        assert _first.endswith(fix.HEADER_GOOD.split(',')[0])
        assert _last == fix.HEADER_GOOD.split(',')[-1]

    def test_append_to_output_file(self, output_filename):
        data = [
            fix.TITLE_GOOD,
            fix.URL_GOOD,
            fix.KEYWORDS_GOOD,
            fix.MATCH_SIMILAR_KEYWORDS_GOOD,
            fix.STATE_GOOD,
            fix.DESCRIPTION,
            fix.END_DATE,
            fix.USE_AAD_LOCATION_FALSE_GOOD,
            fix.LAST_MODIFIED,
            fix.LAST_MODIFIED_BY,
            fix.ID_GOOD
        ]
        xls2bm.append_to_output_file(output_filename, data)
        f = open(output_filename, 'r')
        lines = f.readlines()
        assert len(lines[0].split(',')) == len(data)
