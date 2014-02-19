# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.segment_tree
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Segment Tree data structure.

    TODO (isubuz)
    - Support insertion of new elements in the segment tree.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque


class SegmentTree(object):
    """Construct a segment tree.

    Example usage::
        elements = [2, 1, 3, 6, 0, -1, -2]

        # Build the segment tree
        st = SegmentTree(elements)

        # Update the value of an existing element.
        # Note that the index corresponds to the index in the original list of
        # elements.
        st.update(index, new_value)

        # Query the minimum index within a range
        st.query(start, end)
    """

    def __init__(self, elements):

        # Store the indices of the minimum value for every range index. A range
        # index is the index of the node in the heap which maps to a particular
        # range.
        self._range_min_indices = {}

        # Stores the range indices of all the leaves in the heap.
        self._leaves = {}

        self._size = len(elements)
        self._elements = elements

        self._build(0, 0, self._size - 1)

    def __str__(self):
        """Return a string representation of the segment tree."""

        queue = deque()
        items = []

        queue.append((0, 0, self._size - 1))
        while queue:
            range_index, start, end = queue.popleft()
            min_index = self._range_min_indices[range_index]
            items.append((start, end, min_index, self._elements[min_index]))

            if start != end:
                # If not a left node, add the left and right child to the queue.
                # Note that every non-leaf node is complete i.e. it has both the
                # left and the right child.
                mid = (start + end) / 2
                left_range_index = 2 * range_index + 1
                right_range_index = left_range_index + 1
                queue.append((left_range_index, start, mid))
                queue.append((right_range_index, mid + 1, end))

        sg_tree_str = ''
        for s, e, i, v in items:
            sg_tree_str = \
                '{0}\nstart={1}, end={2}, minimum_index={3}, ' \
                'minimum_value={4}'.format(sg_tree_str, s, e, i, v)
        return sg_tree_str

    def update(self, index, element):
        """Update an element at the specified index."""

        if index < 0 or index > self._size - 1:
            print 'Invalid index'  # Or throw error
            return

        range_index = self._leaves[index]
        self._elements[index] = element

        while True:
            parent_range_index = self._parent_range_index(range_index)
            if parent_range_index < 0:
                break

            parent_min = self._range_min_indices[parent_range_index]

            if element > self._elements[parent_min]:
                break
            else:
                self._range_min_indices[parent_range_index] = index
                range_index = parent_range_index

    def query(self, start, end, range_index=0, range_start=0, range_end=None):
        """Return the index of the minimum within the specified range."""

        if not range_end:
            range_end = self._size - 1

        if range_start == start and range_end == end:
            return self._range_min_indices[range_index]
        elif start == end:
            return self._range_min_indices[self._leaves[start]]
        else:
            mid = (range_start + range_end) / 2
            left_range_index = 2 * range_index + 1
            right_range_index = left_range_index + 1

            if end <= mid:
                return self.query(start, end, left_range_index, range_start,
                                  mid)
            elif start > mid:
                return self.query(start, end, right_range_index, mid + 1,
                                  range_end)
            else:
                left_min_index = self.query(start, mid, left_range_index,
                                            range_start, mid)
                right_min_index = self.query(mid + 1, end, right_range_index,
                                             mid + 1, range_end)
                if self._elements[left_min_index] < \
                        self._elements[right_min_index]:
                    return left_min_index
                else:
                    return right_min_index

    def _build(self, range_index, start, end):
        """Build the heap structure for the segment tree.

        Each index in the heap stores the index of the minimum value within
        a range.
        """

        if start == end:
            self._leaves[start] = range_index
            self._range_min_indices[range_index] = start
        else:
            mid = (start + end) / 2
            left_range_index = 2 * range_index + 1
            right_range_index = left_range_index + 1

            # Build left and right child subtree
            self._build(left_range_index, start, mid)
            self._build(right_range_index, mid + 1, end)

            # Calculate the range minimum index for the current range.
            left_min_index = self._range_min_indices[left_range_index]
            left_range_min = self._elements[left_min_index]
            right_min_index = self._range_min_indices[right_range_index]
            right_range_min = self._elements[right_min_index]

            self._range_min_indices[range_index] = left_min_index \
                if left_range_min < right_range_min else right_min_index

    @staticmethod
    def _parent_range_index(range_index):
        """Return the parent index for the child range index."""

        if range_index % 2 == 0:
            parent_range_index = (range_index - 2) / 2  # parent of right child
        else:
            parent_range_index = (range_index - 1) / 2  # parent of left child
        return parent_range_index


def test1():
    st = SegmentTree(9)
    print st
    st.update(0, 2)
    st.update(1, 1)
    st.update(2, 6)
    st.update(3, 3)
    st.update(4, 5)
    st.update(5, 0)
    st.update(6, 4)
    st.update(7, -1)
    st.update(8, -2)
    print st

    print '---'
    print st.query(0, 7)
    print st.query(0, 3)
    print st.query(4, 7)
    print st.query(0, 1)
    print st.query(2, 3)
    print st.query(4, 5)
    print st.query(6, 7)
    print st.query(0, 0)
    print st.query(1, 1)
    print st.query(2, 2)
    print st.query(3, 3)
    print st.query(4, 4)
    print st.query(5, 5)
    print st.query(6, 6)
    print st.query(7, 7)
    print st.query(0, 5)
    print st.query(2, 7)
    print st.query(1, 3)
    print st.query(2, 4)
    print st.query(5, 7)
    print st.query(5, 6)
    print st.query(0, 8)
    print st.query(5, 8)


def test2():
    st = SegmentTree([2, 1, 6, 3, 5, 0, 4, -1, -2])
    print st
    st.update(4, -3)
    print st
    st.update(8, 7)
    print st


def test3():
    st = SegmentTree([2, 1, 6, 3, -3, 0, 4, -1, -2])
    print st.query(0, 8)
    print st.query(0, 6)
    print st.query(5, 8)
    print st.query(5, 7)
    print st.query(0, 3)

if __name__ == '__main__':
    test3()
