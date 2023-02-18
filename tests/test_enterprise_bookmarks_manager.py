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

from unittest.mock import patch

import pytest

import src.ebm.enterprise_bookmarks_manager as ebm
import tests.ebm_fixtures as fix


@pytest.fixture(scope='session')
def input_filename(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('{}.csv'.format(fix.FILENAME))
    f = open(fn, 'w')
    f.write(fix.CSV_FILE_GOOD)
    f.close()
    return str(fn)


class TestEbmMain(object):

    @pytest.mark.skip()  # TODO Need to fix this test
    def test_main_1(self, capsys):
        try:
            ebm.main([])
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith('usage: pytest [-h]')

    @pytest.mark.parametrize('arg', ('-h', '--help'))
    @pytest.mark.skip()  # TODO Need to fix this test
    def test_main_2(self, capsys, arg):
        try:
            ebm.main([arg])
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith('usage: pytest.EXE [-h]')

    @pytest.mark.parametrize('file', ('sample.csv', 'sample.xlsx'))
    def test_main_3(self, capsys, file):
        try:
            ebm.main([file])
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith('[Errno 2] No such file or directory')

    @patch('sys.argv')
    @pytest.mark.parametrize('inputfile', ('sample.csv', 'sample.xlsx'))
    def test_run_from_command_line_1(self, argv_mock, inputfile, capsys):
        argv_mock.inputfile = inputfile
        try:
            ebm.run_from_command_line(argv_mock)
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith('[Errno 2] No such file or directory')

    # @patch('sys.argv')
    # @patch('src.ebm.enterprise_bookmarks_manager.input')
    # @patch('src.ebm.utils.get_most_possible_file')
    # @pytest.mark.parametrize('input', (
    #   ['yes', 'sample.csv'], ['yes', 'sample.xlsx'], ['yes', 'sample.txt']))
    # @pytest.mark.skip()  # TODO Need to fix this test
    # def test_run_from_command_line_2(self, argv_mock, i_mock, c_mock,
    #   input, capsys):
    #     i_mock = input[0]
    #     c_mock = input[1]
    #     argv_mock.inputfile = None
    #     try:
    #         ebm.run_from_command_line(argv_mock)
    #     except OSError:
    #         pass
    #     output = capsys.readouterr().out
    #     assert str(output).startswith('[Errno 2] No such file or directory')
