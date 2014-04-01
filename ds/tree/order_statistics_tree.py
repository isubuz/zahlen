# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.order_statistics_tree
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Order Statistics Tree data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

import avl_tree


class Node(avl_tree.Node):
    """A node in a order statistics tree.

    An order statistics tree is a binary tree. This implementation of the Order
    statistics tree is also a AVL tree. A node in a Order statistics tree
    maintains an additional attribute ``weight``. The weight of a node is the
    total number of nodes in the subtree with the node as the root. E.g. A
    leaf node has weight 1. A node with 2 leaf nodes as children has weight 3.
    """

    def __init__(self, key):
        super(Node, self).__init__(key)
        self.weight = 1

    @property
    def left_weight(self):
        return self.left.weight if self.left else 0

    @property
    def right_weight(self):
        return self.right.weight if self.right else 0

    def update(self):
        """Recalculates and updates the size of a node."""
        super(Node, self).update()
        self.weight = 1 + self.left_weight + self.right_weight


class OrderStatisticsTree(avl_tree.AVLTree):
    """Implements an Order statistics tree which is also an AVL tree.

    The underlying tree can also be implemented as a simple binary tree
    ``BinarySearchTree`` or a binary tree with duplicates
    ``BinarySearchTreeDupKeys``
    """

    def kth_smallest_key(self, k, root=None):
        """Returns the kth smallest element in the tree.

        :param root: (optional) the root node to start the search from.
        """
        if not root:
            root = self.root

        if not root:
            raise Exception('Tree is empty!')

        if not 1 <= k <= root.weight:
            raise IndexError('Rank must be a positive value less than: '
                             '{0}'.format(root.weight))

        while True:
            left_subtree_weight = root.left_weight
            if k <= left_subtree_weight:
                root = root.left        # Smallest element in the left subtree
            else:
                k -= (left_subtree_weight + 1)  # 1 is for the root element
                if k == 0:
                    return root.key     # Smallest element is the root
                else:
                    root = root.right   # Smallest element in the right subtree

    def kth_successor(self, k, key):
        """Returns the kth-successor of a key."""
        if k < 0:
            raise IndexError('Successor index must be greater than 0')
        if not self.root:
            raise Exception('Tree is empty!')

        node = self._search_node(key, silent=False)

        while True:
            if k == 0:
                return node.key
            else:
                if k > node.right_weight:
                    k -= (node.right_weight + 1)

                    # Go to the ancestor node
                    while node.parent:
                        node = node.parent
                        if node.key > key:
                            break
                    if node.key < key:
                        raise IndexError('Invalid successor index: {0}'
                                         .format(k))
                else:
                    return self.kth_smallest_key(k, node.right)