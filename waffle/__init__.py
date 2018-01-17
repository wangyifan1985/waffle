#!/usr/bin/env python
# coding: utf-8


__author__ = ['Yifan Wang <yifan_wang@silanis.com>']
__copyright__ = "Copyright (C) 2017, The Waffle Authors"
__license__ = "MIT"
__version__ = '0.1.0'
__description__ = 'Blog system'
__status__ = "Internal"


def check_environment():
    import platform
    if platform.python_version_tuple() < ('3', '6') or platform.python_implementation() != 'CPython':
        raise RuntimeError('Waffle requires CPython 3.6 or greater.')


check_environment()


class Waffle(Exception):
    pass
