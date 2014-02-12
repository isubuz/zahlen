

class Node(object):
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

    def is_leaf(self):
        return not self.left and not self.right


class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    def __str__(self):
        return bst_to_str(self.root)

    def delete(self, key):
        """Delete a node with the specified key."""

        node = self.root
        parent = None
        while node:
            if node.key == key:
                break

            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if not node:
            print 'Node with key {0} not found'.format(key)  # or raise error
        elif node.is_leaf():
            self._delete_leaf_node(node, parent)
        else:
            self._delete_non_leaf_node(node, parent)

    def insert(self, key):
        """Insert a new node with the input key using an iterative process."""

        if not self.root:
            self.root = Node(key)
        else:
            node = self.root
            while True:
                if key >= node.key:
                    if node.right:
                        node = node.right
                    else:
                        node.right = Node(key)
                        break
                else:
                    if node.left:
                        node = node.left
                    else:
                        node.left = Node(key)
                        break

    def insert_recursive(self, key, node=None):
        """Insert a new node with the input key using a recursive process."""

        if not node:
            if not self.root:
                self.root = Node(key)
                return
            else:
                node = self.root

        if key < node.key:
            if not node.left:
                node.left = Node(key)
            else:
                self.insert_recursive(key, node.left)
        else:
            if not node.right:
                node.right = Node(key)
            else:
                self.insert_recursive(key, node.right)

    def inorder_walk(self, node):
        """Traverse the BST in in-order rooted at the input node and print the
        keys."""

        if node:
            self.inorder_walk(node.left)
            print node.key
            self.inorder_walk(node.right)

    def postorder_walk(self, node):
        """Traverse the BST in post-order rooted at the input node and print
        the keys."""

        if node:
            self.inorder_walk(node.left)
            self.inorder_walk(node.right)
            print node.key

    def preorder_walk(self, node):
        """Traverse the BST in pre-order rooted at the input node and print the
        keys."""

        if node:
            print node.key
            self.inorder_walk(node.left)
            self.inorder_walk(node.right)

    def search(self, key):
        """Returns true if a node with the specified key exists."""

        node = self.root
        while True:
            if node:
                if key == node.key:
                    return True
                elif key > node.key:
                    node = node.right
                else:
                    node = node.left
            else:
                return False

    def _delete_non_leaf_node(self, node, parent):
        """Delete a node with 1 or 2 children."""

        if not node.left or not node.right:
            if not node.left:
                # Replace node by right child
                node = node.right
            else:
                # Replace node by left child
                node = node.left
            # Update the parent to reflect new child.
            if node.key < parent.key:
                parent.left = node
            else:
                parent.right = node
        else:
            # Replace node's key by inorder successor's key and remove the
            # successor.
            successor = self.successor(node)
            self.delete(successor.key)
            node.key = successor.key

    @staticmethod
    def _delete_leaf_node(node, parent):
        """Delete a leaf node."""

        if node.key < parent.key:
            parent.left = None
        else:
            parent.right = None
        del node

    @staticmethod
    def successor(node):
        """Return the inorder successor of the input node."""
        node = node.right
        if not node:
            return None
        while node.left:
            node = node.left
        return node


def bst_search_recur(node, key):
    """Returns true if a node with the specified key exists.

    Recursively traverses the tree to find the node.
    """

    if node:
        if key == node.key:
            return True
        elif key > node.key:
            return bst_search_recur(node.right, key)
        else:
            return bst_search_recur(node.left, key)
    else:
        return False


def bst_to_str(node, depth=0):
    """Print a subtree rooted at a node at certain depth."""

    key = node.key if node else 'NULL'

    if depth:
        prefix = '|   ' * depth + '|---'
    else:
        prefix = ''

    node_str = prefix + '(' + str(key) + ')\n'

    if node and not node.is_leaf():
        node_str += bst_to_str(node.right, depth + 1)
        node_str += bst_to_str(node.left, depth + 1)

    return node_str


def get_bst():
    bst = BinarySearchTree()
    bst.insert_recursive(8)
    bst.insert_recursive(10)
    bst.insert_recursive(1)
    bst.insert_recursive(4)
    bst.insert_recursive(6)
    bst.insert_recursive(9)
    bst.insert_recursive(2)
    bst.insert_recursive(5)
    return bst


if __name__ == '__main__':
    b = get_bst()
    print b
    b.delete(5)
    print b
    b = get_bst()
    print b
    b.delete(10)
    print b
    b = get_bst()
    print b
    b.delete(4)
    print b
    b = get_bst()
    print b
    b.delete(1)
    print b
    b = get_bst()
    print b
    b.delete(8)
    print b
