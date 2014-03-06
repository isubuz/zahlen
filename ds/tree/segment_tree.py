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

    Note that this implementation of a Segment Tree does not support addition
    of new elements in the tree. All elements must be supplied in a list during
    the segment tree creation. An element at a specified index can be updated.

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

        if not elements:
            raise ValueError('Expected a non-empty list of input elements')

        # Store the index of the minimum value for every range index. A range
        # index is the index of the node in the heap which corresponds to a
        # particular range.
        self._min_range_indices = {}

        # Stores the range indices of all the leaves in the heap i.e. the
        # positions of the leaves in the heap.
        self._leaves_range_indices = {}

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
            min_index = self._min_range_indices[range_index]
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

        range_index = self._leaves_range_indices[index]
        self._elements[index] = element

        while True:
            parent_range_index = self._parent_range_index(range_index)
            if parent_range_index < 0:
                break

            parent_min = self._min_range_indices[parent_range_index]

            if element > self._elements[parent_min]:
                break
            else:
                self._min_range_indices[parent_range_index] = index
                range_index = parent_range_index

    def query(self, start, end, range_index=0, range_start=0, range_end=None):
        """Return the index of the minimum within the specified range.

        The returned index is the index of an element in the list used to create
        the segment tree. If the more than one minimum's within a range,
        the highest index is returned.

        :param start: range start index
        :param end: range end index
        """

        if not 0 <= start <= end:
            raise ValueError("Invalid start index:" + str(start))

        if not start <= end < self._size:
            raise ValueError("Invalid end index: " + str(end))

        if not range_end:
            range_end = self._size - 1

        if range_start == start and range_end == end:
            # Minimum index already computed and stored in node.
            return self._min_range_indices[range_index]
        elif start == end:
            # Leaf node
            return self._min_range_indices[self._leaves_range_indices[start]]
        else:
            # Non-leaf node and compute the minimum index at runtime.
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

        Each node in the heap represents a range and store the index of the
        minimum value within that range. The index referred is the index in the
        list supplied during the segment tree construction.
        """

        if start == end:
            # Leaf node
            self._leaves_range_indices[start] = range_index
            self._min_range_indices[range_index] = start
        else:
            # Internal node
            mid = (start + end) / 2
            left_range_index = 2 * range_index + 1
            right_range_index = left_range_index + 1

            # Build left and right child subtree
            self._build(left_range_index, start, mid)
            self._build(right_range_index, mid + 1, end)

            # Calculate the range minimum index for the current range.
            left_min_index = self._min_range_indices[left_range_index]
            left_range_min = self._elements[left_min_index]
            right_min_index = self._min_range_indices[right_range_index]
            right_range_min = self._elements[right_min_index]

            self._min_range_indices[range_index] = left_min_index \
                if left_range_min < right_range_min else right_min_index

    @staticmethod
    def _parent_range_index(range_index):
        """Return the parent index for the child range index."""

        if range_index % 2 == 0:
            parent_range_index = (range_index - 2) / 2  # parent of right child
        else:
            parent_range_index = (range_index - 1) / 2  # parent of left child
        return parent_range_index