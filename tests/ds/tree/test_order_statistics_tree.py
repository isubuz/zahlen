# -*- coding: utf-8 -*-

"""
    Test case module for zahlen.ds.tree.order_statistics_tree

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from zahlen.ds.tree.order_statistics_tree import Node, OrderStatisticsTree

import unittest


def get_ost(keys):
    ost = OrderStatisticsTree(Node)
    for key in keys:
        ost.insert(key)
    return ost


class TestKthSmallestKey(unittest.TestCase):
    def setUp(self):
        self.ost = get_ost([8, 3, 2, 5, 4, 6, 12, 13, 10, 7])

    def test_empty_tree_exception(self):
        ost = OrderStatisticsTree(Node)
        self.assertRaises(Exception, ost.kth_smallest_key, 1)

    def test_k_less_than_1_exception(self):
        self.assertRaises(IndexError, self.ost.kth_smallest_key, 0)

    def test_k_less_than_root_weight_exception(self):
        root = self.ost.root
        self.assertRaises(IndexError, self.ost.kth_smallest_key, root.weight + 1)
        left = root.left
        self.assertRaises(IndexError, self.ost.kth_smallest_key, left.weight + 1,
                          root=left)

    def test_smallest_element_from_root(self):
        self.assertEqual(self.ost.kth_smallest_key(1), 2)

    def test_smallest_element_from_non_root(self):
        self.assertEqual(
            self.ost.kth_smallest_key(4, root=self.ost.root.right), 10)

    def test_largest_element_from_root(self):
        self.assertEqual(self.ost.kth_smallest_key(self.ost.root.weight), 13)

    def test_largest_element_from_non_root(self):
        root = self.ost.root.left
        self.assertEqual(self.ost.kth_smallest_key(root.weight, root=root), 4)

    def test_path_right_left_right(self):
        self.assertEqual(self.ost.kth_smallest_key(6), 7)

    def test_path_left_right(self):
        self.assertEqual(self.ost.kth_smallest_key(3), 4)

    def test_leaf_node_as_smallest(self):
        self.assertEqual(self.ost.kth_smallest_key(2), 3)

    def test_internal_complete_node_as_smallest(self):
        self.assertEqual(self.ost.kth_smallest_key(7), 8)
        self.assertEqual(self.ost.kth_smallest_key(9), 12)

    def test_internal_non_complete_node_as_smallest(self):
        self.assertEqual(self.ost.kth_smallest_key(5), 6)


class TestKthSuccessor(unittest.TestCase):
    def setUp(self):
        self.ost = get_ost([8, 3, 2, 5, 4, 6, 12, 13, 10, 7])

    def test_empty_tree_exception(self):
        ost = OrderStatisticsTree(Node)
        self.assertRaises(Exception, ost.kth_successor, 1, 1)

    def test_k_less_than_0_exception(self):
        self.assertRaises(IndexError, self.ost.kth_successor, -1, 1)

    def test_k_greater_than_successor_count_exception(self):
        self.assertRaises(IndexError, self.ost.kth_successor, 2, 12)
        self.assertRaises(IndexError, self.ost.kth_successor, 5, 7)
        self.assertRaises(IndexError, self.ost.kth_successor, 7, 6)
        self.assertRaises(IndexError, self.ost.kth_successor, 1, 13)

    def test_k_0(self):
        self.assertEqual(self.ost.kth_successor(0, 8), 8)
        self.assertEqual(self.ost.kth_successor(0, 5), 5)
        self.assertEqual(self.ost.kth_successor(0, 10), 10)
        self.assertEqual(self.ost.kth_successor(0, 2), 2)
        self.assertEqual(self.ost.kth_successor(0, 13), 13)

    def test_parent_successor_of_leaf_node(self):
        self.assertEqual(self.ost.kth_successor(1, 2), 3)
        self.assertEqual(self.ost.kth_successor(1, 4), 5)

    def test_non_parent_successor_of_leaf_node(self):
        self.assertEqual(self.ost.kth_successor(1, 7), 8)

    def test_successor_in_right_subtree(self):
        self.assertEqual(self.ost.kth_successor(1, 3), 4)
        self.assertEqual(self.ost.kth_successor(2, 5), 7)
        self.assertEqual(self.ost.kth_successor(3, 5), 8)
        self.assertEqual(self.ost.kth_successor(1, 8), 10)
        self.assertEqual(self.ost.kth_successor(1, 12), 13)

    def test_ancestor_successor(self):
        self.assertEqual(self.ost.kth_successor(3, 2), 5)
        self.assertEqual(self.ost.kth_successor(1, 4), 5)
        self.assertEqual(self.ost.kth_successor(1, 7), 8)

    def test_successor_in_different_subtree(self):
        self.assertEqual(self.ost.kth_successor(6, 2), 8)
        self.assertEqual(self.ost.kth_successor(7, 3), 12)
        self.assertEqual(self.ost.kth_successor(5, 4), 10)
        self.assertEqual(self.ost.kth_successor(7, 4), 13)