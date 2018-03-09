#!/usr/bin/env python
# coding: utf-8


import re
from . import WaffleError


# Errors ######################################################################
###############################################################################
class RouteError(WaffleError):
    pass


class BaseFilter:
    def __init__(self, name):
        self.name = name


class RegexFilter(BaseFilter):
    def __init__(self, regexp, *args,  **kwargs):
        self.regexp = regexp
        super(RegexFilter, self).__init__(*args, **kwargs)

    @staticmethod
    def format_regex(regexp):
        capture_patt = re.compile(r'([(][?]P<[^>]+>|[(](?![?]))')
        return regexp if '(' not in regexp else capture_patt.sub('(?:', regexp)


class IntFilter(RegexFilter):
    def __init__(self):
        super(IntFilter, self).__init__(name='int', regexp=r'[+-]?[0-9]+')


class FloatFilter(RegexFilter):
    def __init__(self):
        super(FloatFilter, self).__init__(name='float', regexp=r'[+-]?([0-9]*[.])?[0-9]+')
