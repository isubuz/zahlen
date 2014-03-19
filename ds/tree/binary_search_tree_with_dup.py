# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.binary_search_tree_with_dup
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements a Binary Search Tree with duplicate or repeated
    keys.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

import binary_search_tree


class Node(binary_search_tree.Node):
    def __init__(self, key):
        super(Node, self).__init__(key)
        self._count = 1

    def __str__(self):
        pass


class BinarySearchTreeDupKeys(binary_search_tree.BinarySearchTree):
    """Represents a Binary Search Tree with duplicate keys."""

    def insert(self, key):
        """Inserts ``key`` in the tree."""
        if not self._root:
            self._root = self._Node(key)
        else:
            node = self._root
            parent = None

            while node:
                parent = node

                if key == node.key:
                    break

                node = node.left if key < node.key else node.right

            if key == parent.key:
                parent._count += 1
            elif key < parent.key:
                parent.left = self._Node(key)
            else:
                parent.right = self._Node(key)

            self._bubble_up_node_attrs(parent)

    def delete(self, key, delete_all=False):
        """Deletes key ``key`` from the tree.

        :param delete_all: If true, deletes all the duplicate keys. Else deletes
            only a single occurrence of the key.
        """
        node = self._search_node(key, silent=False)

        if not delete_all and node._count > 1:
            node._count -= 1
            self._bubble_up_node_attrs(node)
        elif node.is_leaf():
            self._delete_leaf_node(node)
        else:
            self._delete_internal_node(node)