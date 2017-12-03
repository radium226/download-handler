#!/usr/bin/env python3

def first(l, default=None):
    return default if len(l) < 1 else l[0]
