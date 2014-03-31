# -*- coding: utf-8 -*-

"""
    Test case module for zahlen.ds.tree.binary_search_tree

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque
from zahlen.ds.tree.binary_search_tree import BinarySearchTree, Node

import unittest


def create_bst(keys):
    """Creates and returns a Binary Search Tree."""
    bst = BinarySearchTree(Node)
    for key in keys:
        bst.insert(key)
    return bst


class BSTTestCase(unittest.TestCase):
    """Provides methods to test the structure of a Binary Search Tree."""

    def assert_tree(self, actual, expected):
        queue = deque()
        queue.append((actual.root, expected.root))
        while queue:
            actual_node, expected_node = queue.popleft()
            self.assert_node(actual_node, expected_node)

            if expected_node:
                if expected_node.left:
                    queue.appendleft((actual_node.left, expected_node.left))
                if expected_node.right:
                    queue.appendleft((actual_node.right, expected_node.right))

    def assert_node(self, actual, expected):
        if not expected:
            self.assertIsNone(actual)
        else:
            self.assertIsNotNone(actual)
            self.assertEqual(actual.key, expected.key)

            for act, exp in [(actual.left, expected.left),
                             (actual.right, expected.right),
                             (actual.parent, expected.parent)]:
                if exp:
                    self.assertIsNotNone(act)
                    self.assertEqual(act.key, exp.key)
                else:
                    self.assertIsNone(act)


class TestBSTStructure(unittest.TestCase):
    """Test cases to verify the structure of the BST after inserting one or more
    keys.
    """

    def setUp(self):
        self.bst = create_bst([8, 3, 2, 5, 4, 6, 1, 12, 13, 10, 11])

    def test_leaf_nodes(self):
        root = self.bst.root
        self.assert_leaf_node(root.left.left.left, 1, 2)
        self.assert_leaf_node(root.left.right.left, 4, 5)
        self.assert_leaf_node(root.left.right.right, 6, 5)
        self.assert_leaf_node(root.right.left.right, 11, 10)
        self.assert_leaf_node(root.right.right, 13, 12)

    def test_internal_complete_node(self):
        root = self.bst.root
        self.assert_node(root.left, 3, 2, 5, 8)
        self.assert_node(root.left.right, 5, 4, 6, 3)
        self.assert_node(root.right, 12, 10, 13, 8)
        self.assert_node(root, 8, 3, 12, None)

    def test_internal_non_complete_node(self):
        root = self.bst.root
        self.assert_node(root.left.left, 2, 1, None, 3)
        self.assert_node(root.right.left, 10, None, 11, 12)

    def assert_node(self, actual, key, left_key=None, right_key=None,
                    parent_key=None):
        self.assertEqual(actual.key, key)

        for ptr, val in [(actual.left, left_key),
                         (actual.right, right_key),
                         (actual.parent, parent_key)]:
            if val:
                self.assertEqual(ptr.key, val)
            else:
                self.assertIsNone(ptr)

    def assert_leaf_node(self, actual, key, parent_key):
        self.assert_node(actual, key, parent_key=parent_key)


class TestInsert(unittest.TestCase):
    def test_path_left(self):
        bst = create_bst([10, 2])
        self.assertEqual(bst.root.left.key, 2)
        self.assertIsNone(bst.root.right)

    def test_path_right(self):
        bst = create_bst([10, 12])
        self.assertIsNone(bst.root.left)
        self.assertEqual(bst.root.right.key, 12)

    def test_path_left_right_left(self):
        bst = create_bst([10, 2, 12, 6, 7])
        bst.insert(4)
        self.assertEqual(bst.root.left.right.left.key, 4)

    def test_path_left_right_right(self):
        bst = create_bst([10, 2, 12, 6, 4])
        bst.insert(7)
        self.assertEqual(bst.root.left.right.right.key, 7)

    def test_path_right_right_right(self):
        bst = create_bst([10, 15, 12, 18, 16])
        bst.insert(24)
        self.assertEqual(bst.root.right.right.right.key, 24)

    def test_path_right_right_left(self):
        bst = create_bst([10, 15, 12, 18, 24])
        bst.insert(16)
        self.assertEqual(bst.root.right.right.left.key, 16)


class TestDelete(BSTTestCase):
    """Test cases for delete operations on a Binary Search Tree."""

    def setUp(self):
        self.bst = create_bst([8, 3, 2, 5, 4, 6, 1, 12, 13, 10, 11])

    def test_del_key_not_exists(self):
        self.assertRaises(KeyError, self.bst.delete, 99)

    def test_del_empty_tree_after_delete(self):
        bst = create_bst([10])
        bst.delete(10)
        self.assertFalse(bst.root)

    def test_del_left_leaf_node(self):
        self.bst.delete(1)
        expected = create_bst([8, 3, 2, 5, 4, 6, 12, 13, 10, 11])
        self.assert_tree(self.bst, expected)

    def test_del_right_leaf_node(self):
        self.bst.delete(11)
        expected = create_bst([8, 3, 2, 5, 4, 6, 1, 12, 13, 10])
        self.assert_tree(self.bst, expected)

    def test_del_complete_node_successor_is_right_child_and_leaf_node(self):
        self.bst.delete(12)
        expected = create_bst([8, 3, 2, 5, 4, 6, 1, 13, 10, 11])
        self.assertTrue(self.bst, expected)

    def test_del_complete_node_successor_is_leaf_node(self):
        self.bst.delete(3)
        expected = create_bst([8, 4, 2, 5, 6, 1, 12, 13, 10, 11])
        self.assertTrue(self.bst, expected)

    def test_del_complete_node_successor_is_internal_non_complete_node(self):
        self.bst.delete(8)
        expected = create_bst([10, 3, 2, 5, 4, 6, 1, 12, 11, 13])
        self.assertTrue(self.bst, expected)

    def test_del_non_complete_node_no_left_child(self):
        self.bst.delete(10)
        expected = create_bst(([8, 3, 2, 5, 4, 6, 1, 12, 11, 13]))
        self.assert_tree(self.bst, expected)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.bst = create_bst([3, 1, 0, 5, 4, 8, 9, 0, 5])

    def test_empty_tree(self):
        bst = create_bst([])
        self.assertFalse(bst.search(10))

    def test_exists_in_tree_with_single_element(self):
        bst = create_bst([10])
        self.assertTrue(bst.search(10))

    def test_not_exists_in_tree_with_single_element(self):
        bst = create_bst([10])
        self.assertFalse(bst.search(1))

    def test_exists_leaf_node_left_child(self):
        self.assertTrue(self.bst.search(0))

    def test_exists_leaf_node_right_child(self):
        self.assertTrue(self.bst.search(9))

    def test_exists_internal_non_complete_node(self):
        self.assertTrue(self.bst.search(1))

    def test_exists_internal_complete_node(self):
        self.assertTrue(self.bst.search(5))

    def test_exists_duplicate_key(self):
        self.assertTrue(self.bst.search(5))

    def test_not_exists_missing_right(self):
        self.assertFalse(self.bst.search(2))

    def test_not_exists_missing_left(self):
        self.assertFalse(self.bst.search(7))


class TestSort(unittest.TestCase):
    def test_empty_tree(self):
        bst = create_bst([])
        self.assertListEqual(bst.sorted_keys(), [])

    def test_tree_with_single_element(self):
        bst = create_bst([10])
        self.assertListEqual(bst.sorted_keys(), [10])

    def test_tree_with_multiple_elements(self):
        bst = create_bst([2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(), [1, 2, 3, 4, 5])