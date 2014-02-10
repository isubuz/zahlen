# -*- coding: utf-8 -*-


class Vertex(object):
    def __init__(self, left_index, right_index=None):
        self.left_index = left_index
        self.right_index = right_index
        self.children = {}
        self.suffix = None

    def __eq__(self, other):
        return self.left_index == other.left_index and \
            self.right_index == other.right_index

    def __str__(self):
        return str(self.left_index)

    def is_leaf(self):
        return self.right_index is None


class SuffixTree(object):
    def __init__(self, text):
        self._root = Vertex(-1, -1)
        self._active_vertex = self._root
        self._active_edge = None
        self._active_length = 0
        self._current_end = 0
        self._remainder = 0
        self.text = text + '$'

    def all_suffixes(self, vertex=None, prefix=''):
        if not vertex:
            vertex = self._root

        prefix += self.vertex2substring(vertex)
        if vertex.is_leaf():
            print prefix
        else:
            for child in vertex.children.itervalues():
                self.all_suffixes(child, prefix)

    def build(self):
        for index, char in enumerate(self.text):
            previous_split_vertex = None
            self._current_end += 1
            self._remainder += 1
            if self._active_edge is None:
                self._active_edge = char

            while self._remainder > 0:
                if self._active_edge not in self._active_vertex.children:
                    self._active_vertex.children[self._active_edge] = \
                        Vertex(index)
                    self._set_next_active_point()
                else:
                    child = self._active_vertex.children[self._active_edge]
                    substring = self.vertex2substring(child)
                    active_char = substring[self._active_length]
                    if active_char == char:
                        # If all characters stored in the child are consumed,
                        # start searching from the child.
                        if len(substring) == self._active_length + 1:
                            self._active_vertex = child
                            self._active_edge = None
                            self._active_length = 0
                        else:
                            self._active_length += 1
                        break
                    else:
                        child = self._split_vertex(child, active_char, char)
                        self._set_next_active_point(
                            substring=self.vertex2substring(child))

                        # If not the first vertex split in the current
                        # iteration, create a suffix link from the previous
                        # splitted vertex to the current one.
                        if previous_split_vertex:
                            previous_split_vertex.suffix = child
                        previous_split_vertex = child

    def vertex_length(self, vertex):
        right = self._current_end if not vertex.right_index \
            else vertex.right_index
        return right - vertex.left_index

    def vertex2substring(self, vertex):
        left = vertex.left_index
        right = self._current_end if not vertex.right_index \
            else vertex.right_index
        return self.text[left:right]

    def _canonize(self, next_active_vertex, substring):
        self._active_vertex = next_active_vertex

        if not self._active_edge or self._active_edge \
                not in self._active_vertex.children:
            return

        next_child = next_active_vertex.children[self._active_edge]
        next_child_length = self.vertex_length(next_child)

        if self._active_length + 1 > next_child_length:
            if len(substring) == next_child_length:
                self._active_edge = None
                self._active_length = 0
            else:
                substring = substring[next_child_length:]
                self._active_edge = substring[0]
                self._active_length -= next_child_length

            self._canonize(next_child, substring)

    def _set_next_active_point(self, substring=''):
        self._remainder -= 1

        if self._active_vertex != self._root:
            next_active_vertex = self._root if not self._active_vertex.suffix \
                else self._active_vertex.suffix
            self._canonize(next_active_vertex, substring)
        else:
            if self._remainder > 0:
                self._active_edge = \
                    self.text[self._current_end - self._remainder]
                self._active_length -= 1
            else:
                self._active_edge = None

    def _split_vertex(self, vertex, active_char, new_char):
        """Split the input vertex and create two children."""

        # Create and insert the new vertex at the active vertex and active edge
        new_vertex = Vertex(vertex.left_index,
                            vertex.left_index + self._active_length)
        self._active_vertex.children[self._active_edge] = new_vertex

        # Create a new vertex for the new character to be inserted which
        # becomes the left child.
        new_vertex.children[new_char] = Vertex(self._current_end - 1)

        # The old vertex key is updated and becomes the right child
        vertex.left_index += self._active_length
        new_vertex.children[active_char] = vertex

        return new_vertex


if __name__ == '__main__':
    st = SuffixTree('cxccc')
    st.build()
    st.all_suffixes()
