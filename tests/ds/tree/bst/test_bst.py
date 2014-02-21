# -*- coding: utf-8 -*-

"""
    Test case module for

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from zahlen.ds.tree.bst.tree import BinarySearchTree

import unittest


class TestRootNodeInsert(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()
        self.bst.insert(10)

    def test_root_node_key(self):
        self.assertEqual(self.bst.root.key, 10)

    def test_root_node_empty_children(self):
        root = self.bst.root
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)


class TestInsert(unittest.TestCase):
    def test_left(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2])
        self.assertEqual(bst.root.left.key, 2)
        self.assertIsNone(bst.root.right)

    def test_right(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 12])
        self.assertIsNone(bst.root.left)
        self.assertEqual(bst.root.right.key, 12)

    def test_left_right_left(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 7])
        bst.insert(4)
        self.assertEqual(bst.root.left.right.left.key, 4)

    def test_left_right_right(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 4])
        bst.insert(7)
        self.assertEqual(bst.root.left.right.right.key, 7)

    def test_right_right_right(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 15, 12, 18, 16])
        bst.insert(24)
        self.assertEqual(bst.root.right.right.right.key, 24)

    def test_right_right_left(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 15, 12, 18, 24])
        bst.insert(16)
        self.assertEqual(bst.root.right.right.left.key, 16)

    def test_duplicate_root(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 10, 10, 10])
        self.assertEqual(bst.root.key, 10)
        self.assertEqual(bst.root.key_count, 4)
        self.assertIsNone(bst.root.left)
        self.assertIsNone(bst.root.right)

    def test_duplicate_leaf(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 5])
        bst.insert(12)
        self.assertTrue(bst.root.right.is_leaf())
        self.assertEqual(bst.root.right.key_count, 2)

    def test_duplicate_internal_complete(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 4, 7])
        bst.insert(6)
        self.assertEqual(bst.root.left.right.key, 6)
        self.assertEqual(bst.root.left.right.key_count, 2)

    def test_duplicate_internal_non_complete(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 4, 7])
        bst.insert(2)
        self.assertEqual(bst.root.left.key, 2)
        self.assertEqual(bst.root.left.key_count, 2)


class TestSort(unittest.TestCase):
    def test_empty_tree(self):
        bst = BinarySearchTree()
        self.assertListEqual(bst.sorted_keys(), [])

    def test_tree_single_element(self):
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertListEqual(bst.sorted_keys(), [10])

    def test_tree_multiple_elements(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(), [1, 2, 3, 4, 5])

    def test_tree_multiple_elements_with_duplicates(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3, 1, 1, 6, 4])
        self.assertListEqual(bst.sorted_keys(), [1, 1, 1, 2, 3, 4, 4, 5, 6])

    def test_tree_all_duplicates(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 2, 2, 2, 2, 2, 2])
        self.assertListEqual(bst.sorted_keys(), [2, 2, 2, 2, 2, 2, 2])

    def test_sort_at_leaf_node(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(bst.root.right.left), [3])

    def test_sort_at_internal_complete_node(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(bst.root.right), [3, 4, 5])

    def test_sort_at_internal_non_complete_node(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3, 6])
        self.assertListEqual(bst.sorted_keys(bst.root.right.right), [5, 6])


def _insert(bst, keys):
    for key in keys:
        bst.insert(key)

if __name__ == '__main__':
    unittest.main()
