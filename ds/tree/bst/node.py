# -*- coding: utf-8 -*-

"""

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""


class Node(object):
    def __init__(self, key):
        self.size = 1
        self.key = key
        self.key_count = 1
        self._left = None
        self._right = None
        self.parent = None

    def __eq__(self, other):
        return self.key == other.key

    def __str__(self):
        return 'key:{0},size:{1},count:{2}'.format(self.key, self.size,
                                                   self.key_count)

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node
        if node:
            node.parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        if node:
            node.parent = self

    def add_child(self, child):
        """Add a left or a right child based on the child's key.

        Note that child's key will be less than or greater than the current
        node's key. The child's parent pointer is updated too.
        """

        if child.key < self.key:
            self.left = child
        else:
            self.right = child

    def is_complete(self):
        """Return true if node is a complete node.

        A complete node is an internal node which has non-none left and right
        children.
        """

        return self.left and self.right

    def is_leaf(self):
        """Return true if node is a leaf node."""

        return self.left is None and self.right is None

