from math import log


def sort(a_list, base):
    """Sort the input list with the specified base, using Radix sort.

    This implementation assumes that the input list does not contain negative
    numbers. This algorithm is inspired from the Wikipedia implmentation of
    Radix sort.
    """

    passes = int(log(max(a_list), base) + 1)

    items = a_list[:]
    for digit_index in xrange(passes):
        buckets = [[] for _ in xrange(base)]  # Buckets for sorted sublists.
        for item in items:
            digit = _get_digit(item, base, digit_index)
            buckets[digit].append(item)

        items = []
        for sublists in buckets:
            items.extend(sublists)

    return items


def _get_digit(number, base, digit_index):
    return (number // base ** digit_index) % base
