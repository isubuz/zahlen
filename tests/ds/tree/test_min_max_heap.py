# -*- coding: utf-8 -*-

"""
    Test case module for zahlen.ds.tree.min_max_heap

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from zahlen.ds.tree.min_max_heap import MinMaxHeap

import unittest


class TestBuildMinMaxHeap(unittest.TestCase):
    """Assert the contents of the heap after it has constructed for a list of
    elements.
    """

    def test_empty_heap(self):
        mmh = MinMaxHeap([])
        self.assertListEqual(mmh.elements, [])

    def test_single_element_in_heap(self):
        mmh = MinMaxHeap([10])
        self.assertListEqual(mmh.elements, [10])

    def test_root_with_single_child(self):
        mmh1 = MinMaxHeap([10, 5])
        mmh2 = MinMaxHeap([5, 10])
        self.assertListEqual(mmh1.elements, [5, 10])
        self.assertListEqual(mmh2.elements, [5, 10])

    def test_complete_root(self):
        mmh1 = MinMaxHeap([10, 5, 6])
        mmh2 = MinMaxHeap([5, 6, 10])
        self.assertListEqual(mmh1.elements, [5, 10, 6])
        self.assertListEqual(mmh2.elements, [5, 6, 10])

    def test_tree_all_leaves_at_same_level(self):
        mmh = MinMaxHeap([2, 1, 4, 3, 5, 2, -1])
        self.assertListEqual(mmh.elements, [-1, 5, 4, 2, 3, 2, 1])

    def test_tree_leaves_at_unequal_levels(self):
        mmh = MinMaxHeap([2, 1, 4, 3, 5, 2, -1, 7, 3, 0])
        self.assertListEqual(mmh.elements, [-1, 7, 4, 2, 1, 2, 0, 3, 3, 5])

    # Grandchild - repl (with(out) trickle down at min/max level)
    # Child - repl (min/max leveL)

if __name__ == '__main__':
    unittest.main()