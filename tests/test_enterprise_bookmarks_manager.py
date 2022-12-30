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
# Revision history:
# 2022-12-20  Created
#
# ---------------------------------------------------------------------------

import argparse
import datetime as dt
import os
from unittest.mock import patch

import pytz

import src.ebm.enterprise_bookmarks_manager as ebm

TEST_START_DATE = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
TEST_END_DATE = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) + dt.timedelta(
    days=1)
LAST_MODIFIED = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) - dt.timedelta(
    days=1)
VARIATION = '[{"description":"Italian Description","country":"it"}]'
BM_FIXTURE = "{}Title,Url,Keywords,Match Similar Keywords,State,Description," \
    "Reserved Keywords,Categories,Start Date,End Date,Country/Region," \
    "Use AAD Location,Groups,Device & OS,Targeted Variations,Last Modified," \
    "Last Modified By,Id\n" \
    "Full Bookmark,http://www.dummyfullurl.com,test1;test2," \
    "true,published,Basic Bookmark Description,rtest1;rtest2,Basic Category," \
    "{},{},de;us,False,d0dc8935-5cfb-47ae-bb41-3b362e6fee97;" \
    "d4f274a5-3f82-4165-a60d-f122a87dcdc3,pc-windows;pc-mac,{},{}," \
    "user123,20a830b1-0729-4d97-9dfb-f9f7d93acccd".format(
        u'\uFEFF',
        TEST_START_DATE.strftime('%Y-%m-%dT%H:%M:%S+00'),
        TEST_END_DATE.strftime('%Y-%m-%dT%H:%M:%S+00'),
        VARIATION,
        LAST_MODIFIED.strftime('%m/%d/%Y')
    )


@patch('bookmark.Bookmark')
def _import_csv_cli(monkeypatch):  # TODO Not yet working...
    file = open('test.csv', 'w', encoding='utf-8')
    file.write(BM_FIXTURE)
    file.close()
    parser = argparse.ArgumentParser()
    parser.inputfile = 'test.csv'
    ebm.run_from_command_line(parser)
    os.remove('test.csv')
