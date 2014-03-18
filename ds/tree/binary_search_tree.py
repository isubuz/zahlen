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

    This implementation of a BST supports duplicate or repeated keys in the
    tree. For

    Attributes:
        key:
        count:

    .. note::
        Every node has an attribute ``count``. This is used to support a
        binary search tree with duplicate or repeated keys. For every duplicate
        key, the BST does not contain a duplicate node. Instead the occurrence
        count is saved in ``count``. This attribute and related code can be
        removed if the BST is known to contain unique keys only.

        Every node has an attribute ``weight``. This refers to the total no. of
        nodes in the subtree with the node as the root. E.g. For a leaf node,
        the weight is always 1. For a node with two leaf node as children, the
        weight is 3. This attribute is used to implement methods such as
        kth_successor(), kth_smallest_key(). If these methods are not required,
        this attribute and related code can be removed.
    """

    def __init__(self, key):
        self._left = None
        self._right = None

        self.key = key
        self.count = 1
        self.parent = None

    def __str__(self):
        parent_key = self.parent.key if self.parent else -1
        return 'key:{0},parent:{1},count:{3}'.format(
            self.key, parent_key, self.count)

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

    def add_child(self, child):
        """Add a left or a right child based on the child's key."""

        if child.key < self.key:
            self.left = child
        else:
            self.right = child

    def is_complete(self):
        """Return true if node is a complete node.

        A complete node is an internal node which has non-None left and right
        children.
        """

        return self.left and self.right

    def is_leaf(self):
        """Return true if node is a leaf node."""

        return self.left is None and self.right is None


class BinarySearchTree(object):
    """Represents the Binary Search Tree data structure."""

    def __init__(self, node_type):
        self.root = None
        self._Node = node_type

    def __str__(self):
        return self.draw(self.root)

    def delete(self, key, all=False):
        """Delete key ``key`` from the tree.

        :all If true all occurrences of the key will be deleted.
        """

        node = self._search_node(key)

        if not node:
            raise TreeKeyError(key)

        if not all and node.count > 1:
            node.count -= 1
            self._update(node)
        elif node.is_leaf():
            self._delete_leaf_node(node)
        else:
            self._delete_internal_node(node)

    def draw(self, node, depth=0):
        """Print a subtree rooted at a node at certain depth."""

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

    def insert(self, key):
        """Insert key ``key`` in the tree."""

        if not self.root:
            self.root = self._Node(key)
        else:
            node = self.root
            parent = None

            while node:
                parent = node

                if key == node.key:
                    break

                node = node.left if key < node.key else node.right

            if key == parent.key:
                parent.count += 1
            elif key < parent.key:
                parent.left = self._Node(key)
            else:
                parent.right = self._Node(key)

            self._update(parent)

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

    def successor_count(self, key):
        """Return the number of successors of a key."""

        node = self._search_node(key)
        if not node:
            raise KeyError('Invalid key: {0}'.format(key))

        count = 0
        while node:
            # Account for the successor in the right subtree
            if node.right and not node.key < key:
                count += node.right.weight

            # Account for the parent
            if node.parent and not node.parent.key < key:
                count += 1
            node = node.parent

        return count

    def _delete_leaf_node(self, node):
        """Delete a leaf node."""

        parent = node.parent
        if parent:
            if node.key < parent.key:
                parent.left = None
            else:
                parent.right = None
            self._update(parent)
        else:
            self.root = None
        del node

    def _delete_internal_node(self, node):
        """Delete an internal node with 1 or 2 children."""

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
            else:
                self.root = child
            self._update(parent)
        else:
            # For an complete internal node, replace node's key by inorder
            # successor's key and remove the successor.
            # TODO (isubuz) Avoid calling search_node() again. kth_successor()
            # and delete with call search_node() again.
            successor = self._search_node(self.kth_successor(1, node.key))
            key = successor.key
            count = successor.count
            self.delete(key, all=True)
            node.key = key
            node.count = count
            self._update(node)

    def _inorder_walk(self, node, keys):

        if node:
            self._inorder_walk(node.left, keys)

            # Handle duplicate keys
            for _ in xrange(node.count):
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

    def _update(self, node):
        """Update node attributes.

        This method should be called when deleting or inserting a node in the
        tree.
        """

        while node:
            node.weight = node.count + node.right_weight + node.left_weight
            node = node.parent
