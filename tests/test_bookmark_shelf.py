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

from unittest.mock import patch

import pytest

import src.ebm.bookmark_shelf


class TestBookmarkShelfAdd(object):

    @patch('src.ebm.bookmark.Bookmark')
    def test_add_bookmark_to_shelf(self, MockBookmark):
        bm_shelf = src.ebm.bookmark_shelf.BookmarkShelf()
        bm_shelf.add_bookmark(MockBookmark)
        assert True

    @patch('src.ebm.bookmark.Bookmark')
    def test_add_identical_bookmark_to_shelf(self, MockBookmark):
        bm_shelf = src.ebm.bookmark_shelf.BookmarkShelf()
        bm = MockBookmark
        bm.title = 'Test'
        bm.state = 'published'
        bm_shelf.add_bookmark(bm)
        with pytest.raises(Exception) as e:
            bm_shelf.add_bookmark(bm)
        assert str(e.value).startswith(
            'A bookmark with the title \'Test\'')

    @patch('src.ebm.bookmark.Bookmark')
    def test_add_bookmarks_with_different_state_to_shelf(self, MockBookmark):
        bm_shelf = src.ebm.bookmark_shelf.BookmarkShelf()
        bm1 = MockBookmark
        bm1.title = 'Test1'
        bm1.state = 'published'
        bm_shelf.add_bookmark(bm1)
        bm2 = MockBookmark
        bm2.title = 'Test1'
        bm2.state = 'draft'
        bm_shelf.add_bookmark(bm2)
        assert True

    @patch('src.ebm.bookmark.Bookmark')
    def test_add_bookmark_to_shelf_with_existing_reserved_keyword(
            self, MockBookmark):
        bm_shelf = src.ebm.bookmark_shelf.BookmarkShelf()
        bm_shelf.reserved_keywords = ['test']
        bm = MockBookmark
        bm.keywords = ['test']
        with pytest.raises(Exception) as e:
            bm_shelf.add_bookmark(bm)
        assert str(e.value) == 'The keyword \'test\' exists ' \
            'as reserved keyword'

    def test_add_reserved_keywords(self):
        bm_shelf = src.ebm.bookmark_shelf.BookmarkShelf()
        bm_shelf.add_reserved_keywords(['test'])
        assert bm_shelf.reserved_keywords == ['test']

    def test_add_identical_reserved_keywords(self):
        bm_shelf = src.ebm.bookmark_shelf.BookmarkShelf()
        bm_shelf.add_reserved_keywords(['test'])
        with pytest.raises(Exception) as e:
            bm_shelf.add_reserved_keywords(['test'])
        assert str(e.value) == 'The reserved keyword \'test\' exists already'


class TestBookmarkShelfValidate(object):

    def test_validate_reserved_keywords(self):
        bm_shelf = src.ebm.bookmark_shelf.BookmarkShelf()
        bm_shelf.keywords = ['test', 'test1']
        with pytest.raises(Exception) as e:
            bm_shelf.validate_reserved_keywords(['test'])
        assert str(e.value) == 'The reserved keyword \'test\' exists ' \
            'in other keywords'
