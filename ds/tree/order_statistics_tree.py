# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.order_statistics_tree
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Order Statistics Tree data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

import binary_search_tree


class Node(binary_search_tree.Node):
    def __init__(self, key):
        super(Node, self).__init__(key)
        self._size = 1

    @property
    def size(self):
        return self._size

    @property
    def left_size(self):
        return self.left._size if self.left else 0

    @property
    def right_size(self):
        return self.right._size if self.right else 0


class OrderStatisticsTree(binary_search_tree.BinarySearchTree):
    def __init__(self):
        super(OrderStatisticsTree, self).__init__(Node)

    def kth_smallest_key(self, k, root=None):
        """Return the kth smallest element in the tree.

        :param root: (optional) the root node to start the search from.
        """

        if not root:
            root = self.root

        max_index = 0 if not root else root.size
        if not 1 <= k <= max_index:
            raise IndexError('Rank must be a positive value greater than: '
                             '{0}'.format(max_index))

        while True:
            left_subtree_size = root.left_size

            if k <= left_subtree_size:
                # Smallest element lies in the left subtree
                root = root.left
            else:
                k -= (left_subtree_size + root.count)
                if k <= 0:
                    # Smallest element is the root
                    return root.key
                else:
                    # Smallest element lies in the right subtree
                    root = root.right

    def kth_successor(self, k, key):
        """Return the kth-successor of a key."""

        if k < 0 or k > self.successor_count(key):
            raise IndexError('Invalid successor index: {0}'.format(k))

        node = self._search_node(key)

        while True:
            if k == 0:
                return node.key
            else:
                if k > node.right_size:
                    node = self.successor_ancestor(node)
                    k = k - node.right_size - 1
                else:
                    return self.kth_smallest_key(k, node.right)

    def _update_node(self, node):
        """Updates the attributes of a tree node."""
        while node:
            pass