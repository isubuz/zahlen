# -*- coding: utf-8 -*-

"""

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from zahlen.ds.tree.bst.node import Node


class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert a new node with key ``key``."""

        if not self.root:
            self.root = Node(key)
        else:
            node = self.root
            parent = None

            while node:
                parent = node

                # If key already in the tree, increment key count for the node
                # and return. A new node is not inserted.
                if key == node.key:
                    node.key_count += 1
                    return

                node = node.left if key < node.key else node.right

            if key < parent.key:
                parent.left = Node(key)
            else:
                parent.right = Node(key)

    def search(self, key):
        """Returns true if key `key` exists in the tree, else False."""

        node = self.root
        while node:
            if node.key == key:
                return True
            else:
                node = node.left if key < node.key else node.right

        return False

    def sorted_keys(self, node=None):
        """Returns a sorted list of the keys in the tree.

        Sorting is done by an inorder traversal of the tree starting from the
        node ``node``. If start node is not passed, the traversal starts from
        the root.
        """

        keys = []
        self._inorder_walk(node or self.root, keys)
        return keys

    def _inorder_walk(self, node, keys):

        if node:
            self._inorder_walk(node.left, keys)

            # Handle duplicate keys
            for _ in xrange(node.key_count):
                keys.append(node.key)
            self._inorder_walk(node.right, keys)
