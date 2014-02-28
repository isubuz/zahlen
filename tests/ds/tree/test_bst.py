# -*- coding: utf-8 -*-

"""
    Test case module for zahlen.ds.tree.bst

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque
from zahlen.ds.tree.bst import BinarySearchTree, TreeKeyError, \
    SmallestElementIndexError, SuccessorIndexError

import unittest


class BSTTestCase(unittest.TestCase):
    """This class provides methods to test the equality of Binary search trees
    and nodes in a tree.
    """

    def assert_tree(self, actual, expected):
        """Assert if two trees are equal."""

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
        """Assert if two nodes are equal."""

        if not expected:
            self.assertIsNone(actual)
        else:
            self.assertIsNotNone(actual)

            self.assertEqual(actual.key, expected.key)
            self.assertEqual(actual.key_count, expected.key_count)
            self.assertEqual(actual.size, expected.size)

            for act, exp in [(actual.left, expected.left),
                             (actual.right, expected.right),
                             (actual.parent, expected.parent)]:
                if exp:
                    self.assertIsNotNone(act)
                    self.assertEqual(act.key, exp.key)
                else:
                    self.assertIsNone(act)


class TestBSTStructure(unittest.TestCase):
    """This class contains test cases to verify the structure of the BST after
    inserting one or more keys.
    """

    def setUp(self):
        self.bst = _get_bst([8, 3, 2, 5, 3, 4, 6, 1, 2, 12, 13, 6, 10, 11, 2])

    def test_leaf_nodes(self):
        root = self.bst.root
        self.assert_leaf_node(root.left.left.left, 1, 1, 2)
        self.assert_leaf_node(root.left.right.left, 4, 1, 5)
        self.assert_leaf_node(root.left.right.right, 6, 2, 5)
        self.assert_leaf_node(root.right.left.right, 11, 1, 10)
        self.assert_leaf_node(root.right.right, 13, 1, 12)

    def test_internal_complete_nodes(self):
        root = self.bst.root
        self.assert_node(root.left, 3, 2, 6, 2, 5, 8)
        self.assert_node(root.left.right, 5, 1, 3, 4, 6, 3)
        self.assert_node(root.right, 12, 1, 4, 10, 13, 8)

    def test_internal_non_complete_node(self):
        root = self.bst.root
        self.assert_node(root.right.left, 10, 1, 2, right_key=11, parent_key=12)
        self.assert_node(root.left.left, 2, 3, 2, left_key=1, parent_key=3)

    def assert_node(self, actual, key, key_count, size, left_key=None,
                    right_key=None, parent_key=None):
        self.assertEqual(actual.key, key)
        self.assertEqual(actual.key_count, key_count)
        self.assertEqual(actual.size, size)

        for ptr, val in [(actual.left, left_key),
                         (actual.right, right_key),
                         (actual.parent, parent_key)]:
            if val:
                self.assertEqual(ptr.key, val)
            else:
                self.assertIsNone(ptr)

    def assert_leaf_node(self, actual, key, key_count, parent_key):
        self.assert_node(actual, key, key_count, 1, parent_key=parent_key)


class TestDelete(BSTTestCase):
    def setUp(self):
        self.bst = _get_bst([8, 3, 2, 5, 3, 4, 6, 1, 2, 12, 13, 6, 10, 11, 2])

    def test_del_key_not_exists(self):
        self.assertRaises(TreeKeyError, self.bst.delete, 99)

    def test_del_empty_tree_after_delete(self):
        bst = _get_bst([10])
        bst.delete(10)
        self.assertFalse(bst.root)

    def test_del_left_leaf_node(self):
        self.bst.delete(1)
        expected = _get_bst([8, 3, 2, 5, 3, 4, 6, 2, 12, 13, 6, 10, 11, 2])
        self.assert_tree(self.bst, expected)

    def test_del_right_leaf_node(self):
        self.bst.delete(11)
        expected = _get_bst([8, 3, 2, 5, 3, 4, 6, 1, 2, 12, 13, 6, 10, 2])
        self.assert_tree(self.bst, expected)

    def test_del_repeated_leaf_node(self):
        """Test that only 1 occurrence of the repeated leaf node is deleted."""
        self.bst.delete(6)
        expected = _get_bst([8, 3, 2, 5, 3, 4, 6, 1, 2, 12, 13, 10, 11, 2])
        self.assert_tree(self.bst, expected)

    def test_del_complete_node_successor_is_right_child_and_leaf_node(self):
        self.bst.delete(12)
        expected = _get_bst([8, 3, 2, 5, 3, 4, 6, 1, 2, 13, 6, 10, 11, 2])
        self.assert_tree(self.bst, expected)

    def test_del_complete_node_successor_is_leaf_node(self):
        self.bst.delete(3)
        self.bst.delete(3)  # Delete both occurrences of 3
        expected = _get_bst([8, 4, 2, 5, 6, 1, 2, 12, 13, 6, 10, 11, 2])
        self.assert_tree(self.bst, expected)

    def test_del_complete_node_successor_is_repeated_node(self):
        self.bst.delete(5)
        expected = _get_bst([8, 3, 2, 3, 6, 4, 1, 2, 12, 13, 6, 10, 11, 2])
        self.assert_tree(self.bst, expected)

    def test_del_complete_node_successor_is_internal_non_complete_node(self):
        self.bst.delete(8)
        expected = _get_bst([10, 3, 2, 5, 3, 4, 6, 1, 2, 12, 13, 6, 11, 2])
        self.assert_tree(self.bst, expected)

    def test_del_non_complete_node_no_left_child(self):
        self.bst.delete(10)
        expected = _get_bst([8, 3, 2, 5, 3, 4, 6, 1, 2, 12, 13, 6, 11, 2])
        self.assert_tree(self.bst, expected)


class TestRootNodeInsert(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()
        self.bst.insert(10)

    def test_root_node_key(self):
        self.assertEqual(self.bst.root.key, 10)
        self.assertEqual(self.bst.root.size, 1)

    def test_root_node_empty_children(self):
        root = self.bst.root
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)


class TestInsert(unittest.TestCase):
    def test_path_left(self):
        bst = _get_bst([10, 2])
        self.assertEqual(bst.root.left.key, 2)
        self.assertIsNone(bst.root.right)

    def test_path_right(self):
        bst = _get_bst([10, 12])
        self.assertIsNone(bst.root.left)
        self.assertEqual(bst.root.right.key, 12)

    def test_path_left_right_left(self):
        bst = _get_bst([10, 2, 12, 6, 7])
        bst.insert(4)
        self.assertEqual(bst.root.left.right.left.key, 4)

    def test_path_left_right_right(self):
        bst = _get_bst([10, 2, 12, 6, 4])
        bst.insert(7)
        self.assertEqual(bst.root.left.right.right.key, 7)

    def test_path_right_right_right(self):
        bst = _get_bst([10, 15, 12, 18, 16])
        bst.insert(24)
        self.assertEqual(bst.root.right.right.right.key, 24)

    def test_path_right_right_left(self):
        bst = _get_bst([10, 15, 12, 18, 24])
        bst.insert(16)
        self.assertEqual(bst.root.right.right.left.key, 16)

    def test_duplicate_root(self):
        bst = _get_bst([10, 10, 10, 10])
        self.assertEqual(bst.root.key, 10)
        self.assertEqual(bst.root.key_count, 4)
        self.assertIsNone(bst.root.left)
        self.assertIsNone(bst.root.right)

    def test_duplicate_leaf_node(self):
        bst = _get_bst([10, 2, 12, 5])
        bst.insert(12)
        self.assertTrue(bst.root.right.is_leaf())
        self.assertEqual(bst.root.right.key_count, 2)

    def test_duplicate_internal_complete_node(self):
        bst = _get_bst([10, 2, 12, 6, 4, 7])
        bst.insert(6)
        self.assertEqual(bst.root.left.right.key, 6)
        self.assertEqual(bst.root.left.right.key_count, 2)

    def test_duplicate_internal_non_complete_node(self):
        bst = _get_bst([10, 2, 12, 6, 4, 7])
        bst.insert(2)
        self.assertEqual(bst.root.left.key, 2)
        self.assertEqual(bst.root.left.key_count, 2)


class TestKthSmallestKey(unittest.TestCase):
    def setUp(self):
        self.bst = _get_bst([8, 3, 2, 5, 4, 6, 12, 13, 10, 11])

    def test_empty_tree_exception(self):
        bst = BinarySearchTree()
        self.assertRaises(SmallestElementIndexError, bst.kth_smallest_key, 1)

    def test_k_less_than_1_exception(self):
        self.assertRaises(Exception, self.bst.kth_smallest_key, 0)

    def test_k_less_than_root_size_exception(self):
        root = self.bst.root
        self.assertRaises(Exception, self.bst.kth_smallest_key, root.size + 1)
        left = root.left
        self.assertRaises(Exception, self.bst.kth_smallest_key, left.size + 1,
                          root=left)

    def test_smallest_element_from_root(self):
        self.assertEqual(self.bst.kth_smallest_key(1), 2)

    def test_smallest_element_from_non_root(self):
        self.assertEqual(self.bst.kth_smallest_key(3, root=self.bst.root.left),
                         4)

    def test_largest_element_from_root(self):
        self.assertEqual(self.bst.kth_smallest_key(self.bst.root.size), 13)

    def test_largest_element_from_non_root(self):
        root = self.bst.root.left
        self.assertEqual(self.bst.kth_smallest_key(root.size, root=root), 6)

    def test_path_right_left_right(self):
        self.assertEqual(self.bst.kth_smallest_key(8), 11)

    def test_path_left_right_right(self):
        self.assertEqual(self.bst.kth_smallest_key(5), 6)

    def test_leaf_node_as_smallest(self):
        self.assertEqual(self.bst.kth_smallest_key(3), 4)

    def test_internal_complete_node_as_smallest(self):
        self.assertEqual(self.bst.kth_smallest_key(4), 5)
        self.assertEqual(self.bst.kth_smallest_key(9), 12)

    def test_internal_non_complete_node_as_smallest(self):
        self.assertEqual(self.bst.kth_smallest_key(7), 10)


class TestKthSuccessor(unittest.TestCase):
    def setUp(self):
        self.bst = _get_bst([8, 3, 2, 5, 4, 6, 12, 13, 10, 11])

    def test_empty_tree_exception(self):
        bst = BinarySearchTree()
        self.assertRaises((TreeKeyError, SuccessorIndexError),
                          bst.kth_successor, 1, 1)

    def test_k_less_than_0_exception(self):
        self.assertRaises(SuccessorIndexError, self.bst.kth_successor, -1, 1)

    def test_k_greater_than_successor_count_exception(self):
        self.assertRaises(SuccessorIndexError, self.bst.kth_successor, 2, 12)
        self.assertRaises(SuccessorIndexError, self.bst.kth_successor, 4, 11)
        self.assertRaises(SuccessorIndexError, self.bst.kth_successor, 7, 6)
        self.assertRaises(SuccessorIndexError, self.bst.kth_successor, 1, 13)

    def test_k_0(self):
        self.assertEqual(self.bst.kth_successor(0, 8), 8)
        self.assertEqual(self.bst.kth_successor(0, 5), 5)
        self.assertEqual(self.bst.kth_successor(0, 10), 10)
        self.assertEqual(self.bst.kth_successor(0, 2), 2)
        self.assertEqual(self.bst.kth_successor(0, 13), 13)

    def test_parent_successor_of_leaf_node(self):
        self.assertEqual(self.bst.kth_successor(1, 2), 3)
        self.assertEqual(self.bst.kth_successor(1, 4), 5)

    def test_non_parent_successor_of_leaf_node(self):
        self.assertEqual(self.bst.kth_successor(1, 6), 8)
        self.assertEqual(self.bst.kth_successor(1, 11), 12)

    def test_successor_in_right_subtree(self):
        self.assertEqual(self.bst.kth_successor(1, 3), 4)
        self.assertEqual(self.bst.kth_successor(2, 3), 5)
        self.assertEqual(self.bst.kth_successor(3, 3), 6)
        self.assertEqual(self.bst.kth_successor(1, 10), 11)
        self.assertEqual(self.bst.kth_successor(1, 12), 13)

    def test_ancestor_successor(self):
        self.assertEqual(self.bst.kth_successor(5, 2), 8)
        self.assertEqual(self.bst.kth_successor(3, 4), 8)
        self.assertEqual(self.bst.kth_successor(2, 5), 8)
        self.assertEqual(self.bst.kth_successor(1, 6), 8)

    def test_successor_in_different_subtree(self):
        self.assertEqual(self.bst.kth_successor(6, 2), 10)
        self.assertEqual(self.bst.kth_successor(7, 3), 12)
        self.assertEqual(self.bst.kth_successor(5, 4), 11)
        self.assertEqual(self.bst.kth_successor(5, 6), 13)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.bst = _get_bst([3, 1, 0, 5, 4, 8, 9, 0, 5])

    def test_empty_tree(self):
        bst = BinarySearchTree()
        self.assertFalse(bst.search(10))

    def test_exists_in_tree_with_single_element(self):
        bst = _get_bst([10])
        self.assertTrue(bst.search(10))

    def test_not_exists_in_tree_with_single_element(self):
        bst = _get_bst([10])
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
        bst = BinarySearchTree()
        self.assertListEqual(bst.sorted_keys(), [])

    def test_tree_with_single_element(self):
        bst = _get_bst([10])
        self.assertListEqual(bst.sorted_keys(), [10])

    def test_tree_with_multiple_elements(self):
        bst = _get_bst([2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(), [1, 2, 3, 4, 5])

    def test_tree_with_multiple_elements_and_duplicates(self):
        bst = _get_bst([2, 1, 4, 5, 3, 1, 1, 6, 4])
        self.assertListEqual(bst.sorted_keys(), [1, 1, 1, 2, 3, 4, 4, 5, 6])

    def test_tree_with_all_duplicates(self):
        bst = _get_bst([2, 2, 2, 2, 2, 2, 2])
        self.assertListEqual(bst.sorted_keys(), [2, 2, 2, 2, 2, 2, 2])

    def test_at_leaf_node(self):
        bst = _get_bst([2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(bst.root.right.left), [3])

    def test_at_internal_complete_node(self):
        bst = _get_bst([2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(bst.root.right), [3, 4, 5])

    def test_at_internal_non_complete_node(self):
        bst = _get_bst([2, 1, 4, 5, 3, 6])
        self.assertListEqual(bst.sorted_keys(bst.root.right.right), [5, 6])


class TestSuccessorCount(unittest.TestCase):
    def setUp(self):
        self.bst = _get_bst([8, 3, 2, 5, 4, 6, 12, 13, 10, 11])

    def test_key_not_in_tree(self):
        self.assertRaises(TreeKeyError, self.bst.successor_count, 99)

    def test_successor_count_for_all_keys(self):
        keys = self.bst.sorted_keys()
        for key, count in zip(keys, xrange(len(keys) - 1, -1, -1)):
            self.assertEqual(self.bst.successor_count(key), count)


def _get_bst(keys):
    """Return a BST after inserting the input keys."""

    bst = BinarySearchTree()
    for key in keys:
        bst.insert(key)
    return bst


if __name__ == '__main__':
    unittest.main()
