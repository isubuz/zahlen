# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.min_max_heap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Min-Max heap data structure.

    - Add tests for insert()
    - Check if build can be replaced by insert().
    - Added test cases for minimum(), maximum(), delete_min(), delete_max()
    - Rethink variable names and documentation.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque
from math import floor, log

import operator


class MinMaxHeap(object):
    def __init__(self, elements):
        # self._elements = deque()
        # for element in elements:
        #     self.insert(element)
        self._elements = deque(elements)
        if self._elements:
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
        """Insert a new value into the heap."""
        next_leaf_index = len(self._elements)
        self._elements.append(value)

        if next_leaf_index != 0:    # Inserting a leaf node (or anon-root node)
            parent_index = self._parent_index(next_leaf_index)

            level = floor(log(next_leaf_index + 1, 2))
            if level % 2 == 0:  # Even min level
                if self._swap(next_leaf_index, parent_index, operator.gt):
                    self._bubble_up_max(parent_index)
                else:
                    self._bubble_up_min(next_leaf_index)
            else:   # Odd max level
                if self._swap(next_leaf_index, parent_index, operator.lt):
                    self._bubble_up_min(parent_index)
                else:
                    self._bubble_up_max(next_leaf_index)

    @staticmethod
    def _is_grand_child(index, child):
        return child > (2 * index + 2)

    @classmethod
    def _parent_index(cls, index):
        """Returns the parent (if any) index of ``index.``"""
        if not index:
            return None
        else:
            return (index - 1) / 2 if index % 2 != 0 else (index - 2) / 2

    @classmethod
    def _grand_parent_index(cls, index):
        """Returns the grand parent (if any) index of ``index``."""
        return cls._parent_index(cls._parent_index(index))

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

    def _swap(self, i, j, cmp):
        """Swaps elements at index i and j and returns true if comparator
        returns true. Else returns false.
        """
        if cmp(self._elements[i], self._elements[j]):
            self._elements[i], self._elements[j] = \
                self._elements[j], self._elements[i]
            return True
        else:
            return False

    def _build(self):
        heap_size = len(self._elements)
        mid = heap_size / 2 - 1
        for i in xrange(mid, -1, -1):
            level = floor(log(i + 1, 2))
            if level % 2 == 0:
                self._trickle_down_min(i)   # Even min level
            else:
                self._trickle_down_max(i)   # Odd max level

    def _bubble_up_min(self, index):
        """Bubbles the minimum value up the tree by comparing with the grand
        parent's value.
        """
        grand_parent_index = self._grand_parent_index(index)
        if grand_parent_index:
            if self._swap(index, grand_parent_index, operator.lt):
                self._bubble_up_min(grand_parent_index)

    def _bubble_up_max(self, index):
        """Bubbles the maximum value up the tree by comparing with the grand
        parent's value.
        """
        grand_parent_index = self._grand_parent_index(index)
        if grand_parent_index:
            if self._swap(index, grand_parent_index, operator.gt):
                self._bubble_up_max(grand_parent_index)

    def _trickle_down_min(self, index):
        for child in self._get_children_and_grand_children(index):
            self._swap(child, index, operator.lt)
            if self._is_grand_child(index, child):
                self._trickle_down_min(child)

    def _trickle_down_max(self, index):
        for child in self._get_children_and_grand_children(index):
            self._swap(child, index, operator.gt)
            if self._is_grand_child(index, child):
                self._trickle_down_max(child)