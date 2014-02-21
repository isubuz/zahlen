# -*- coding: utf-8 -*-

"""

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""


class Node(object):
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.key_count = 1
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

