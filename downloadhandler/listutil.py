#!/usr/bin/env python2

def first(l, default=None):
    return default if len(l) < 1 else l[0]
