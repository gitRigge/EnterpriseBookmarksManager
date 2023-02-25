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

import pytz

FILENAME = 'testfile'

HEADER_GOOD = 'Title,Url,Keywords,Match Similar Keywords,'\
    'State,Description,Reserved Keywords,Categories,'\
    'Start Date,End Date,Country/Region,Use AAD Location,'\
    'Groups,Device & OS,Targeted Variations,Last Modified,'\
    'Last Modified By,Id'
HEADER_BAD = 'Title,Url,Keywords,Match Similar Keywords,'\
    'State,Description,Reserved Keywords,Categories,'\
    'Start Date,End Date,Country/Region,Use AAD Location,'\
    'Groups,Device & OS,Targeted Variations,Last Modified,Id'

TITLE_GOOD = 'Test'
TITLE_BAD = 'Test Lorem ipsum dolor sit amet, consetetur sadipscing elitr'
URL_GOOD = 'http://test-rr.de'
URL_BAD = 'www.test-rr.de'
KEYWORDS_GOOD = 'test;testrr;test_rr'
KEYWORDS_BAD = 'test;testrr;test_rr;rtest1'
MATCH_SIMILAR_KEYWORDS_GOOD = 'true'
MATCH_SIMILAR_KEYWORDS_BAD = 'True'
STATE_GOOD = 'published'
STATE_BAD = 'Published'
DESCRIPTION = 'Das ist nur ein Test von Roland'
DESCRIPTION_BAD = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr,'\
    'sed diam nonumy eirmod tempor invidunt ut labore et dolore magna'\
    'aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo'\
    'dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus'\
    'est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur'\
    'sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et'\
    'dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam'\
    'et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea'\
    'takimata sanctus est Lorem ipsum dolor sit amet.'
RESERVED_KEYWORDS_GOOD = 'rtest1;rtest2'
RESERVED_KEYWORDS_BAD = 'testrr'
CATEGORIES = 'Basic Category'
START_DATE = '2022-12-01T07:30:00+00'
START_DATE_BAD = 'Lorem ipsum'
END_DATE = '2022-12-29T07:30:00+00'
END_DATE_BAD = 'Lorem ipsum'
COUNTRY_GOOD = 'de;us'
COUNTRY_BAD = 'aa'
USE_AAD_LOCATION_FALSE_GOOD = 'False'
USE_AAD_LOCATION_FALSE_BAD = 'false'
USE_AAD_LOCATION_TRUE_GOOD = 'True'
USE_AAD_LOCATION_TRUE_BAD = 'true'
GROUPS_GOOD = 'd0dc8935-5cfb-47ae-bb41-3b362e6fee97;'\
    'd4f274a5-3f82-4165-a60d-f122a87dcdc3'
GROUPS_BAD = 'd0dc8935-5cfb-47ae-bb41-3b362e6fee9'
DEVICE_AND_OS_GOOD = 'pc-windows;pc-mac'
DEVICE_AND_OS_BAD = 'pc'

VAR_COUNTRY = 'it'
VARIATION_GOOD = '[{{"title":"{}","description":"{}","url":"{}",'\
    '"device":"{}","country":"{}"}}]'.format(
        TITLE_GOOD, DESCRIPTION, URL_GOOD, DEVICE_AND_OS_GOOD, VAR_COUNTRY)
VARIATION_BAD_1 = '[{{"title":"{}","description":"{}","url":"{}",'\
    '"device":"{}","country":"{}"}}]'.format(
        TITLE_GOOD, DESCRIPTION, URL_GOOD, DEVICE_AND_OS_GOOD, COUNTRY_BAD)
VARIATION_BAD_2 = '[{{"test":"{}","description":"{}","url":"{}",'\
    '"device":"{}","country":"{}"}}]'.format(
        TITLE_GOOD, DESCRIPTION, URL_GOOD, DEVICE_AND_OS_GOOD, VAR_COUNTRY)
VARIATION_BAD_3 = '[{{"title":"{}","description":"{}","url":"{}",'\
    '"device":"{}","country":"{}"}}]'.format(
        TITLE_BAD, DESCRIPTION, URL_GOOD, DEVICE_AND_OS_GOOD, VAR_COUNTRY)
VARIATION_BAD_4 = '[{{"title":"{}","description":"{}","url":"{}",'\
    '"device":"{}","country":"{}"}}]'.format(
        TITLE_GOOD, DESCRIPTION, URL_BAD, DEVICE_AND_OS_GOOD, VAR_COUNTRY)
VARIATION_BAD_5 = '[{{"title":"{}","description":"{}","url":"{}",'\
    '"device":"{}","country":"{}"}}]'.format(
        TITLE_GOOD, DESCRIPTION, URL_GOOD, DEVICE_AND_OS_BAD, VAR_COUNTRY)
VARIATION_BAD_6 = '[{{"title":"{}","description":"{}","url":"{}",'\
    '"device":"{}","country":"{}"}}]'.format(
        TITLE_GOOD, DESCRIPTION_BAD, URL_GOOD, DEVICE_AND_OS_GOOD, VAR_COUNTRY)

LAST_MODIFIED = '12/28/2022'
LAST_MODIFIED_BAD_1 = '12/12/2022'
LAST_MODIFIED_BAD_2 = 'Lorem ipsum'
LAST_MODIFIED_BY = 'usr@test.com'
ID_GOOD = 'dd8901da-7f6d-4c54-9251-a11a0ee48d52'
ID_BAD = '20a830b1-0729-4d97-9dfb-f9f7d93accc'

CSV_FILE_GOOD = '{}\n{},{},{},{},{},{},,,,{},,{},,,,{},{},{}'.format(
        HEADER_GOOD,
        TITLE_GOOD,
        URL_GOOD,
        KEYWORDS_GOOD,
        MATCH_SIMILAR_KEYWORDS_GOOD,
        STATE_GOOD,
        DESCRIPTION,
        END_DATE,
        USE_AAD_LOCATION_FALSE_GOOD,
        LAST_MODIFIED,
        LAST_MODIFIED_BY,
        ID_GOOD
    )
CSV_FILE_BAD = '{}\n{},{},{},{},{},{},,,,{},,{},,,,{},{},{}'.format(
        HEADER_GOOD,
        TITLE_BAD,
        URL_GOOD,
        KEYWORDS_GOOD,
        MATCH_SIMILAR_KEYWORDS_GOOD,
        STATE_GOOD,
        DESCRIPTION,
        END_DATE,
        USE_AAD_LOCATION_FALSE_GOOD,
        LAST_MODIFIED,
        LAST_MODIFIED_BY,
        ID_GOOD
    )

TEST_START_DATE = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
TEST_END_DATE = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) + dt.timedelta(
    days=1)
TEST_LAST_MOD = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) - dt.timedelta(
    days=1)
