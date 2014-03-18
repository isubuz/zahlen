# -*- coding: utf-8 -*-

"""
    zahlen.ds.heap.min_max_median_heap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Min-max-median heap data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""


class MinMaxMedianHeap(object):
    def __init__(self):
        self._min_max_heap = None
        self._max_min_heap = None
        self._median = None

    def min(self):
        """Returns the minimum value in the heap."""
        return self._min_max_heap.min()

    def median(self):
        """Returns the median in the heap."""
        return self._median

    def max(self):
        """Returns the maximum element in the heap."""
        return self._max_min_heap.max()

    def delete_min(self):
        """Deletes and returns the minimum element in the heap."""
        minimum = self._min_max_heap.delete_min()
        self._balance()
        return minimum

    def delete_median(self):
        """Deletes and returns the median in the heap.

        If the no. of elements in the heap is even, the deleted value is the
        smaller of the two mid elements.
        """
        diff = self._min_max_heap.size - self._max_min_heap.size
        if diff == 1:
            median = self._min_max_heap.max()
        elif diff == -1:
            median = self._max_min_heap.min()
        else:
            left = self._min_max_heap.max()
            right = self._max_min_heap.min()
            median = self._min_max_heap.delete_max() if left < right \
                else self._max_min_heap.delete_min()
        self._balance()
        self._set_median()
        return median

    def delete_max(self):
        """Deletes and returns the maximum value in the heap."""
        maximum = self._max_min_heap.delete_max()
        self._balance()
        return maximum

    def insert(self, value):
        """Inserts ``value`` into the heap."""
        if value >= self._median:
            self._max_min_heap.insert(value)
        else:
            self._min_max_heap.insert(value)

        self._balance()
        self._set_median()

    def _balance(self):
        """Balances the sizes of the min-max heap and the max-min heap if the
        difference is greater than 1.
        """
        diff = self._min_max_heap.size - self._max_min_heap.size
        if diff > 1:
            self._max_min_heap.insert(self._min_max_heap.delete_max())
        elif diff < -1:
            self._min_max_heap.insert(self._max_min_heap.delete_min())

    def _set_median(self):
        """Calculates and sets the median in the heap.

        If the no. of elements in the heap is even, the median is the smaller of
        the two mid elements.
        """
        diff = self._min_max_heap.size - self._max_min_heap.size
        if diff == 1:
            median = self._min_max_heap.max()
        elif diff == -1:
            median = self._max_min_heap.min()
        else:
            median = min(self._min_max_heap.max(), self._max_min_heap.min())
        self._median = median