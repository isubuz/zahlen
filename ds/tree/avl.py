# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.avl
    ~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

import bst


class Node(bst.Node):
    def __init__(self, key):
        """

        height: No. of nodes in the longest path from the node to a leaf node.
        """
        super(Node, self).__init__(key)
        self.height = 0

    @property
    def left_height(self):
        return self.left.height if self.left else -1

    @property
    def right_height(self):
        return self.right.height if self.right else -1

    def is_heavy(self):
        return abs(self.left_height - self.right_height) > 1

    def is_left_heavy(self, diff=1):
        return (self.left_height - self.right_height) > diff

    def is_right_heavy(self, diff=1):
        return (self.right_height - self.left_height) > diff

    def update(self):
        """Update the size and height of the node."""

        self.size = 1 + self.left_size + self.right_size
        self.height = 1 + max(self.left_height, self.right_height)


class AVLTree(bst.BinarySearchTree):

    @staticmethod
    def create_node(key):
        return Node(key)

    def is_balanced(self, node=None):
        """Return true if the AVL tree is balanced.

        Recursively check if node and its children are heavy nodes.
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
        """Rotate to make the node the left child of its ``heavy_child``."""

        parent = node.parent

        node.right = heavy_child.left
        node.update()

        heavy_child.parent = parent
        heavy_child.left = node
        heavy_child.update()

        if parent:
            parent.add_child(heavy_child)
        else:
            self.root = heavy_child

    def _rotate_right(self, node, heavy_child):
        """Rotate to make the node the right child of its ``heavy_child.``"""

        parent = node.parent

        node.left = heavy_child.right
        node.update()

        heavy_child.parent = parent
        heavy_child.right = node
        heavy_child.update()

        if parent:
            parent.add_child(heavy_child)
        else:
            self.root = heavy_child

    def _update(self, node):
        while node:
            node.update()

            # Updating the height may make the subtree rooted at ``node``
            # unbalanced. Hence balance.
            self._balance(node)

            node = node.parent
