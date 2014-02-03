# -*- coding: utf-8 -*-
"""
    zahlen.ds.trie.trie
    ~~~~~~~~~~~~~~~~~~~

    Implements the Trie data structure. A Trie is also known as a Prefix Tree.
    The edge links for every node in the trie is stored in a dictionary.

    References:
    - http://community.topcoder.com/tc?module=Static&d1=tutorials&d2=usingTries
    - http://en.wikipedia.org/wiki/Trie
"""


class Vertex(object):
    def __init__(self, key):
        self._key = key
        self.word_count = 0
        self.prefix_count = 0
        self.edges = {}


class Trie(object):
    def __init__(self):
        self._root = Vertex('')

    def add_word(self, word, vertex=None):
        """Add a word to the trie."""

        if not vertex:
            vertex = self._root

        if word:
            key = word[0]
            if key not in vertex.edges:
                next_vertex = Vertex(key)
                vertex.edges[key] = next_vertex
            else:
                next_vertex = vertex.edges[key]

            next_vertex.prefix_count += 1
            if len(word) == 1:
                next_vertex.word_count += 1
            else:
                self.add_word(word[1:], next_vertex)

    def add_words(self, words, vertex=None):
        """Add a list of words to the trie."""

        for word in words:
            self.add_word(word, vertex)

    def prefix_count(self, prefix, vertex=None):
        """Return the count of words which begins with the specified prefix."""

        if not vertex:
            vertex = self._root

        if prefix:
            key = prefix[0]
            if key in vertex.edges:
                next_vertex = vertex.edges[key]
                if len(prefix) == 1:
                    return next_vertex.prefix_count
                else:
                    return self.prefix_count(prefix[1:], next_vertex)
        return 0

    def remove_word(self, word):
        pass

    def search(self, word, vertex=None):
        """Search for a word in the trie.

        This is merely a utility method and calls word_count() and checks if the
        word frequency is greater than zero.
        """

        if not vertex:
            vertex = self._root

        return self.word_count(word, vertex) > 0

    def word_count(self, word, vertex=None):
        """Return the frequency of the word in the trie."""

        if not vertex:
            vertex = self._root

        if word:
            key = word[0]
            if key in vertex.edges:
                next_vertex = vertex.edges[key]
                if len(word) == 1:
                    return next_vertex.word_count
                else:
                    return self.word_count(word[1:], next_vertex)
        return 0
