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

import datetime
import json

import pytz
import validators

try:
    import src.ebm.enums as enums
except ModuleNotFoundError:
    import enums


class Bookmark(object):

    def __init__(self, title: str, url: str, keywords: str, **kwargs):

        # Class variables with default values
        self.title = ''
        self.url = ''
        self.keywords = []
        self.match_similar_keywords = True
        self.state = None
        self.description = None
        self.reserved_keywords = None
        self.categories = None
        self.start_date = None
        self.end_date = None
        self.country_region = None
        self.use_aad_location = False
        self.groups = None
        self.device_and_os = None
        self.targeted_variations = None
        self.last_modified = None
        self.last_modified_by = None
        self.id = None

        if self.validate_title(title):
            self.title = title
        else:
            self.title = '{}...'.format(title[:57])
            print('Title has been shortened to \'{}\''.format(self.title))

        if self.validate_url(url):
            self.url = url
        else:
            raise ValidationError(
                'URL of \'{}\' could not be validated'.format(self.title))

        if self.validate_keywords(
                self.remove_duplicates(self.get_serialized_values(keywords))):
            self.keywords = self.remove_duplicates(
                self.get_serialized_values(keywords))
        else:
            raise ValidationError(
                'Keywords of \'{}\' could not be validated'.format(self.title))

        if 'match_similar_keywords' in kwargs:
            if kwargs['match_similar_keywords'] is not None:
                if self.valid_match_sim_kw(kwargs['match_similar_keywords']):
                    self.match_similar_keywords = self.get_boolean(
                        kwargs['match_similar_keywords'])
                else:
                    raise ValidationError(
                        'Match similar keywords value of \'{}\' '
                        'could not be validated'.format(self.title))

        if 'state' in kwargs:
            if self.validate_state(kwargs['state']):
                self.state = kwargs['state']
            else:
                raise ValidationError(
                    'State of \'{}\' could not be validated'.format(
                        self.title))

        if 'description' in kwargs:
            if kwargs['description'] is not None:
                if self.validate_description(kwargs['description']):
                    self.description = kwargs['description']
                else:
                    self.description = '{}...'.format(
                        kwargs['description'][:297])
                    print('Description has been shortened to \'{}\''.format(
                        self.description))

        if 'reserved_keywords' in kwargs:
            self.reserved_keywords = self.remove_duplicates(
                self.get_serialized_values(kwargs['reserved_keywords']))

        if 'categories' in kwargs:
            self.categories = self.remove_duplicates(
                self.get_serialized_values(kwargs['categories']))

        if 'start_date' in kwargs:
            if self.validate_date(kwargs['start_date']):
                self.start_date = kwargs['start_date']
            else:
                raise ValidationError(
                    'Start Date of \'{}\' could not be validated'.format(
                        self.title))

        if 'end_date' in kwargs:
            if self.validate_date(kwargs['end_date']):
                self.end_date = kwargs['end_date']
            else:
                raise ValidationError(
                    'End Date of \'{}\' could not be validated'.format(
                        self.title))

        if 'country_region' in kwargs:
            if self.validate_country_region(
                    self.get_serialized_values(kwargs['country_region'])):
                self.country_region = self.get_serialized_values(
                    kwargs['country_region'])
            else:
                raise ValidationError(
                    'Country/Region of \'{}\' could not be validated'.format(
                        self.title))

        if 'use_aad_location' in kwargs:
            if kwargs['use_aad_location'] is not None:
                if self.validate_use_aad_location(kwargs['use_aad_location']):
                    self.use_aad_location = self.get_boolean(
                        kwargs['use_aad_location'])
                else:
                    raise ValidationError(
                        'Use AAD Location of \'{}\' '
                        'could not be validated'.format(self.title))

        if 'groups' in kwargs:
            if self.validate_groups(self.get_serialized_values(
                    kwargs['groups'])):
                self.groups = self.get_serialized_values(kwargs['groups'])
            else:
                raise ValidationError(
                    'Groups of \'{}\' could not be validated'.format(
                        self.title))

        if 'device_and_os' in kwargs:
            if self.validate_device_and_os(self.get_serialized_values(
                    kwargs['device_and_os'])):
                self.device_and_os = self.get_serialized_values(
                    kwargs['device_and_os'])
            else:
                raise ValidationError(
                    'Device/OS of \'{}\' could not be validated'.format(
                        self.title))

        if 'targeted_variations' in kwargs:
            if self.validate_targeted_variations(
                    kwargs['targeted_variations']):
                self.targeted_variations = self.get_serialized_variations(
                    kwargs['targeted_variations'])
            else:
                raise ValidationError(
                    'Variations of \'{}\' could not be validated'.format(
                        self.title))

        if 'last_modified' in kwargs:
            if self.validate_date(kwargs['last_modified']):
                self.last_modified = kwargs['last_modified']
            else:
                raise ValidationError(
                    'Last Modified Date of \'{}\' could '
                    'not be validated'.format(self.title))

        if 'last_modified_by' in kwargs:
            self.last_modified_by = kwargs['last_modified_by']

        if 'id' in kwargs:
            if self.validate_id(kwargs['id']):
                self.id = kwargs['id']
            else:
                raise ValidationError(
                    'ID of \'{}\' could not be validated'.format(self.title))

        if not self.validate_start_end_dates(self.start_date, self.end_date):
            raise ValidationError(
                'Start Date/End Date of \'{}\' could not be validated'.format(
                    self.title))

        if not self.validate_state_and_dates(self.state, self.start_date):
            raise ValidationError(
                'State/End Date of \'{}\' could '
                'not be validated'.format(self.title))

        if not self.validate_keywords_and_reserved_keywords(
                self.keywords, self.reserved_keywords):
            raise ValidationError(
                'Keywords/Reserved Keywords of \'{}\' could '
                'not be validated'.format(self.title))

    def to_string(self):
        if self.match_similar_keywords:
            match_similar_keywords = 'true'
        if self.description is None:
            description = ''
        else:
            description = self.description
        if self.reserved_keywords is None:
            reserved_keywords = ''
        else:
            reserved_keywords = ';'.join(self.reserved_keywords)
        if self.categories is None:
            categories = ''
        else:
            categories = ';'.join(self.categories)
        if self.start_date is None:
            start_date = ''
        else:
            start_date = self.start_date.strftime('%Y-%m-%dT%H:%M:%S+00')
        if self.end_date is None:
            end_date = ''
        else:
            end_date = self.end_date.strftime('%Y-%m-%dT%H:%M:%S+00')
        if self.country_region is None:
            country_region = ''
        else:
            country_region = ';'.join(self.country_region)
        if self.use_aad_location:
            use_aad_location = 'True'
        else:
            use_aad_location = 'False'
        if self.groups is None:
            groups = ''
        else:
            groups = ';'.join(self.groups)
        if self.device_and_os is None:
            device_and_os = ''
        else:
            device_and_os = ';'.join(self.device_and_os)
        if self.targeted_variations is None:
            targeted_variations = ''
        else:
            targeted_variations = self.targeted_variations
        if self.last_modified is None:
            last_modified = ''
        else:
            last_modified = self.last_modified.strftime('%m/%d/%Y')
        if self.last_modified_by is None:
            last_modified_by = ''
        else:
            last_modified_by = self.last_modified_by
        if self.id is None:
            id = ''
        else:
            id = self.id
        retval = [
            self.title,
            self.url,
            ';'.join(self.keywords),
            match_similar_keywords,
            self.state,
            description,
            reserved_keywords,
            categories,
            start_date,
            end_date,
            country_region,
            use_aad_location,
            groups,
            device_and_os,
            targeted_variations,
            last_modified,
            last_modified_by,
            id
        ]
        return retval

    @classmethod
    def get_serialized_values(cls, strvalues):
        if strvalues is not None:
            return strvalues.split(';')
        else:
            return None

    @classmethod
    def get_serialized_variations(cls, variations):
        if variations is not None:
            return json.loads(variations.replace('""', '"'))
        else:
            return None

    @classmethod
    def get_boolean(cls, value: str):
        if value in ['true', 'True', '1']:
            return True
        else:
            return False

    @classmethod
    def remove_duplicates(cls, keywords):
        unique_keywords = None
        if keywords is not None:
            unique_keywords = []
            for kw in keywords:
                if not kw.lower() in unique_keywords:
                    unique_keywords.append(kw.lower())
        return unique_keywords

    @classmethod
    def validate_title(cls, title):
        if title is not None and len(title) > 0 and len(title) < 60:
            return True
        return False

    @classmethod
    def validate_url(cls, url):
        if url is not None and validators.url(url):
            return True
        return False

    @classmethod
    def validate_keywords(cls, keywords: list):
        if len(keywords) == 0:
            return False
        for kw in keywords:
            if len(kw) == 0 or kw == ';':
                return False
        return True

    @classmethod
    def valid_match_sim_kw(cls, msk: str):
        if msk in ['true', 'false']:
            return True
        return False

    @classmethod
    def validate_state(cls, state: str):
        if state in enums.Enums().status:
            return True
        return False

    @classmethod
    def validate_description(cls, description: str):
        if len(description) < 300:
            return True
        return False

    @classmethod
    def validate_date(cls, date):
        if isinstance(date, datetime.date) or date is None:
            return True
        return False

    @classmethod
    def validate_country_region(cls, country_region):
        if country_region is not None:
            for region in country_region:
                if region not in enums.Enums().countries:
                    return False
        return True

    @classmethod
    def validate_use_aad_location(cls, uad: str):
        if uad in ['True', 'False']:
            return True
        return False

    @classmethod
    def validate_groups(cls, groups):
        if groups is not None:
            for group in groups:
                if not validators.uuid(group):
                    return False
        return True

    @classmethod
    def validate_device_and_os(cls, device_and_os):
        if device_and_os is not None:
            for spec in device_and_os:
                if spec not in enums.Enums().devices:
                    return False
        return True

    @classmethod
    def validate_targeted_variations(cls, tv):
        if tv is not None:
            _tv_json = json.loads(tv)
            for i in range(len(_tv_json)):
                for key in list(_tv_json[i].keys()):
                    if key not in enums.Enums().variations:
                        return False
                    if key == 'title':
                        if not cls.validate_title(_tv_json[i][key]):
                            raise ValidationError(
                                'Variation Title \'{}\' could not be '
                                'validated'.format(_tv_json[i][key]))
                    if key == 'url':
                        if not cls.validate_url(_tv_json[i][key]):
                            raise ValidationError(
                                'Variation URL \'{}\' could not be '
                                'validated'.format(_tv_json[i][key]))
                    if key == 'description':
                        if not cls.validate_description(_tv_json[i][key]):
                            raise ValidationError(
                                'Variation Description \'{}\' could not be '
                                'validated'.format(_tv_json[i][key]))
                    if key == 'country':
                        if not cls.validate_country_region(
                                cls.get_serialized_values(_tv_json[i][key])):
                            raise ValidationError(
                                'Variation Country \'{}\' could not be '
                                'validated'.format(_tv_json[i][key]))
                    if key == 'device':
                        if not cls.validate_device_and_os(
                                cls.get_serialized_values(_tv_json[i][key])):
                            raise ValidationError(
                                'Variation Device \'{}\' could not be '
                                'validated'.format(_tv_json[i][key]))
            return True
        else:
            return True

    @classmethod
    def validate_id(cls, id):
        if id is not None:
            if not validators.uuid(id):
                return False
        return True

    @classmethod
    def validate_start_end_dates(cls, sdate, edate):
        if isinstance(edate, datetime.date):
            if edate < datetime.datetime.utcnow().replace(tzinfo=pytz.UTC):
                return False
        if isinstance(sdate, datetime.date) and isinstance(
                edate, datetime.date):
            if edate < sdate:
                return False
        return True

    @classmethod
    def validate_state_and_dates(cls, state, sdate):
        if state == 'scheduled' and not isinstance(sdate, datetime.date):
            return False
        return True

    @classmethod
    def validate_keywords_and_reserved_keywords(cls, keywords, rkeywords):
        if rkeywords is not None:
            for kw in rkeywords:
                if kw in keywords:
                    return False  # TODO: Need to validate this!
            for kw in keywords:
                if kw in rkeywords:
                    return False
        return True

    @classmethod
    def get_columns(cls):
        return {
            'A': 'Title',
            'B': 'Url',
            'C': 'Keywords',
            'D': 'Match Similar Keywords',
            'E': 'State',
            'F': 'Description',
            'G': 'Reserved Keywords',
            'H': 'Categories',
            'I': 'Start Date',
            'J': 'End Date',
            'K': 'Country/Region',
            'L': 'Use AAD Location',
            'M': 'Groups',
            'N': 'Device & OS',
            'O': 'Targeted Variations',
            'P': 'Last Modified',
            'Q': 'Last Modified By',
            'R': 'Id'
        }


class ValidationError(Exception):
    pass
