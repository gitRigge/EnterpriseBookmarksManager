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
import json

import pytest
import pytz

import src.ebm.bookmark as bookmark
import tests.ebm_fixtures as fix


class TestBookmark(object):

    def test_basic_bookmark(self):
        my_title = fix.TITLE_GOOD
        my_url = fix.URL_GOOD
        my_keywords = fix.KEYWORDS
        bm = bookmark.Bookmark(
            title=my_title,
            url=my_url,
            keywords=my_keywords
        )
        assert isinstance(bm, bookmark.Bookmark)
        assert bm.title == my_title
        assert bm.url == my_url
        assert bm.keywords == my_keywords.split(';')

    def test_full_bookmark(self):
        test_start_date = fix.TEST_START_DATE
        test_end_date = fix.TEST_END_DATE
        last_modified = fix.TEST_LAST_MOD
        bm = bookmark.Bookmark(
            title=fix.TITLE_GOOD,
            url=fix.URL_GOOD,
            keywords=fix.KEYWORDS,
            match_similar_keywords=fix.MATCH_SIMILAR_KEYWORDS_GOOD,
            state=fix.STATE_GOOD,
            description=fix.DESCRIPTION,
            reserved_keywords=fix.RESERVED_KEYWORDS_GOOD,
            categories=fix.CATEGORIES,
            start_date=test_start_date,
            end_date=test_end_date,
            country_region=fix.COUNTRY_GOOD,
            use_aad_location=fix.USE_AAD_LOCATION_GOOD,
            groups=fix.GROUPS_GOOD,
            device_and_os=fix.DEVICE_AND_OS_GOOD,
            targeted_variations=fix.VARIATION_GOOD,
            last_modified=last_modified,
            last_modified_by=fix.LAST_MODIFIED_BY,
            id=fix.ID_GOOD
        )
        assert isinstance(bm, bookmark.Bookmark)


class TestBookmarkHelpers(object):

    def test_get_instance_1_bookmark(self):
        test_start_date = fix.TEST_START_DATE
        test_end_date = fix.TEST_END_DATE
        last_modified = fix.TEST_LAST_MOD
        bm = bookmark.Bookmark(
            title=fix.TITLE_GOOD,
            url=fix.URL_GOOD,
            keywords=fix.KEYWORDS,
            match_similar_keywords=fix.MATCH_SIMILAR_KEYWORDS_GOOD,
            state=fix.STATE_GOOD,
            description=fix.DESCRIPTION,
            reserved_keywords=fix.RESERVED_KEYWORDS_GOOD,
            categories=fix.CATEGORIES,
            start_date=test_start_date,
            end_date=test_end_date,
            country_region=fix.COUNTRY_GOOD,
            use_aad_location=fix.USE_AAD_LOCATION_GOOD,
            groups=fix.GROUPS_GOOD,
            device_and_os=fix.DEVICE_AND_OS_GOOD,
            targeted_variations=fix.VARIATION_GOOD,
            last_modified=last_modified,
            last_modified_by=fix.LAST_MODIFIED_BY,
            id=fix.ID_GOOD
        )
        bm_list = bm.to_string()
        bm_columns = bm.get_columns()
        assert len(bm_list) == len(bm_columns)
        assert bm_list[0] == fix.TITLE_GOOD
        assert bm_list[1] == fix.URL_GOOD
        assert bm_list[2] == fix.KEYWORDS
        assert bm_list[3] == fix.MATCH_SIMILAR_KEYWORDS_GOOD
        assert bm_list[4] == fix.STATE_GOOD
        assert bm_list[5] == fix.DESCRIPTION
        assert bm_list[6] == fix.RESERVED_KEYWORDS_GOOD
        assert bm_list[7] == fix.CATEGORIES.lower()
        assert bm_list[8] == test_start_date.strftime('%Y-%m-%dT%H:%M:%S+00')
        assert bm_list[9] == test_end_date.strftime('%Y-%m-%dT%H:%M:%S+00')
        assert bm_list[10] == fix.COUNTRY_GOOD
        assert bm_list[11] == fix.USE_AAD_LOCATION_GOOD
        assert bm_list[12] == fix.GROUPS_GOOD
        assert bm_list[13] == fix.DEVICE_AND_OS_GOOD
        assert bm_list[14] == json.loads(fix.VARIATION_GOOD.replace('""', '"'))
        assert bm_list[15] == last_modified.strftime('%m/%d/%Y')
        assert bm_list[16] == fix.LAST_MODIFIED_BY
        assert bm_list[17] == fix.ID_GOOD

    def test_get_instance_2_bookmark(self):
        bm = bookmark.Bookmark(
            title=fix.TITLE_GOOD,
            url=fix.URL_GOOD,
            keywords=fix.KEYWORDS,
            description=None,
            reserved_keywords=None,
            categories=None,
            start_date=None,
            end_date=None,
            country_region=None,
            groups=None,
            device_and_os=None,
            targeted_variations=None,
            last_modified=None,
            last_modified_by=None,
            id=None
        )
        bm_list = bm.to_string()
        assert bm_list[5] == ''
        assert bm_list[6] == ''
        assert bm_list[7] == ''
        assert bm_list[8] == ''
        assert bm_list[9] == ''
        assert bm_list[10] == ''
        assert bm_list[12] == ''
        assert bm_list[13] == ''
        assert bm_list[14] == ''
        assert bm_list[15] == ''
        assert bm_list[16] == ''
        assert bm_list[17] == ''


