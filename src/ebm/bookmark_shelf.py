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

import uuid

try:
    import src.ebm.bookmark as bookmark
except ModuleNotFoundError:
    import bookmark


class BookmarkShelf(object):

    def __init__(self):
        self.shelf = {}
        self.keywords = []
        self.reserved_keywords = []

    def add_bookmark(self, bm: bookmark.Bookmark):
        if self.validate_keywords(bm.keywords):
            self.keywords = self.keywords + bm.keywords
        if self.validate_reserved_keywords(bm.reserved_keywords):
            self.add_reserved_keywords(bm.reserved_keywords)
        if self.validate_title_with_state(bm.title, bm.state):
            self.shelf[str(uuid.uuid4())] = bm
        else:
            raise ValidationError(
                'A bookmark with the title \'{}\' exists already'.format(
                    bm.title))

    def add_reserved_keywords(self, rkeywords: list):
        if rkeywords is not None:
            for kw in rkeywords:
                if kw in self.reserved_keywords:
                    raise ValidationError(
                        'The reserved keyword \'{}\' exists already'.format(
                            kw))
            self.reserved_keywords = self.reserved_keywords + rkeywords

    def validate_title_with_state(self, title: str, state: str):
        bms = self.get_bookmarks()
        for id in bms:
            bm = bms[id]
            mytitle = bm.title
            mystate = bm.state
            if (title == mytitle and
                    state in ['published', 'scheduled'] and state == mystate):
                return False
        return True

    def validate_reserved_keywords(self, rkeywords: list):
        if rkeywords is not None:
            for kw in rkeywords:
                if kw in self.keywords:
                    raise ValidationError(
                        'The reserved keyword \'{}\' exists in '
                        'other keywords'.format(kw))
        return True

    def validate_keywords(self, keywords: list):
        if keywords is not None:
            for kw in keywords:
                if kw in self.reserved_keywords:
                    raise ValidationError(
                        'The keyword \'{}\' exists as reserved keyword'.format(
                            kw))
        return True

    def get_bookmark(self, key: str):
        return self.shelf[key]

    def get_bookmarks(self):
        return self.shelf


class ValidationError(Exception):
    pass
