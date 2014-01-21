

def partition(items, start, end):
    """Find the pivot position and partition the items based on that."""

    pivot_item = items[start]
    pivot_pos = start

    for j in xrange(start + 1, end):
        if items[j] <= pivot_item:
            pivot_pos += 1
            items[pivot_pos], items[j] = items[j], items[pivot_pos]

    items[start], items[pivot_pos] = items[pivot_pos], items[start]

    return pivot_pos


def sort(items):
    """Sort the input list of items using Quick sort.

    This method modifies the input by sorting the elements in the list.
    """

    _sort_recursive(items, 0, len(items))


def _sort_recursive(items, start, end):
    if start < end - 1:
        pivot_pos = partition(items, start, end)
        _sort_recursive(items, start, pivot_pos - 1)
        _sort_recursive(items, pivot_pos + 1, end)
