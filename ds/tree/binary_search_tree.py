# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.bst
    ~~~~~~~~~~~~~~~~~~

    This module implements the Binary Search Tree data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""


class Node(object):
    """A node in a binary search tree.

    :param key: value stored in the node
    """

    def __init__(self, key):
        self._left = None
        self._right = None
        self.parent = None
        self.key = key

    def __str__(self):
        parent_key = self.parent.key if self.parent else -1
        return 'key:{0},parent:{1}'.format(self.key, parent_key)

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node
        if node:
            node.parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        if node:
            node.parent = self

    def is_leaf(self):
        """Returns true if node is a leaf node."""
        return self.left is None and self.right is None


class BinarySearchTree(object):
    """Represents the Binary Search Tree data structure."""

    def __init__(self, node_type):
        self.root = None
        self._Node = node_type

    def __str__(self):
        return self.draw(self.root)

    def insert(self, key):
        """Inserts key ``key`` in the tree."""

        if not self.root:
            self.root = self._Node(key)
        else:
            node = self.root
            parent = None

            while node:
                parent = node
                node = node.left if key < node.key else node.right

            if key < parent.key:
                parent.left = self._Node(key)
            else:
                parent.right = self._Node(key)
            self._bubble_up_node_attrs(parent)

    def delete(self, key):
        """Deletes key ``key`` from the tree."""
        node = self._search_node(key, silent=False)
        self._delete_node(node)

    def search(self, key):
        """Returns True if key `key` exists in the tree, else False."""
        return self._search_node(key) is not None

    def sorted_keys(self):
        """Returns a sorted list of the keys in the tree."""
        keys = []
        self.inorder_walk(self.root, keys)
        return keys

    def inorder_walk(self, node, keys):
        if node:
            self.inorder_walk(node.left, keys)
            keys.append(node.key)
            self.inorder_walk(node.right, keys)

    def draw(self, node, depth=0):
        """Prints a subtree rooted at a node at certain depth."""
        key = node.key if node else 'NULL'

        if depth:
            prefix = '|   ' * depth + '|---'
        else:
            prefix = ''

        node_str = prefix + '(' + str(key) + ')\n'

        if node and not node.is_leaf():
            node_str += self.draw(node.right, depth + 1)
            node_str += self.draw(node.left, depth + 1)

        return node_str

    def _delete_node(self, node):
        """Deletes a leaf node or an internal node."""
        if node.is_leaf():
            self._delete_leaf_node(node)
        else:
            self._delete_internal_node(node)

    def _delete_leaf_node(self, node):
        """Deletes a leaf node."""
        parent = node.parent
        if parent:
            if node.key < parent.key:
                parent.left = None
            else:
                parent.right = None
            self._bubble_up_node_attrs(parent)
        else:
            self.root = None
        del node

    def _delete_internal_node(self, node):
        """Deletes an internal node with 1 or 2 children."""
        if not node.left or not node.right:
            # For an incomplete internal node, replace the node with its left or
            # right child and update the parent if any.
            parent = node.parent
            child = node.left if node.left else node.right
            child.parent = parent

            if parent:
                if node.key < parent.key:
                    parent.left = child
                else:
                    parent.right = child
                self._bubble_up_node_attrs(parent)
            else:
                self.root = child
        else:
            # For an complete internal node, replace node's key by inorder
            # successor's key and remove the successor.
            successor = node.right
            while successor.left:
                successor = successor.left
            self._delete_node(successor)
            node.key = successor.key

    def _search_node(self, key, silent=True):
        """Return the node with key ``key`` if it exists, else return None.

        :param silent: If False, raises an exception if ``key`` does not exist
            in the tree.
        """
        node = self.root
        while node:
            if node.key == key:
                break
            else:
                node = node.left if key < node.key else node.right

        if not node and not silent:
            raise KeyError('Key: {0} not found in tree'.format(key))

        return node

    def _bubble_up_node_attrs(self, node):
        """Updates node attributes and bubbles up the updated values up to the
        root.

        This method is simply a hook for the sub-classes of BinarySearchTree to
        update the attributes of a node (e.g. height for an AVL tree) when a
        node is inserted or deleted. Sub-classes can override this method to
        perform necessary after-insert of after-delete actions.
        """
        pass