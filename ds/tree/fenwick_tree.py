# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.fenwick_tree
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Fenwick tree (also known as Bit Indexed Tree)
    data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""


class FenwickTree(object):
    """Construct a Fenwick tree.

    This implementation of the Fenwick Tree uses a fixed length array to
    represent the tree. The size of the tree is specified during the
    construction of the tree and cannot be modified i.e. new elements cannot be
    added but existing elements can be modified.

    Example usage::
        # Construct the tree
        ft = FenwickTree(10)

        # Update an element at an index
        ft.update(index, value)

        # Read the value at an index
        ft.read(index)
    """

    def __init__(self, size):
        """
        :param size: no. of elements to be contained in the tree
        """

        if size < 1:
            raise ValueError('Size must be greater than 0')

        self._size = size
        self._tree = [0] * self._size

    @property
    def size(self):
        return self._size

    def read(self, index):
        """Read the value at the specified index.

        As the tree is implemented using a fixed length array, the index must be
        based on a 0-indexed array.
        """

        if not 0 <= index <= self._size - 1:
            raise IndexError('Invalid index: {0}'.format(index))

        value = 0
        index += 1  # position w.r.t a one-indexed array.
        while index > 0:
            value += self._tree[index - 1]
            index -= (index & -index)
        return value

    def update(self, index, value):
        """Update the value at the specified index.

        As the tree is implemented using a fixed length array, the index must be
        based on a 0-indexed array.
        """

        if not 0 <= index <= self._size - 1:
            raise IndexError('Invalid index: {0}'.format(index))

        index += 1  # position w.r.t a one-indexed array.
        while index <= self._size:
            self._tree[index - 1] += value
            index += (index & -index)
