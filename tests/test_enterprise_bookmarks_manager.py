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

import base64
import os

import pytest
import pathlib
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

    @pytest.fixture
    def excel_file(self):
        encoded = b''
        for i in fix.TEST_XLSX_FILE_SMALL:
            encoded = encoded + i
        file_path = pathlib.Path('sample.xlsx')
        with open(file_path, 'wb') as f:
            bytes = base64.b64decode(encoded)
            f.write(bytes)
        yield str(file_path)
        file_path.unlink()

    @pytest.fixture
    def excel_file_1(self):
        encoded = b''
        for i in fix.TEST_XLSX_FILE_SMALL:
            encoded = encoded + i
        file1_path = pathlib.Path('sample1.xlsx')
        with open(file1_path, 'wb') as f:
            bytes = base64.b64decode(encoded)
            f.write(bytes)
        yield str(file1_path)
        file1_path.unlink()

    @pytest.fixture
    def excel_file_2(self):
        encoded = b''
        for i in fix.TEST_XLSX_FILE_SMALL:
            encoded = encoded + i
        file2_path = pathlib.Path('sample2.xlsx')
        with open(file2_path, 'wb') as f:
            bytes = base64.b64decode(encoded)
            f.write(bytes)
        yield str(file2_path)
        file2_path.unlink()

    @pytest.fixture
    def csv_file(self):
        file_path = pathlib.Path('sample.csv')
        f = open(file_path, 'x')
        f.close()
        yield str(file_path)
        file_path.unlink()

    @pytest.fixture
    def csv_file_1(self):
        file1_path = pathlib.Path('sample1.csv')
        f = open(file1_path, 'x')
        f.close()
        yield str(file1_path)
        file1_path.unlink()

    @pytest.fixture
    def csv_file_2(self):
        file2_path = pathlib.Path('sample2.csv')
        f = open(file2_path, 'x')
        f.close()
        yield str(file2_path)
        file2_path.unlink()

    def test_main_no_argument_fail(self, capsys):
        try:
            ebm.main([])
        except SystemExit:
            pass
        output = capsys.readouterr().out
        assert str(output).startswith(
            'Run \'enterprise_bookmarks_manager --help\' to get help')

    def test_main_no_argument_with_csv_1(self, monkeypatch, capsys, csv_file):
        csvf = csv_file
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        ebm.main([])
        i = input('Do you want to continue with \'{}\' (yes/no):'.format(csvf))
        assert i == 'y'
        output = capsys.readouterr().out
        assert output.startswith('Output file: sample.xlsx')
        os.remove('sample.xlsx')

    def test_main_no_argument_with_csv_2(
            self, monkeypatch, capsys, csv_file_1, csv_file_2):
        csvf1 = csv_file_1
        csvf2 = csv_file_2
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        monkeypatch.setattr('builtins.input', lambda _: csvf1)
        ebm.main([])
        i = input('Do you want to continue with \'{}\' (yes/no):'.format(
            csvf2))
        assert i == csvf1
        output = capsys.readouterr().out
        assert output.startswith('Output file: sample1.xlsx')
        os.remove('sample1.xlsx')

    @pytest.mark.skip()  # TODO Need to fix this test
    def test_main_no_argument_with_xlsx_1(
            self, monkeypatch, capsys, excel_file):
        xlsf = excel_file
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        ebm.main([])
        i = input('Do you want to continue with \'{}\' (yes/no):'.format(xlsf))
        assert i == 'y'
        output = capsys.readouterr().out
        assert output.startswith('Output file: sample_1.csv')

    @pytest.mark.skip()  # TODO Need to fix this test
    def test_main_no_argument_with_xlsx_2(
            self, monkeypatch, capsys, excel_file_1, excel_file_2):
        xlsf1 = excel_file_1
        xlsf2 = excel_file_2
        xlsf2
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        monkeypatch.setattr('builtins.input', lambda _: xlsf1)
        ebm.main([])
        i = input("Do you want to continue with '{}' (yes/no):".format(xlsf1))
        assert i == xlsf1
        output = capsys.readouterr().out
        assert output.startswith('Output file: sample1.csv')
        os.remove('sample1.csv')

    @pytest.mark.parametrize('arg, response', [
        ('-h', 'usage:'),
        ('--help', 'usage:'),
        ('-c', 'Allowed Country Codes are:'),
        ('--countries', 'Allowed Country Codes are:'),
        ('-v', 'Template Variation:'),
        ('--variation', 'Template Variation:'),
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
