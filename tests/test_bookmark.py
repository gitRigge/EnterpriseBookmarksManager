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

import pytest
import pytz

import bookmark


class TestBookmark(object):

    def test_basic_bookmark(self):
        my_title = 'Basic Bookmark'
        my_url = 'http://www.dummybasicurl.com'
        my_keywords = 'test'
        bm = bookmark.Bookmark(
            title = my_title,
            url = my_url,
            keywords = my_keywords
        )
        assert isinstance(bm, bookmark.Bookmark)
        assert bm.title == my_title
        assert bm.url == my_url
        assert bm.keywords == [my_keywords]

    def test_full_bookmark(self):
        test_start_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
        test_end_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) + dt.timedelta(days=1)
        last_modified = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) - dt.timedelta(days=1)
        bm = bookmark.Bookmark(
            title = 'Full Bookmark',
            url = 'http://www.dummyfullurl.com',
            keywords = 'test1;test2',
            match_similar_keywords = 'true',
            state = 'published',
            description = 'Basic Bookmark Description',
            reserved_keywords = 'rtest1;rtest2',
            categories = 'Basic Category',
            start_date = test_start_date,
            end_date = test_end_date,
            country_region = 'de;us',
            use_aad_location = 'False',
            groups = 'd0dc8935-5cfb-47ae-bb41-3b362e6fee97;d4f274a5-3f82-4165-a60d-f122a87dcdc3',
            device_and_os = 'pc-windows;pc-mac',
            targeted_variations = '[{"description":"Italian Description","country":"it"}]',
            last_modified = last_modified,
            last_modified_by = 'user123',
            id = '20a830b1-0729-4d97-9dfb-f9f7d93acccd'
        )
        assert isinstance(bm, bookmark.Bookmark)

class TestBookmarkHelpers(object):

    def test_get_instance_bookmark(self):
        bm = bookmark.Bookmark(
            title = 'Basic Bookmark',
            url = 'http://www.dummybasicurl.com',
            keywords = 'test'
        )
        bm_list = bm.to_string()
        bm_columns = bm.get_columns()
        assert len(bm_list) == len(bm_columns)

class TestBookmarkValidation(object):

    def test_missing_url_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                keywords = 'test'
            )
        assert str(e.value) == 'Bookmark.__init__() missing 1 required positional argument: \'url\''

    def test_missing_keyword_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com'
            )
        assert str(e.value) == 'Bookmark.__init__() missing 1 required positional argument: \'keywords\''

    def test_valid_match_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                match_similar_keywords = 'True'
            )
        assert str(e.value) == 'Match similar keywords value of \'Basic Bookmark\' could not be validated'

    def test_valid_state_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                state = 'Published'
            )
        assert str(e.value) == 'State of \'Basic Bookmark\' could not be validated'

    def test_reservered_keywords_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                reserved_keywords = 'test'
            )
        assert str(e.value) == 'Keywords/Reserved Keywords of \'Basic Bookmark\' could not be validated'

    def test_country_region_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                country_region = 'aa'
            )
        assert str(e.value) == 'Country/Region of \'Basic Bookmark\' could not be validated'

    def test_aad_location_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                use_aad_location = 'false'
            )
        assert str(e.value) == 'Use Azure-AD Location of \'Basic Bookmark\' could not be validated'

    def test_groups_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                groups = 'd0dc8935-5cfb-47ae-bb41-3b362e6fee9'
            )
        assert str(e.value) == 'Groups of \'Basic Bookmark\' could not be validated'

    def test_devices_and_os_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                device_and_os = 'pc'
            )
        assert str(e.value) == 'Device/OS of \'Basic Bookmark\' could not be validated'

    def test_targeted_variations_1_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                targeted_variations = '[{"description":"Italian Description","country":"aa"}]'
            )
        assert str(e.value) == 'Variation Country \'aa\' could not be validated'
    
    def test_targeted_variations_2_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                targeted_variations = '[{"test":"This node does not exist","country":"it"}]'
            )
        assert str(e.value) == 'Variations of \'Basic Bookmark\' could not be validated'

    def test_id_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                id = '20a830b1-0729-4d97-9dfb-f9f7d93accc'
            )
        assert str(e.value) == 'ID of \'Basic Bookmark\' could not be validated'

    def test_state_vs_start_date_bookmark(self):
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                state = 'scheduled',
                start_date = None
            )
        assert str(e.value) == 'State/End Date of \'Basic Bookmark\' could not be validated'

    def test_start_date_vs_end_date_bookmark(self):
        test_start_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
        test_end_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) - dt.timedelta(days=1)
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                start_date = test_start_date,
                end_date = test_end_date
            )
        assert str(e.value) == 'Start Date/End Date of \'Basic Bookmark\' could not be validated'

    def test_outdated_end_date_bookmark(self):
        test_end_date = dt.datetime.utcnow().replace(tzinfo=pytz.UTC) - dt.timedelta(days=1)
        with pytest.raises(Exception) as e:
            bm = bookmark.Bookmark(
                title = 'Basic Bookmark',
                url = 'http://www.dummyurl.com',
                keywords = 'test',
                end_date = test_end_date
            )
        assert str(e.value) == 'Start Date/End Date of \'Basic Bookmark\' could not be validated'



