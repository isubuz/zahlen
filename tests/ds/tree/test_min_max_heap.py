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

    def test_swap_child_parent_min_level(self):
        """Swap 0 with its parent 3 which is at a min level."""
        mmh = MinMaxHeap([2, 1, 4, 3, 5, 2, -1, 7, 0, 6])
        self.assertListEqual(mmh.elements, [-1, 7, 4, 2, 1, 2, 0, 5, 3, 6])

    def test_swap_child_parent_max_level(self):
        """Swap 3 with its parent 1 which is at a max level."""
        mmh = MinMaxHeap([2, 1, 6, 3, 2, 2, -1, 5, 4])
        self.assertListEqual(mmh.elements, [-1, 5, 6, 2, 2, 2, 1, 3, 4])

    def test_swap_grandchild_grandparent_min_level(self):
        """Swap -1 with its grand parent 2 which is at a max level."""
        mmh = MinMaxHeap([2, 4, 6, 2, 3, 4, -1, 4])
        self.assertListEqual(mmh.elements, [-1, 4, 6, 2, 3, 4, 2, 4])

    def test_swap_grandchild_grandparent_max_level(self):
        """Swap 5 with its grand parent 4 which is at a max level."""
        mmh = MinMaxHeap([2, 4, 6, 2, 3, 4, -1, 5])
        self.assertListEqual(mmh.elements, [-1, 5, 6, 2, 3, 4, 2, 4])

    def test_swap_grandchild_trickle_down_min_level(self):
        """Swap 1 with its grand parent 4 which is at a min level. 4 is then
        trickled down and swapped with its child 2.
        """
        mmh = MinMaxHeap([4, 8, 4, 1, 5, 2, -1, 7, 2, 6, 8, 1, 4, 5, 6, 6, 4, 2,
                          1])
        self.assertListEqual(mmh.elements, [-1, 8, 6, 1, 5, 1, 1, 7, 4, 6, 8,
                                            2, 4, 4, 5, 6, 4, 2, 2])

    def test_swap_grandchild_trickle_down_max_level(self):
        """Swap 7 with its grand parent 5 which is at a max level. 5 is then
        trickled down and swapped with 6.
        """
        mmh = MinMaxHeap([2, 5, 4, 3, 5, 2, -1, 7, 6, 6, 8, 1, 4, 5, 3, 6, 4, 2,
                          0])
        self.assertListEqual(mmh.elements, [-1, 8, 5, 2, 5, 1, 0, 6, 6, 6, 7, 2,
                                            4, 4, 3, 5, 4, 3, 2])


if __name__ == '__main__':
    unittest.main()