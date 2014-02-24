# -*- coding: utf-8 -*-

"""
    Test case module for zahlen.ds.tree.bst

    TODO (isubuz)
    - TestBSTStructure is subclassed. However subclassing runs the test cases in
    the base class multiple times. This should not happen.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from zahlen.ds.tree.bst.tree import BinarySearchTree, TreeKeyError, \
    SmallestElementIndexError, SuccessorIndexError

import unittest


class TestBSTStructure(unittest.TestCase):
    """This class verifies the structure the BST i.e. verifies the leaf nodes
    and the complete and non-complete internal nodes.
    This provides a BST which is used in other test classes. Test cases which
    use the BST provided by this class can safely assume the correctness of the
    BST structure.
    """

    def setUp(self):
        self.bst = _get_bst([8, 3, 2, 5, 4, 6, 12, 13, 10, 11])

    def test_leaf_nodes(self):
        root = self.bst.root
        self.assertTrue(root.left.left.is_leaf())
        self.assertTrue(root.left.right.left.is_leaf())
        self.assertTrue(root.left.right.right.is_leaf())
        self.assertTrue(root.right.left.right.is_leaf())
        self.assertTrue(root.right.right.is_leaf())

    def test_internal_complete_nodes(self):
        root = self.bst.root
        self.assertTrue(root.is_complete())
        self.assertTrue(root.left.is_complete())
        self.assertTrue(root.left.right.is_complete())
        self.assertTrue(root.right.is_complete())

    def test_internal_non_complete_node(self):
        node = self.bst.root.right.left
        self.assertTrue(not node.is_leaf() and not node.is_complete())


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
        bst = BinarySearchTree()
        _insert(bst, [10, 2])
        self.assertEqual(bst.root.left.key, 2)
        self.assertIsNone(bst.root.right)

    def test_path_right(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 12])
        self.assertIsNone(bst.root.left)
        self.assertEqual(bst.root.right.key, 12)

    def test_path_left_right_left(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 7])
        bst.insert(4)
        self.assertEqual(bst.root.left.right.left.key, 4)

    def test_path_left_right_right(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 4])
        bst.insert(7)
        self.assertEqual(bst.root.left.right.right.key, 7)

    def test_path_right_right_right(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 15, 12, 18, 16])
        bst.insert(24)
        self.assertEqual(bst.root.right.right.right.key, 24)

    def test_path_right_right_left(self):
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

    def test_duplicate_leaf_node(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 5])
        bst.insert(12)
        self.assertTrue(bst.root.right.is_leaf())
        self.assertEqual(bst.root.right.key_count, 2)

    def test_duplicate_internal_complete_node(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 4, 7])
        bst.insert(6)
        self.assertEqual(bst.root.left.right.key, 6)
        self.assertEqual(bst.root.left.right.key_count, 2)

    def test_duplicate_internal_non_complete_node(self):
        bst = BinarySearchTree()
        _insert(bst, [10, 2, 12, 6, 4, 7])
        bst.insert(2)
        self.assertEqual(bst.root.left.key, 2)
        self.assertEqual(bst.root.left.key_count, 2)


class TestNodeSizeAfterInsert(TestBSTStructure):
    def test_tree_with_single_node(self):
        bst = _get_bst([10])
        self.assertEqual(bst.root.size, 1)

    def test_leaf_node(self):
        node = self.bst.root.left.right.left
        self.assertEqual(node.size, 1)

    def test_internal_complete_node_root(self):
        self.assertEqual(self.bst.root.size, 10)

    def test_internal_complete_node(self):
        node = self.bst.root.right
        self.assertEqual(node.size, 4)

    def test_internal_non_complete_node(self):
        node = self.bst.root.right.left
        self.assertEqual(node.size, 2)


class TestKthSmallestKey(TestBSTStructure):

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


class TestKthSuccessor(TestBSTStructure):
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
        bst = BinarySearchTree()
        bst.insert(10)
        self.assertListEqual(bst.sorted_keys(), [10])

    def test_tree_with_multiple_elements(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(), [1, 2, 3, 4, 5])

    def test_tree_with_multiple_elements_and_duplicates(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3, 1, 1, 6, 4])
        self.assertListEqual(bst.sorted_keys(), [1, 1, 1, 2, 3, 4, 4, 5, 6])

    def test_tree_with_all_duplicates(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 2, 2, 2, 2, 2, 2])
        self.assertListEqual(bst.sorted_keys(), [2, 2, 2, 2, 2, 2, 2])

    def test_at_leaf_node(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(bst.root.right.left), [3])

    def test_at_internal_complete_node(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3])
        self.assertListEqual(bst.sorted_keys(bst.root.right), [3, 4, 5])

    def test_at_internal_non_complete_node(self):
        bst = BinarySearchTree()
        _insert(bst, [2, 1, 4, 5, 3, 6])
        self.assertListEqual(bst.sorted_keys(bst.root.right.right), [5, 6])


class TestSuccessorCount(TestBSTStructure):
    def test_key_not_in_tree(self):
        self.assertRaises(TreeKeyError, self.bst.successor_count, 99)

    def test_successor_count_for_all_keys(self):
        keys = self.bst.sorted_keys()
        for key, count in zip(keys, xrange(len(keys) - 1, -1, -1)):
            self.assertEqual(self.bst.successor_count(key), count)


def _get_bst(keys):
    bst = BinarySearchTree()
    for key in keys:
        bst.insert(key)
    return bst


def _insert(bst, keys):
    for key in keys:
        bst.insert(key)

if __name__ == '__main__':
    unittest.main()
