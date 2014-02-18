__author__ = 'isubuz'


class FenwickTree(object):
    def __init__(self, frequencies):
        # Note that the Fenwick tree is represented as a one-indexed array.
        self.size = len(frequencies) + 1
        self._tree = [0] * self.size

        for i in range(1, self.size + 1):
            self.update(i, frequencies[i - 1])

    def read(self, index):
        """Read the value at the specified index.

        Arguments:
            index   position in an one-indexed array
        """
        value = 0
        while index > 0:
            value += self._tree[index]
            index -= (index & -index)
        return value

    def update(self, index, value):
        """Update the value at the specified index.

        Arguments:
            index   position in an one-indexed array
            value   new value at the specified index
        """
        while index <= self.size:
            self._tree[index] += value
            index += (index & -index)
