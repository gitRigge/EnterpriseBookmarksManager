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

import bookmark_shelf


class TestBookmarkShelfAdd(object):

    @patch('bookmark.Bookmark')
    def test_add_bookmark_to_shelf(self, MockBookmark):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm_shelf.add_bookmark(MockBookmark)
        assert True

    @patch('bookmark.Bookmark')
    def test_add_identical_bookmark_to_shelf(self, MockBookmark):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm_shelf.add_bookmark(MockBookmark)
        with pytest.raises(Exception) as e:
            bm_shelf.add_bookmark(MockBookmark)
        assert str(e.value).startswith('A bookmark with the title \'<MagicMock name=\'Bookmark.title\'')
    
    @patch('bookmark.Bookmark')
    def test_add_bookmark_to_shelf_with_existing_reserved_keyword(self, MockBookmark):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm_shelf.reserved_keywords = ['test']
        bm = MockBookmark
        bm.keywords = ['test']
        with pytest.raises(Exception) as e:
            bm_shelf.add_bookmark(bm)
        assert str(e.value) == 'The keyword \'test\' exists as reserved keyword'

    def test_add_reserved_keywords(self):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm_shelf.add_reserved_keywords(['test'])
        assert bm_shelf.reserved_keywords == ['test']
    
    def test_add_identical_reserved_keywords(self):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm_shelf.add_reserved_keywords(['test'])
        with pytest.raises(Exception) as e:
            bm_shelf.add_reserved_keywords(['test'])
        assert str(e.value) == 'The reserved keyword \'test\' exists already'


class TestBookmarkShelfGet(object):

    def test_get_no_bookmark_from_shelf(self):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        with pytest.raises(Exception) as e:
            bm_shelf.get_bookmark('Test')
        assert str(e.value) == '"There is no title \'Test\' in the shelf"'

    @patch('bookmark.Bookmark')
    def test_get_bookmark_from_shelf(self, MockBookmark):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm = MockBookmark
        title = bm.title
        bm_shelf.add_bookmark(bm)
        bm = bm_shelf.get_bookmark(title)
        assert True

    @patch('bookmark.Bookmark')
    def test_get_bookmarks_from_shelf(self, MockBookmark):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm1 = MockBookmark
        bm1.title = 'Test1'
        bm_shelf.add_bookmark(bm1)
        bm2 = MockBookmark
        bm2.title = 'Test2'
        bm_shelf.add_bookmark(bm2)
        bms = bm_shelf.get_bookmarks()
        assert len(bms) == 2

class TestBookmarkShelfValidate(object):

    def test_validate_reserved_keywords(self):
        bm_shelf = bookmark_shelf.BookmarkShelf()
        bm_shelf.keywords = ['test', 'test1']
        with pytest.raises(Exception) as e:
            bm_shelf.validate_reserved_keywords(['test'])
        assert str(e.value) == 'The reserved keyword \'test\' exists in other keywords'