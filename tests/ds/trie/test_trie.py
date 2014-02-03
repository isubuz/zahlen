# -*- coding: utf-8 -*-
"""
    Test case module for Trie data structure.
"""

from zahlen.ds.trie.trie import Trie

import unittest


class TestEmptyTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()

    def test_prefix_count_0_len(self):
        self.assertEqual(self.trie.prefix_count(''), 0)

    def test_prefix_count(self):
        self.assertEqual(self.trie.prefix_count('bar'), 0)

    def test_word_count_0_len(self):
        self.assertEqual(self.trie.word_count(''), 0)

    def test_word_count(self):
        self.assertEqual(self.trie.word_count('foo'), 0)

    def test_search_0_len(self):
        self.assertEqual(self.trie.search(''), False)

    def test_search(self):
        self.assertEqual(self.trie.search('foo'), False)


class TestTrieWithAddWord(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.trie.add_word('tree')
        self.trie.add_word('trees')
        self.trie.add_word('treaty')
        self.trie.add_word('trie')
        self.trie.add_word('algo')
        self.trie.add_word('assoc')
        self.trie.add_word('all')
        self.trie.add_word('also')
        self.trie.add_word('abbrev')
        self.trie.add_word('beast')
        self.trie.add_word('beast')
        self.trie.add_word('beast')
        self.trie.add_word('z')

    def test_prefix_count_0_len(self):
        self.assertEqual(self.trie.prefix_count(''), 0)

    def test_prefix_count_1_len(self):
        self.assertEqual(self.trie.prefix_count('a'), 5)

    def test_prefix_count_n_len(self):
        self.assertEqual(self.trie.prefix_count('tre'), 3)

    def test_prefix_count_prefix_same_as_word(self):
        self.assertEqual(self.trie.prefix_count('tree'), 2)

    def test_prefix_count_prefix_as_longest_word(self):
        self.assertEqual(self.trie.prefix_count('treaty'), 1)

    def test_prefix_count_prefix_not_found(self):
        self.assertEqual(self.trie.prefix_count('assob'), 0)

    def test_word_count_0_len(self):
        self.assertEqual(self.trie.word_count(''), 0)

    def test_word_count_1_len(self):
        self.assertEqual(self.trie.word_count('z'), 1)

    def test_word_count_single_occurrence(self):
        self.assertEqual(self.trie.word_count('also'), 1)

    def test_word_count_multiple_occurrences(self):
        self.assertEqual(self.trie.word_count('beast'), 3)

    def test_word_count_word_not_found(self):
        self.assertEqual(self.trie.word_count('treat'), 0)
        self.assertEqual(self.trie.word_count('algol'), 0)

    def test_search_0_len(self):
        self.assertEqual(self.trie.search(''), False)

    def test_search_1_len(self):
        self.assertEqual(self.trie.search('z'), True)

    def test_search_1_len_not_found(self):
        self.assertEqual(self.trie.search('u'), False)

    def test_search_single_occurrence(self):
        self.assertEqual(self.trie.search('treaty'), True)

    def test_search_multiple_occurrences(self):
        self.assertEqual(self.trie.search('beast'), True)

    def test_search_word_not_found(self):
        self.assertEqual(self.trie.search('bar'), False)


class TestTrieWithAddWords(TestTrieWithAddWord):
    def setUp(self):
        self.trie = Trie()
        self.trie.add_words(['tree', 'trees', 'treaty', 'trie', 'algo', 'assoc',
                             'all', 'also', 'abbrev', 'beast', 'beast', 'beast',
                             'z'])

if __name__ == '__main__':
    unittest.main()
