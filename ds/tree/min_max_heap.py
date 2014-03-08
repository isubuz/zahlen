# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.min_max_heap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Min-Max heap data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque
from math import floor, log


class MinMaxHeap(object):
    def __init__(self, elements):
        self._elements = deque(elements)
        self._build()

    @property
    def elements(self):
        return list(self._elements)

    def delete_max(self):
        maximum = self.maximum()
        self._elements.remove(maximum)
        return maximum

    def delete_min(self):
        minimum = self.minimum()
        self._elements.popleft()
        return minimum

    def minimum(self):
        if not self._elements:
            raise ValueError('Heap is empty')
        return self._elements[0]

    def maximum(self):
        if not self._elements:
            raise ValueError('Heap is empty')
        maximum = self._elements[0]
        for child in self._get_children(0):
            if self._elements[child] > maximum:
                maximum = self._elements[child]
        return maximum

    def insert(self, value):
        pass

    def _get_children(self, index):
        max_size = len(self._elements) - 1
        children = []
        left = 2 * index + 1
        if left <= max_size:
            children.append(left)
            if left + 1 <= max_size:
                children.append(left + 1)
        return children

    def _get_children_and_grand_children(self, index):
        """Return children and grand-children of a node at index ``index``.

        The returned list contains children before the grand-children.
        Grand-children are the children of the children.
        """

        # Add children
        indices = self._get_children(index)

        # Add grandchildren
        grand_children = [child for i in indices
                          for child in self._get_children(i)]
        indices.extend(grand_children)

        return indices

    @staticmethod
    def _is_grand_child(index, child):
        return child > (2 * index + 2)

    def _swap_max(self, i, j):
        if self._elements[i] > self._elements[j]:
            self._elements[i], self._elements[j] = \
                self._elements[j], self._elements[i]

    def _swap_min(self, i, j):
        if self._elements[i] < self._elements[j]:
            self._elements[i], self._elements[j] = \
                self._elements[j], self._elements[i]

    def _build(self):
        heap_size = len(self._elements)
        mid = heap_size / 2 - 1
        for i in xrange(mid, -1, -1):
            level = floor(log(i + 1, 2))
            if level % 2 == 0:
                self._trickle_down_min(i)   # Even min level
            else:
                self._trickle_down_max(i)   # Odd max level

    def _trickle_down_min(self, index):
        for child in self._get_children_and_grand_children(index):
            self._swap_min(child, index)
            if self._is_grand_child(index, child):
                self._trickle_down_min(child)

    def _trickle_down_max(self, index):
        for child in self._get_children_and_grand_children(index):
            self._swap_max(child, index)
            if self._is_grand_child(index, child):
                self._trickle_down_max(child)