# -*- coding: utf-8 -*-

"""
    zahlen.ds.tree.segment_tree
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Segment Tree data structure.

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from collections import deque


class SegmentTree(object):
    def __init__(self, size, elements=None):
        self._rmqs = {}
        self._size = size
        self._leaves = {}

        if not elements:
            self._elements = [None] * size
        else:
            if len(elements) != size:
                print 'Size mismatch'   # Or throw error
                return
            self._elements = elements

        self._build(0, 0, size - 1)

    def __str__(self):
        """Return a string representation of the segment tree."""

        queue = deque()
        items = []

        queue.append((0, 0, self._size - 1))
        while queue:
            range_index, start, end = queue.popleft()
            items.append((start, end, self._rmqs[range_index]))

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
        for s, e, m in items:
            sg_tree_str = \
                '{0}\nstart={1}, end={2}, minimum={3}'.format(sg_tree_str,
                                                              s, e, m)
        return sg_tree_str

    def update(self, index, element):
        """Update an element at the specified index."""

        if index < 0 or index > self._size - 1:
            print 'Invalid index'  # Or throw error
            return

        range_index = self._leaves[index]
        self._elements[index] = element
        self._rmqs[range_index] = element

        while True:
            parent_range_index = self._parent_range_index(range_index)
            if parent_range_index < 0:
                break

            # Range minimum at the parent node may not be set i.e. it has the
            # default value of None. Update the parent for the comparisons to be
            # correct.
            parent_min = self._rmqs[parent_range_index]

            # Explicitly check for None because parent minimum may be zero.
            if parent_min is None:
                parent_min = element

            if element > parent_min:
                break
            else:
                self._rmqs[parent_range_index] = element
                range_index = parent_range_index

    def query(self, start, end, range_index=0, range_start=0, range_end=None):
        """Return the minimum within the specified range."""

        if not range_end:
            range_end = self._size - 1

        if range_start == start and range_end == end:
            return self._rmqs[range_index]
        elif start == end:
            return self._rmqs[self._leaves[start]]
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
                return \
                    min(self.query(start, mid, left_range_index, range_start,
                                   mid),
                        self.query(mid + 1, end, right_range_index, mid + 1,
                                   range_end))

    def _build(self, range_index, start, end):
        if start == end:
            self._leaves[start] = range_index
            self._rmqs[range_index] = self._elements[start]
        else:
            mid = (start + end) / 2
            left_range_index = 2 * range_index + 1
            right_range_index = left_range_index + 1

            # Build left and right child subtree
            self._build(left_range_index, start, mid)
            self._build(right_range_index, mid + 1, end)

            # Calculate the range minimum for the current range.
            left_range_min = self._rmqs[left_range_index]
            right_range_min = self._rmqs[right_range_index]
            self._rmqs[range_index] = left_range_min \
                if left_range_min < right_range_min else right_range_min

    @staticmethod
    def _parent_range_index(range_index):
        if range_index % 2 == 0:
            parent_range_index = (range_index - 2) / 2  # parent of right child
        else:
            parent_range_index = (range_index - 1) / 2  # parent of left child
        return parent_range_index


if __name__ == '__main__':
    st = SegmentTree(9)
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
