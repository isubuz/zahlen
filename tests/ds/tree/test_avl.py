# -*- coding: utf-8 -*-

"""
    Test case module for zahlen.ds.tree.avl.AVLTree

    TODO (isubuz)
    - Write test cases for AVLTestCase

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque
from zahlen.ds.tree.avl2 import AVLTree

import unittest


class AVLTestCase(unittest.TestCase):
    def assert_tree(self, actual, expected):
        """Assert if two tree are equal."""

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
            self.assertEqual(actual.height, expected.height)

            for act, exp in [(actual.left, expected.left),
                             (actual.right, expected.right),
                             (actual.parent, expected.parent)]:
                if exp:
                    self.assertIsNotNone(act)
                    self.assertEqual(act.key, exp.key)
                else:
                    self.assertIsNone(act)


class TestInsert(AVLTestCase):
    def test_rotate_left_heavy_child_without_left_child(self):
        actual = _get_avl([9, 10, 11])
        expected = _get_balanced_bst([10, 9, 11])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_rotate_left_heavy_child_with_left_child(self):
        actual = _get_avl([10, 9, 20, 15, 25, 26])
        expected = _get_balanced_bst([20, 10, 25, 9, 15, 26])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_rotate_right_rotate_left_1(self):
        actual = _get_avl([10, 6, 20, 15, 25, 17])
        expected = _get_balanced_bst([15, 10, 20, 6, 17, 25])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_rotate_right_rotate_left_2(self):
        actual = _get_avl([10, 6, 20, 15, 25, 12])
        expected = _get_balanced_bst([15, 10, 20, 6, 12, 25])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_rotate_right_heavy_child_without_right_child(self):
        actual = _get_avl([8, 7, 6])
        expected = _get_balanced_bst([7, 6, 8])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_rotate_right_heavy_child_with_right_child(self):
        actual = _get_avl([20, 10, 25, 8, 15, 6])
        expected = _get_balanced_bst([10, 8, 20, 6, 15, 25])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_rotate_left_rotate_right_1(self):
        actual = _get_avl([20, 10, 25, 8, 15, 12])
        expected = _get_balanced_bst([15, 10, 20, 8, 12, 25])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_rotate_left_rotate_right_2(self):
        actual = _get_avl([20, 10, 25, 8, 15, 17])
        expected = _get_balanced_bst([15, 10, 20, 8, 17, 25])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())


class TestDelete(AVLTestCase):
    def test_del_leaf_node_rotate_left(self):
        actual = _get_avl([16, 10, 25, 6, 18, 28, 17, 27, 29])
        actual.delete(6)
        expected = _get_balanced_bst([25, 16, 28, 10, 18, 27, 29, 17])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_del_internal_non_complete_node_rotate_left(self):
        actual = _get_avl([16, 10, 25, 6, 18, 28, 17, 27, 29])
        actual.delete(10)
        expected = _get_balanced_bst([25, 16, 28, 6, 18, 27, 29, 17])
        self.assert_tree(actual, expected)
        self.assertTrue(actual.is_balanced())

    def test_del_internal_complete_node_rotate_left(self):
        actual = _get_avl([16, 10, 25, 6, 14, 18, 28, 15, 17, 27, 29, 30])
        actual.delete(10)
        expected = _get_balanced_bst([25, 16, 28, 14, 18, 27, 29, 6, 15, 17,
                                      30])
        self.assert_tree(actual, expected)


def _get_avl(keys):
    """Return an AVL tree by inserting the keys."""

    avl = AVLTree()
    for key in keys:
        avl.insert(key)
    return avl


def _get_balanced_bst(keys):
    """Return a balanced binary search tree.

    A subclass of AVLTree is returned to assist in testing an actual AVL tree
    with an expected AVL tree. Balancing is not required in the subclass tree
    because the keys are inserted in an order such the tree is always balanced
    on insertion.
    The caller must take care that the keys are correctly ordered.
    """

    class BalancedAVL(AVLTree):
        def _update(self, node):
            """Overridden update() which does not balance the tree."""

            while node:
                node.update()
                node = node.parent

    avl = BalancedAVL()
    for key in keys:
        avl.insert(key)
    return avl


if __name__ == '__main__':
    unittest.main()