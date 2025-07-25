#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2025, Roland Rickborn (r_2@gmx.net)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ---------------------------------------------------------------------------

import pycountry


class Enums(object):

    devices = {
        'pc-windows': 'PC - Windows',
        'pc-mac': 'PC - Apple Mac',
        'mobile-ios': 'Mobile - iOS',
        'mobile-android': 'Mobile - Android'
    }

    status = {
        'published': 'Published',
        'draft': 'Draft',
        'scheduled': 'Scheduled',
        'suggested': 'Suggested',
        'excluded': 'Excluded',
        'expired': 'Expired'
    }

    countries = {}

    variations = {
        'title': '<your title>',
        'url': '<your URL>',
        'description': '<your description>',
        'country': '<your country>',
        'device': '<your device>'
    }

    def __init__(self):
        all_countries = list(pycountry.countries)
        for country in all_countries:
            self.countries[country.alpha_2.lower()] = country.name
