# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.bst.tree
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from .node import Node


class TreeKeyError(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'Key: {0} not found in tree.'.format(self.key)


class SmallestElementIndexError(Exception):
    def __init__(self, max_index):
        self.index = max_index

    def __str__(self):
        return 'Smallest element index must be a positive value less than {0}'\
            .format(self.index)


class SuccessorIndexError(Exception):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return 'Invalid successor index: {0}'.format(self.index)


class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    def delete(self, key):
        """Delete key ``key`` from the tree."""

        node = self._search_node(key)
        if not node:
            raise TreeKeyError(key)
        elif node.is_leaf():
            self._delete_leaf_node(node)
        else:
            self._delete_internal_node(node)

    def insert(self, key):
        """Insert key ``key`` in the tree."""

        if not self.root:
            self.root = Node(key)
        else:
            node = self.root
            parent = None

            while node:
                parent = node
                parent.size += 1

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

    def kth_smallest_key(self, k, root=None):
        """Return the kth smallest element in the tree.

        :param root: (optional) the root node to start the search from.
        """

        if not root:
            root = self.root

        max_index = 0 if not root else root.size
        if not 1 <= k <= max_index:
            raise SmallestElementIndexError(max_index)

        if root.left:
            left_subtree_size_and_root = root.left.size + 1
        else:
            left_subtree_size_and_root = 1

        if left_subtree_size_and_root == k:
            return root.key
        elif left_subtree_size_and_root > k:
            return self.kth_smallest_key(k, root.left)
        else:
            return self.kth_smallest_key(k - left_subtree_size_and_root,
                                         root.right)

    def kth_successor(self, k, key):
        """Return the kth-successor of a key."""

        if k < 0 or k > self.successor_count(key):
            raise SuccessorIndexError(k)

        node = self._search_node(key)

        while True:
            if k == 0:
                return node.key
            else:
                right_subtree_size = node.right.size if node.right else 0
                if k > right_subtree_size:
                    node = self.successor_ancestor(node)
                    k = k - right_subtree_size - 1
                else:
                    return self.kth_smallest_key(k, node.right)

    def search(self, key):
        """Returns true if key `key` exists in the tree, else False."""

        return self._search_node(key) is not None

    def sorted_keys(self, node=None):
        """Returns a sorted list of the keys in the tree.

        Sorting is done by an inorder traversal of the tree starting from the
        node ``node``. If start node is not passed, the traversal starts from
        the root.
        """

        keys = []
        self._inorder_walk(node or self.root, keys)
        return keys

    def successor_count(self, key):
        """Return the number of successors of a key."""

        node = self._search_node(key)
        if not node:
            raise TreeKeyError(key)

        count = 0
        while node:
            # Account for the successor in the right subtree
            if node.right and not node.key < key:
                count += node.right.size

            # Account for the parent
            if node.parent and not node.parent.key < key:
                count += 1
            node = node.parent

        return count

    def _delete_leaf_node(self, node):
        """Delete a leaf node."""

        if node.parent:
            node.parent.add_child(node)
        else:
            self.root = None
        del node

    def _delete_internal_node(self, node):
        """Delete an internal node with 1 or 2 children."""

        if not node.left or not node.right:
            # For an incomplete internal node, replace the node with its left or
            # right child and update the parent if any.
            child = node.left if not node.left else node.right
            parent = node.parent
            if parent:
                parent.add_child(child)
            else:
                self.root = child
        else:
            # For an complete internal node, replace node's key by inorder
            # successor's key and remove the successor.
            successor = self.successor(node)
            self.delete(successor)
            node.key = successor.key()

    def _inorder_walk(self, node, keys):

        if node:
            self._inorder_walk(node.left, keys)

            # Handle duplicate keys
            for _ in xrange(node.key_count):
                keys.append(node.key)
            self._inorder_walk(node.right, keys)

    def _search_node(self, key):
        """Return the node with key ``key`` if it exists, else return None."""

        node = self.root
        while node:
            if node.key == key:
                break
            else:
                node = node.left if key < node.key else node.right
        return node

    @staticmethod
    def successor_ancestor(node):
        """Return the successor ancestor of a node."""

        key = node.key
        node = node.parent
        while node:
            if node.key < key:
                node = node.parent
            else:
                break
        return node
