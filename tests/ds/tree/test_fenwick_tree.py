from zahlen.ds.tree.fenwick_tree import FenwickTree

import unittest


class TestFenwickTreeExceptions(unittest.TestCase):
    """Assert the exceptions thrown during the creation, read and update
    operations on a Fenwick Tree.
    """

    def test_invalid_size_exception(self):
        self.assertRaises(ValueError, FenwickTree, 0)
        self.assertRaises(ValueError, FenwickTree, -3)

    def test_index_less_than_0_read_exception(self):
        ft = FenwickTree(10)
        self.assertRaises(IndexError, ft.read, -1)

    def test_index_greater_than_size_read_exception(self):
        ft = FenwickTree(10)
        self.assertRaises(IndexError, ft.read, 11)

    def test_index_less_than_0_update_exception(self):
        ft = FenwickTree(10)
        self.assertRaises(IndexError, ft.update, -1, 4)

    def test_index_greater_than_size_update_exception(self):
        ft = FenwickTree(10)
        self.assertRaises(IndexError, ft.update, 11, 4)


class TestFenwickTree(unittest.TestCase):
    def setUp(self):
        self.ft = FenwickTree(13)
        for index, value in enumerate([1, 0, 2, 1, 1, 3, 0, 4, 2, 5, 2, 2, 3]):
            self.ft.update(index, value)

    def test_read_left_edge(self):
        self.assertEqual(self.ft.read(0), 1)

    def test_read_right_edge(self):
        self.assertEqual(self.ft.read(self.ft.size - 1), 26)

    def test_read_power_of_2(self):
        self.assertEqual(self.ft.read(1), 1)
        self.assertEqual(self.ft.read(3), 4)
        self.assertEqual(self.ft.read(7), 12)

    def test_read_even_index(self):
        """Note that the index referred is the index in the BIT indexed tree
        which is based on a 1-indexed array. But internally the tree is
        implemented using a 0-indexed array.
        """

        self.assertEqual(self.ft.read(5), 8)
        self.assertEqual(self.ft.read(9), 19)
        self.assertEqual(self.ft.read(11), 23)

    def test_read_odd_index(self):
        """Note that the index referred is the index in the BIT indexed tree
        which is based on a 1-indexed array. But internally the tree is
        implemented using a 0-indexed array.
        """

        self.assertEqual(self.ft.read(2), 3)
        self.assertEqual(self.ft.read(4), 5)
        self.assertEqual(self.ft.read(6), 8)
        self.assertEqual(self.ft.read(8), 14)
        self.assertEqual(self.ft.read(10), 21)
