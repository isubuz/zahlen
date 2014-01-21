

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

        pass

    def insert(self, key):
        """Insert a new node with the specified key."""

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
        node_str = node_str + bst_to_str(node.left, depth + 1)
        node_str = node_str + bst_to_str(node.right, depth + 1)

    return node_str


if __name__ == '__main__':
    bst = BinarySearchTree()
    bst.insert(8)
    bst.insert(10)
    bst.insert(1)
    bst.insert(4)
    bst.insert(6)
    bst.insert(9)
    bst.insert(2)
    bst.insert(5)

    print bst
