# -*- coding: utf-8 -*-

from collections import defaultdict


class KeyDefaultDict(defaultdict):
    def __missing__(self, key):
        if not self.default_factory:
            raise KeyError(key)
        else:
            self[key] = self.default_factory(key)
            return self[key]
