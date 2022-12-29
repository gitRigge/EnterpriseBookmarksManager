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

import utils
import time


class TestFilenameSuggestion(object):

    def test_suggested_filename_xlsx(self):
        filename = 'test.xlsx'
        file = open(filename, 'w')
        file.write('Test')
        file.close()
        new_filename = utils.get_save_filename(filename)
        assert new_filename == 'test_(1).xlsx'
        os.remove(filename)

    def test_suggested_filename_csv(self):
        filename = 'test.csv'
        file = open(filename, 'w')
        file.write('Test')
        file.close()
        new_filename = utils.get_save_filename(filename)
        assert new_filename == 'test_(1).csv'
        os.remove(filename)


class TestMostPossibleFile(object):

    def test_most_possible_file_xlsx(self):
        to_be_deleted = []
        for i in range(1, 4):
            filename = 'test{}.xlsx'.format(i)
            file = open(filename, 'w')
            file.write('Test')
            file.close()
            to_be_deleted.append(filename)
            time.sleep(0.1)  # to diff creation timestamps
        most_possible_file = utils.get_most_possible_file()
        assert most_possible_file == 'test3.xlsx'
        for filename in to_be_deleted:
            os.remove(filename)

    def test_most_possible_file_csv(self):
        to_be_deleted = []
        for i in range(1, 4):
            filename = 'test{}.csv'.format(i)
            file = open(filename, 'w')
            file.write('Test')
            file.close()
            to_be_deleted.append(filename)
            time.sleep(0.1)  # to diff creation timestamps
        most_possible_file = utils.get_most_possible_file()
        assert most_possible_file == 'test3.csv'
        for filename in to_be_deleted:
            os.remove(filename)
