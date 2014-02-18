# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.avl
    ~~~~~~~~~~~~~~~~~~

    This module implements the AVL tree data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""


class _Node(object):
    def __init__(self, key=None, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        parent_key = self.parent.key if self.parent else '-1'
        return '{0}:{1}:{2}:{3}'.format(self.key, parent_key, self.size,
                                        self.height)

    @property
    def height(self):
        h = 1 + max(self.left_height, self.right_height)
        return h

    @property
    def left_height(self):
        return 0 if not self.left else self.left.height

    @property
    def left_size(self):
        return 0 if not self.left else self.left.size + 1

    @property
    def right_height(self):
        return 0 if not self.right else self.right.height

    @property
    def right_size(self):
        return 0 if not self.right else self.right.size + 1

    @property
    def size(self):
        return self.left_size + self.right_size

    def is_left_heavy(self, diff=1):
        return (self.left_height - self.right_height) > diff

    def is_right_heavy(self, diff=1):
        return (self.right_height - self.left_height) > diff

    def is_leaf(self):
        return not self.left and not self.right

    def is_left_child(self):
        return not self.is_root() and self.key < self.parent.key

    def is_right_child(self):
        return not self.is_root() and not self.is_left_child()

    def is_root(self):
        return self.parent is None


class AVLTree(object):
    def __init__(self):
        self._root = None

    def __str__(self):
        return bst_to_str(self._root)

    def delete(self, key):
        pass

    def insert(self, key):
        """Insert a node with key ``key``."""

        if self._root is None:
            self._root = _Node(key)
            return

        node = self._root
        while True:
            if key < node.key:
                if not node.left:
                    node.left = _Node(key, parent=node)
                    self._update_height(node)
                    break
                else:
                    node = node.left
            else:
                if not node.right:
                    node.right = _Node(key, parent=node)
                    self._update_height(node)
                    break
                else:
                    node = node.right

    def kth_successor(self, k, node=None):
        """Return the kth-successor."""

        if not node:
            node = self._root

        if k < 1 or (node.key + k) > self._root.size:
            print 'Invalid k:{0}'.format(k)     # Or throw error
            return

        if node.right_size >= k:
            return self.kth_smallest_element(k, node.right)
        elif node.right_size + 1 == k:
            return node.parent.key
        else:
            return self.kth_successor(k - node.right_size - 1, node.parent)

    def kth_smallest_element(self, k, node=None):
        """Return the kth smallest element in the tree."""

        if not node:
            node = self._root

        if k < 1 or k > node.size + 1:
            print 'Invalid k:{0}'.format(k)     # Or throw error
            return

        if node.left_size + 1 == k:
            return node.key
        elif node.left_size + 1 > k:
            return self.kth_smallest_element(k, node.left)
        else:
            return self.kth_smallest_element(k - node.left_size - 1, node.right)

    def sort(self):
        pass

    def search(self, key):
        """Find the node with key ``key``."""
        node = self._root
        while node:
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def _balance(self, node):
        if node.is_left_heavy():
            # If left child is right-heavy, first convert it to left-heavy.
            if node.left.is_right_heavy(diff=0):
                self._rotate_left(node.left, node.left.right)
            self._rotate_right(node, node.left)
        elif node.is_right_heavy():
            # If right child is left-heavy, first convert it to right-heavy.
            if node.right.is_left_heavy(diff=0):
                self._rotate_right(node.right, node.right.left)
            self._rotate_left(node, node.right)

    def _update_height(self, node):
        parent = node.parent
        self._balance(node)
        if parent:
            self._update_height(parent)

    def _rotate_left(self, node, heavy_child):
        """Rotate to make the node the left child of its ``heavy_child``."""

        parent = node.parent
        node.right = heavy_child.left
        node.parent = heavy_child
        heavy_child.left = node
        heavy_child.parent = parent
        if parent:
            if heavy_child.key < parent.key:
                parent.left = heavy_child
            else:
                parent.right = heavy_child
        else:
            self._root = heavy_child

    def _rotate_right(self, node, heavy_child):
        """Rotate to make the node the right child of its ``heavy_child``."""

        parent = node.parent
        node.left = heavy_child.right
        node.parent = heavy_child
        heavy_child.right = node
        heavy_child.parent = node.parent
        if parent:
            if heavy_child.key < parent.key:
                parent.left = heavy_child
            else:
                parent.right = heavy_child
        else:
            self._root = heavy_child


def bst_to_str(node, depth=0):
    """Print a subtree rooted at a node at certain depth."""

    if depth:
        prefix = '|   ' * depth + '|---'
    else:
        prefix = ''

    node_str = prefix + '(' + str(node) + ')\n'

    if node and not node.is_leaf():
        node_str += bst_to_str(node.right, depth + 1)
        node_str += bst_to_str(node.left, depth + 1)

    return node_str


def main():
    avl = AVLTree()
    for k in [1, 3, 4, 5, 6, 2, 0, 7, 8]:
        avl.insert(k)
    print avl
    print '---'
    print avl.kth_smallest_element(1)
    print avl.kth_smallest_element(2)
    print avl.kth_smallest_element(3)
    print avl.kth_smallest_element(4)
    print avl.kth_smallest_element(5)
    print avl.kth_smallest_element(6)
    print avl.kth_smallest_element(7)
    print avl.kth_smallest_element(8)
    print avl.kth_smallest_element(9)
    print '---'
    for key in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        node = avl.search(key)
        successors = []
        for k in xrange(1, avl._root.size - key + 1):
            successors.append(avl.kth_successor(k, node))
        print 'successor of {0}: {1}'.format(key, successors)


def main1():
    avl = AVLTree()
    avl.insert(1)
    avl.insert(3)
    avl.insert(4)
    print avl

if __name__ == '__main__':
    main()
