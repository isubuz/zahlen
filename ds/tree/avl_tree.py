# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.avl
    ~~~~~~~~~~~~~~~~~~

    This module implements the AVL tree data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

import binary_search_tree


class Node(binary_search_tree.Node):
    """A node in an AVL tree.

    An AVL tree node is same as a BST node but maintains an additional property
    ``height``. The height of a node is the longest path from the node to a
    leaf node.
    """

    def __init__(self, key):
        super(Node, self).__init__(key)
        self.height = 0

    @property
    def left_height(self):
        """Returns the height of the left child."""
        return self.left.height if self.left else -1

    @property
    def right_height(self):
        """Returns the height of the right child."""
        return self.right.height if self.right else -1

    def is_heavy(self):
        """Returns true if the difference of height between the left and right
        children is greater than 1.
        """
        return abs(self.left_height - self.right_height) > 1

    def is_left_heavy(self, diff=1):
        """Returns true if left child's height minus right child's height is
        greater than ``diff``.
        """
        return self.left_height - self.right_height > diff

    def is_right_heavy(self, diff=1):
        """Returns true if right child's height minus left child's height is
        greater than ``diff``.
        """
        return self.right_height - self.left_height > diff

    def add_child(self, child):
        """Add a left or a right child based on the child's key."""
        if child.key < self.key:
            self.left = child
        else:
            self.right = child

    def update(self):
        """Recalculate and updates the height of a node."""
        self.height = 1 + max(self.left_height, self.right_height)


class AVLTree(binary_search_tree.BinarySearchTree):
    """Represents an AVL tree which is a binary search tree."""

    def is_balanced(self, node=None):
        """Returns true if the tree is balanced.

        The tree is balanced if every node in the tree is non-heavy i.e. for
        every node the difference in height of its children is not greater
        than 1.

        :param node: Root node. This can be root of the AVL tree or the root of
            a subtree in the AVL tree.
        """
        if not node:
            node = self.root

        is_balanced = not node.is_heavy()

        # If parent is balanced, check left child
        if is_balanced and node.left:
            is_balanced = self.is_balanced(node.left)

        # If parent and left child are balanced, check right child
        if is_balanced and node.right:
            is_balanced = self.is_balanced(node.right)

        return is_balanced

    def _balance(self, node):
        """Balances a node and all its ancestors."""
        parent = node.parent

        if node.is_left_heavy():
            # If left child is right heavy, first make it left heavy.
            if node.left.is_right_heavy(diff=0):
                self._rotate_left(node.left, node.left.right)

            self._rotate_right(node, node.left)
        elif node.is_right_heavy():
            # If right child is left heavy, first make it right heavy.
            if node.right.is_left_heavy(diff=0):
                self._rotate_right(node.right, node.right.left)

            self._rotate_left(node, node.right)

        if parent:
            self._balance(parent)

    def _rotate_left(self, node, heavy_child):
        """Rotates ``node`` to make it the left child of ``heavy_child``."""
        parent = node.parent

        node.right = heavy_child.left
        node.update()

        heavy_child.parent = parent
        heavy_child.left = node
        heavy_child.update()

        # Update parent pointers (if any)
        if parent:
            parent.add_child(heavy_child)
        else:
            self.root = heavy_child

    def _rotate_right(self, node, heavy_child):
        """Rotates ``node`` to make it the right child of ``heavy_child.``"""
        parent = node.parent

        node.left = heavy_child.right
        node.update()

        heavy_child.parent = parent
        heavy_child.right = node
        heavy_child.update()

        # Update parent pointers (if any)
        if parent:
            parent.add_child(heavy_child)
        else:
            self.root = heavy_child

    def _bubble_up_node_attrs(self, node):
        """Updates node attributes and bubbles up the updated values upto the
        root.
        """
        while node:
            # Update node height and balance
            node.update()
            self._balance(node)

            node = node.parent