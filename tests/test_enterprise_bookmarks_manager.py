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

import os
from unittest.mock import patch

import pytest

import src.ebm.enterprise_bookmarks_manager as ebm
import tests.ebm_fixtures as fix


@pytest.fixture(scope='session')
def input_csv_filename(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('{}.csv'.format(fix.FILENAME))
    f = open(fn, 'w')
    f.write(fix.CSV_FILE_GOOD)
    f.close()
    return str(fn)


class TestEbmMain(object):

    def test_main_no_argument_fail(self, capsys):
        try:
            ebm.main([])
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith(
            'Run \'enterprise_bookmarks_manager --help\' to get help')

    def test_main_no_argument_with_csv(self, monkeypatch, capsys):
        f = open('sample.csv', 'x')
        f.close()
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        try:
            ebm.main([])
            i = input('Do you want to continue with \'sample.csv\' (yes/no):')
            assert i == 'y'
            output = capsys.readouterr().out
            assert output.startswith('Output file: sample.xlsx')
        finally:
            if os.path.exists('sample.csv'):
                os.remove('sample.csv')
            if os.path.exists('sample.xlsx'):
                os.remove('sample.xlsx')

    @pytest.mark.parametrize('arg, response', [
        ('-h', 'usage:'),
        ('--help', 'usage:'),
        ('-c', 'Allowed Country Codes are:'),
        ('--countries', 'Allowed Country Codes are:'),
        ('-v', 'Sample Variation:'),
        ('--variation', 'Sample Variation:'),
        ('-d', 'Allowed Devices are:'),
        ('--devices', 'Allowed Devices are:'),
        ('-s', 'Allowed Status are:'),
        ('--status', 'Allowed Status are:'),
        ('--version', 'version:')
        ])
    def test_main_optional_arguments(self, capsys, arg, response):
        try:
            ebm.main([arg])
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith(response)

    @pytest.mark.parametrize('arg', [
        ('-i {}.csv'.format(fix.FILENAME)),
        ('-i {}.xlsx'.format(fix.FILENAME))
        ])
    def test_main_input_file_fail(self, capsys, arg):
        try:
            ebm.main([arg])
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith('[Errno 2] No such file or directory')

    @patch('src.ebm.bm2xls')
    @pytest.mark.skip()
    def test_main_input_file_ok(self, bm2xls_mock, input_csv_filename, capsys):
        ebm.main(['-i {}'.format(input_csv_filename)])
        output = capsys.readouterr().out
        assert str(output).startswith('[Errno 2] No such file or directory')


class TestEbmHelpers(object):

    @patch('sys.argv')
    @pytest.mark.parametrize('arg', [
        ('sample.csv'),
        ('sample.xlsx')
        ])
    @pytest.mark.skip()
    def test_run_from_command_line_1(self, argv_mock, arg, capsys):
        argv_mock.inputfile = arg
        argv_mock.countries = False
        argv_mock.variation = False
        argv_mock.devices = False
        argv_mock.status = False
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