class TestBookmarkValidation(object):

    def test_long_title_bookmark(self):
        my_title = fix.TITLE_BAD
        my_url = fix.URL_GOOD
        my_keywords = fix.KEYWORDS
        bm = bookmark.Bookmark(
            title=my_title,
            url=my_url,
            keywords=my_keywords
        )
        assert len(bm.title) == 60

    def test_missing_url_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                keywords=fix.KEYWORDS
            )
        assert str(e.value).endswith(
            '__init__() missing 1 required positional argument: \'url\'')

    def test_missing_keyword_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD
            )
        assert str(e.value).endswith(
            '__init__() missing 1 required positional argument: \'keywords\'')

    def test_valid_match_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                match_similar_keywords=fix.MATCH_SIMILAR_KEYWORDS_BAD
            )
        assert str(e.value) == 'Match similar keywords value of \'{}' \
            '\' could not be validated'.format(fix.TITLE_GOOD)

    def test_valid_state_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                state=fix.STATE_BAD
            )
        assert str(e.value) == 'State of \'{}\' could ' \
            'not be validated'.format(fix.TITLE_GOOD)

    def test_reservered_keywords_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                reserved_keywords=fix.RESERVED_KEYWORDS_BAD
            )
        assert str(e.value) == 'Keywords/Reserved Keywords of \'{}' \
            '\' could not be validated'.format(fix.TITLE_GOOD)

    def test_country_region_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                country_region=fix.COUNTRY_BAD
            )
        assert str(e.value) == 'Country/Region of \'{}\' could '\
            'not be validated'.format(fix.TITLE_GOOD)

    def test_aad_location_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                use_aad_location=fix.USE_AAD_LOCATION_BAD
            )
        assert str(e.value) == 'Use AAD Location of \'{}\' could '\
            'not be validated'.format(fix.TITLE_GOOD)

    def test_groups_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                groups=fix.GROUPS_BAD
            )
        assert str(e.value) == 'Groups of \'{}\' could ' \
            'not be validated'.format(fix.TITLE_GOOD)

    def test_devices_and_os_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                device_and_os=fix.DEVICE_AND_OS_BAD
            )
        assert str(e.value) == 'Device/OS of \'{}\' could ' \
            'not be validated'.format(fix.TITLE_GOOD)

    def test_url_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_BAD,
                keywords=fix.KEYWORDS
            )
        assert str(e.value) == 'URL of \'{}\' could ' \
            'not be validated'.format(fix.TITLE_GOOD)

    @pytest.mark.parametrize('variation, response', [
        (fix.VARIATION_BAD_1, 'Variation Country \'{}\''.format(
            fix.COUNTRY_BAD)),
        (fix.VARIATION_BAD_2, 'Variations of \'{}\''.format(fix.TITLE_GOOD)),
        (fix.VARIATION_BAD_3, 'Variation Title'),
        (fix.VARIATION_BAD_4, 'Variation URL'),
        (fix.VARIATION_BAD_5, 'Variation Device')])
    def test_targeted_variations_bookmark(self, variation, response):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                targeted_variations=variation
            )
        assert str(e.value).startswith(response)

    def test_id_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                id=fix.ID_BAD
            )
        assert str(e.value) == 'ID of \'{}\' could ' \
            'not be validated'.format(fix.TITLE_GOOD)

    def test_state_vs_start_date_bookmark(self):
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                state='scheduled',
                start_date=None
            )
        assert str(e.value) == 'State/End Date of \'{}\' could ' \
            'not be validated'.format(fix.TITLE_GOOD)

    def test_start_date_vs_end_date_bookmark(self):
        test_start_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
        test_end_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) - \
            dt.timedelta(days=1)
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                start_date=test_start_date,
                end_date=test_end_date
            )
        assert str(e.value) == 'Start Date/End Date of \'{}' \
            '\' could not be validated'.format(fix.TITLE_GOOD)

    def test_outdated_end_date_bookmark(self):
        test_end_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) - \
            dt.timedelta(days=1)
        with pytest.raises(Exception) as e:
            bookmark.Bookmark(
                title=fix.TITLE_GOOD,
                url=fix.URL_GOOD,
                keywords=fix.KEYWORDS,
                end_date=test_end_date
            )
        assert str(e.value) == 'Start Date/End Date of \'{}' \
            '\' could not be validated'.format(fix.TITLE_GOOD)
