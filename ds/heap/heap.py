# -*- coding: utf-8 -*-

"""
    zahlen.ds.heap.heap
    ~~~~~~~~~~~~~~~~~~~

    This module implements the Heap data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

import operator


class Heap(object):
    def __init__(self, elements, min_heap=True):
        self._opr = operator.lt if min_heap else operator.gt

        if not elements:
            self.elements = []
        else:
            self.elements = elements[:]
            self._build()

    @property
    def heap_size(self):
        return len(self.elements)

    def insert(self, value):
        """Inserts ``value`` into the heap."""
        pass

    def delete(self, index):
        """Deletes an element at index ``index``."""
        pass

    def sort(self):
        """Sorts the elements in the heap.

        ..note::
            The sorted list of elements can be obtained from ``heap.elements``.
            For a min-heap the elements are sorted in ascending order but for a
            max-heap the elements are sorted in descending order.
        """
        for i in xrange(self.heap_size - 1, 0, -1):
            self.elements[i], self.elements[0] = \
                self.elements[0], self.elements[i]

            self._trickle_down(0, i - 1)

    def _build(self):
        mid = self.heap_size / 2 - 1
        for i in xrange(mid, -1, -1):
            self._trickle_down(i)

    def _trickle_down(self, index, max_index=None):
        if max_index is None:
            max_index = self.heap_size - 1

        left_index = 2 * index + 1
        right_index = left_index + 1

        winner = index
        for i in [left_index, right_index]:
            if i <= max_index and \
                    self._opr(self.elements[i], self.elements[winner]):
                winner = i

        if winner != index:
            self.elements[winner], self.elements[index] = \
                self.elements[index], self.elements[winner]
            self._trickle_down(winner, max_index)