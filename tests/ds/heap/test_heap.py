# -*- coding: utf-8 -*-

"""
    Test case module for zahlen.ds.heap.heap

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from zahlen.ds.heap.heap import Heap

import unittest


class TestHeap(unittest.TestCase):
    def test_min_heap(self):
        heap = Heap([2, 3, 0, 9, -1, 4, 9])
        print heap.elements
        heap.sort()
        print heap.elements

    def test_max_heap(self):
        heap = Heap([2, 3, 0, 9, -1, 4, 9], min_heap=False)
        print heap.elements
        heap.sort()
        print heap.elements
