#!/usr/bin/env python
# coding: utf-8

def haha():
    print(locals())

haha()
print(globals())
print(type(globals()))