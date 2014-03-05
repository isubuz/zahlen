"""
    Test case module for

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from zahlen.ds.tree.segment_tree import SegmentTree

import unittest


class TestCreateSegmentTree(unittest.TestCase):
    """Test cases to test the creation of a segment tree from an
    initial list of elements.

    This test asserts the internal structures of the segment tree. Inorder to do
    so, it has to access the private/protected members of the class.
    """

    def test_empty_list_exception(self):
        self.assertRaises(ValueError, SegmentTree, [])

    def test_list_with_1_element(self):
        sg = SegmentTree([10])
        self.assertEqual(sg._min_range_indices[0], 0)
        self.assertEqual(sg._leaves_range_indices[0], 0)

    def test_list_with_odd_elements(self):
        sg = SegmentTree([2, 1, 3, 6, 0, -1, -2])
        min_indices = sg._min_range_indices

        self.assertEqual(min_indices[0], 6)
        self.assertEqual(min_indices[1], 1)
        self.assertEqual(min_indices[2], 6)
        self.assertEqual(min_indices[3], 1)
        self.assertEqual(min_indices[4], 2)
        self.assertEqual(min_indices[5], 5)
        self.assertEqual(min_indices[6], 6)
        self.assertEqual(min_indices[7], 0)
        self.assertEqual(min_indices[8], 1)
        self.assertEqual(min_indices[9], 2)
        self.assertEqual(min_indices[10], 3)
        self.assertEqual(min_indices[11], 4)
        self.assertEqual(min_indices[12], 5)

        leaves_indices = sg._leaves_range_indices
        self.assertEqual(leaves_indices[6], 6)
        self.assertEqual(leaves_indices[0], 7)
        self.assertEqual(leaves_indices[1], 8)
        self.assertEqual(leaves_indices[2], 9)
        self.assertEqual(leaves_indices[3], 10)
        self.assertEqual(leaves_indices[4], 11)
        self.assertEqual(leaves_indices[5], 12)

    def test_list_with_even_elements(self):
        sg = SegmentTree([3, -1, 1, -2, 6, 5, 0, 2])
        min_indices = sg._min_range_indices

        self.assertEqual(min_indices[0], 3)
        self.assertEqual(min_indices[1], 3)
        self.assertEqual(min_indices[2], 6)
        self.assertEqual(min_indices[3], 1)
        self.assertEqual(min_indices[4], 3)
        self.assertEqual(min_indices[5], 5)
        self.assertEqual(min_indices[6], 6)
        self.assertEqual(min_indices[7], 0)
        self.assertEqual(min_indices[8], 1)
        self.assertEqual(min_indices[9], 2)
        self.assertEqual(min_indices[10], 3)
        self.assertEqual(min_indices[11], 4)
        self.assertEqual(min_indices[12], 5)
        self.assertEqual(min_indices[13], 6)
        self.assertEqual(min_indices[14], 7)

        leaves_indices = sg._leaves_range_indices
        self.assertEqual(leaves_indices[0], 7)
        self.assertEqual(leaves_indices[1], 8)
        self.assertEqual(leaves_indices[2], 9)
        self.assertEqual(leaves_indices[3], 10)
        self.assertEqual(leaves_indices[4], 11)
        self.assertEqual(leaves_indices[5], 12)
        self.assertEqual(leaves_indices[6], 13)
        self.assertEqual(leaves_indices[7], 14)


class TestQuery(unittest.TestCase):
    """Test cases to test query() on a segment tree.

    These tests assumes the correctness of the Segment Tree construction.
    """
    pass


class TestUpdate(unittest.TestCase):
    """Test cases to test update() on a segment tree.

    These tests assumes the correctness of SegmentTree.query().
    """
    pass