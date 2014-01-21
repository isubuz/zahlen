
"""heap_sort.py: Implements the Heap Sort algorithm."""


def max_heapify(items, index, heap_size):
    left_index = 2 * index + 1      # index of left child
    right_index = 2 * index + 2     # index of right child

    largest = index
    for i in [left_index, right_index]:
        if i <= heap_size - 1 and items[i] > items[largest]:
            largest = i

    if largest != index:
        items[largest], items[index] = items[index], items[largest]
        max_heapify(items, largest, heap_size)


def build_max_heap(items):
    heap_size = len(items)
    mid = heap_size / 2 - 1
    for i in xrange(mid, -1, -1):
        max_heapify(items, i, heap_size)


def sort(items):
    """Sort the input list of elements using Heap sort algorithm."""

    build_max_heap(items)

    for i in xrange(len(items) - 1, 0, -1):
        # Move the highest element to the end of the sorted list.
        items[0], items[i] = items[i], items[0]

        max_heapify(items, 0, i)
