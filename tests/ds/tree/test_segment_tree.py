"""
    Test case module for zahlen.ds.tree.segment_tree

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

    def test_sg_with_1_element(self):
        sg = SegmentTree([10])
        self.assertEqual(sg.query(0, 0), 0)

    def test_all_equal_even_elements(self):
        sg = SegmentTree([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(sg.query(0, 9), 9)
        self.assertEqual(sg.query(1, 8), 8)
        self.assertEqual(sg.query(2, 7), 7)
        self.assertEqual(sg.query(3, 6), 6)
        self.assertEqual(sg.query(4, 5), 5)
        self.assertEqual(sg.query(5, 5), 5)

    def test_all_equal_odd_elements(self):
        sg = SegmentTree([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(sg.query(0, 10), 10)
        self.assertEqual(sg.query(1, 8), 8)
        self.assertEqual(sg.query(2, 7), 7)
        self.assertEqual(sg.query(3, 6), 6)
        self.assertEqual(sg.query(4, 5), 5)
        self.assertEqual(sg.query(5, 5), 5)

    def test_sorted_elements(self):
        sg = SegmentTree([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(sg.query(0, 0), 0)
        self.assertEqual(sg.query(0, 1), 0)
        self.assertEqual(sg.query(0, 2), 0)
        self.assertEqual(sg.query(1, 3), 1)
        self.assertEqual(sg.query(1, 4), 1)
        self.assertEqual(sg.query(2, 5), 2)
        self.assertEqual(sg.query(3, 6), 3)

    def test_reverse_sorted_elements(self):
        sg = SegmentTree([8, 7, 6, 5, 4, 3, 2, 1])
        self.assertEqual(sg.query(0, 0), 0)
        self.assertEqual(sg.query(0, 1), 1)
        self.assertEqual(sg.query(0, 2), 2)
        self.assertEqual(sg.query(2, 3), 3)
        self.assertEqual(sg.query(2, 4), 4)
        self.assertEqual(sg.query(3, 5), 5)
        self.assertEqual(sg.query(3, 6), 6)
        self.assertEqual(sg.query(4, 7), 7)

    def test_exp_start_less_than_0(self):
        sg = SegmentTree([2, 1, 0, 3])
        self.assertRaises(IndexError, sg.query, -1, 2)

    def test_exp_start_greater_than_end(self):
        sg = SegmentTree([2, 1, 0, 3])
        self.assertRaises(IndexError, sg.query, 3, 1)

    def test_exp_end_greater_than_max_size(self):
        sg = SegmentTree([2, 1, 0, 3])
        self.assertRaises(IndexError, sg.query, 1, 6)


class TestQueryEvenElements(unittest.TestCase):
    """Test cases to test query() on a segment tree with even no. of elements.

    These tests assumes the correctness of the Segment Tree construction.
    """

    def setUp(self):
        self.sg = SegmentTree([3, -1, 1, -2, 6, 5, 0, 2])

    def test_even_ranges(self):
        """The range is same as the range represented by a node i.e. minimum
        index is stored in the heap node. query() simply traverses down the
        tree to find the correct node.
        """

        self.assertEqual(self.sg.query(0, 7), 3)
        self.assertEqual(self.sg.query(0, 3), 3)
        self.assertEqual(self.sg.query(4, 7), 6)
        self.assertEqual(self.sg.query(0, 1), 1)
        self.assertEqual(self.sg.query(2, 3), 3)
        self.assertEqual(self.sg.query(4, 5), 5)
        self.assertEqual(self.sg.query(6, 7), 6)
        self.assertEqual(self.sg.query(0, 0), 0)
        self.assertEqual(self.sg.query(1, 1), 1)
        self.assertEqual(self.sg.query(2, 2), 2)
        self.assertEqual(self.sg.query(3, 3), 3)
        self.assertEqual(self.sg.query(4, 4), 4)
        self.assertEqual(self.sg.query(5, 5), 5)
        self.assertEqual(self.sg.query(6, 6), 6)
        self.assertEqual(self.sg.query(7, 7), 7)

    def test_odd_ranges(self):
        """The range start and end indices are not in the same node. query() has
        to perform additional comparisons at runtime to find the minimum index.
        """

        self.assertEqual(self.sg.query(0, 2), 1)
        self.assertEqual(self.sg.query(0, 3), 3)
        self.assertEqual(self.sg.query(0, 4), 3)
        self.assertEqual(self.sg.query(0, 5), 3)
        self.assertEqual(self.sg.query(0, 6), 3)
        self.assertEqual(self.sg.query(0, 7), 3)

        self.assertEqual(self.sg.query(1, 2), 1)
        self.assertEqual(self.sg.query(1, 3), 3)
        self.assertEqual(self.sg.query(1, 4), 3)
        self.assertEqual(self.sg.query(1, 5), 3)
        self.assertEqual(self.sg.query(1, 6), 3)
        self.assertEqual(self.sg.query(1, 7), 3)

        self.assertEqual(self.sg.query(2, 4), 3)
        self.assertEqual(self.sg.query(2, 5), 3)
        self.assertEqual(self.sg.query(2, 6), 3)
        self.assertEqual(self.sg.query(2, 7), 3)

        self.assertEqual(self.sg.query(3, 4), 3)
        self.assertEqual(self.sg.query(3, 5), 3)
        self.assertEqual(self.sg.query(3, 6), 3)
        self.assertEqual(self.sg.query(3, 7), 3)

        self.assertEqual(self.sg.query(4, 6), 6)
        self.assertEqual(self.sg.query(4, 7), 6)

        self.assertEqual(self.sg.query(5, 6), 6)
        self.assertEqual(self.sg.query(5, 7), 6)


class TestQueryOddElements(unittest.TestCase):
    """Test cases to test query() on a segment tree with odd no. of elements.

    These tests assumes the correctness of the Segment Tree construction.
    """

    def setUp(self):
        self.sg = SegmentTree([2, 1, 3, 6, -2, 1, 0, -2, -1])

    def test_even_ranges(self):
        """The range is same as the range represented by a node i.e. minimum
        index is stored in the heap node. query() simply traverses down the
        tree to find the correct node.
        """

        self.assertEqual(self.sg.query(0, 8), 7)
        self.assertEqual(self.sg.query(0, 4), 4)
        self.assertEqual(self.sg.query(5, 8), 7)
        self.assertEqual(self.sg.query(0, 2), 1)
        self.assertEqual(self.sg.query(3, 4), 4)
        self.assertEqual(self.sg.query(5, 6), 6)
        self.assertEqual(self.sg.query(7, 8), 7)
        self.assertEqual(self.sg.query(0, 1), 1)
        self.assertEqual(self.sg.query(2, 2), 2)
        self.assertEqual(self.sg.query(3, 3), 3)
        self.assertEqual(self.sg.query(4, 4), 4)
        self.assertEqual(self.sg.query(5, 5), 5)
        self.assertEqual(self.sg.query(6, 6), 6)
        self.assertEqual(self.sg.query(7, 7), 7)
        self.assertEqual(self.sg.query(8, 8), 8)

    def test_odd_ranges(self):
        """The range start and end indices are not in the same node. query() has
        to perform additional comparisons at runtime to find the minimum index.
        """

        self.assertEqual(self.sg.query(0, 3), 1)
        self.assertEqual(self.sg.query(0, 4), 4)
        self.assertEqual(self.sg.query(0, 5), 4)
        self.assertEqual(self.sg.query(0, 6), 4)
        self.assertEqual(self.sg.query(0, 7), 7)

        self.assertEqual(self.sg.query(1, 2), 1)
        self.assertEqual(self.sg.query(1, 3), 1)
        self.assertEqual(self.sg.query(1, 4), 4)
        self.assertEqual(self.sg.query(1, 5), 4)
        self.assertEqual(self.sg.query(1, 6), 4)
        self.assertEqual(self.sg.query(1, 7), 7)
        self.assertEqual(self.sg.query(1, 8), 7)

        self.assertEqual(self.sg.query(2, 3), 2)
        self.assertEqual(self.sg.query(2, 4), 4)
        self.assertEqual(self.sg.query(2, 5), 4)
        self.assertEqual(self.sg.query(2, 6), 4)
        self.assertEqual(self.sg.query(2, 7), 7)
        self.assertEqual(self.sg.query(2, 8), 7)

        self.assertEqual(self.sg.query(3, 5), 4)
        self.assertEqual(self.sg.query(3, 6), 4)
        self.assertEqual(self.sg.query(3, 7), 7)
        self.assertEqual(self.sg.query(3, 8), 7)

        self.assertEqual(self.sg.query(4, 5), 4)
        self.assertEqual(self.sg.query(4, 6), 4)
        self.assertEqual(self.sg.query(4, 7), 7)
        self.assertEqual(self.sg.query(4, 8), 7)

        self.assertEqual(self.sg.query(5, 7), 7)
        self.assertEqual(self.sg.query(5, 8), 7)

        self.assertEqual(self.sg.query(6, 7), 7)
        self.assertEqual(self.sg.query(6, 8), 7)


class TestUpdate(unittest.TestCase):
    """Test cases to test update() on a segment tree.

    These tests assumes the correctness of SegmentTree.query().
    """

    def test_index_less_than_0_exception(self):
        sg = SegmentTree([10, 11])
        self.assertRaises(IndexError, sg.update, -1, 10)

    def test_index_greater_than_size_exception(self):
        sg = SegmentTree([10, 11])
        self.assertRaises(IndexError, sg.update, 2, 10)

    def test_update_leftmost_leaf(self):
        sg = SegmentTree([2, 1, 3, 6, -2, 1, 0, -2, -1])
        sg.update(0, 0)
        self.assertEqual(sg.query(0, 1), 0)
        self.assertEqual(sg.query(0, 3), 0)
        self.assertEqual(sg.query(0, 4), 4)

    def test_update_rightmost_leaf(self):
        sg = SegmentTree([2, 1, 3, 6, -2, 1, 0, -2, -1])
        sg.update(8, 2)
        self.assertEqual(sg.query(0, 8), 7)
        sg.update(8, -3)
        self.assertEqual(sg.query(5, 8), 8)

    def test_update_left_leaf(self):
        sg = SegmentTree([2, 1, 3, 6, -2, 1, 0, -2, -1])
        sg.update(2, 0)
        self.assertEqual(sg.query(0, 3), 2)
        self.assertEqual(sg.query(0, 4), 4)

    def test_update_right_leaf(self):
        sg = SegmentTree([2, 1, 3, 6, -2, 1, 0, -2, -1])
        sg.update(6, -1)
        self.assertEqual(sg.query(5, 6), 6)
        self.assertEqual(sg.query(4, 8), 7)

    def test_update_root_min(self):
        sg = SegmentTree([2, 1, 3, 6, -2, 1, 0, -2, -1])
        sg.update(5, -3)
        self.assertEqual(sg.query(5, 8), 5)
        self.assertEqual(sg.query(0, 8), 5)