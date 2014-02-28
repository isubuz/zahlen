# -*- coding: utf-8 -*-

"""
    zahlen.algorithms.graph.djikstra
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by Subhajit Ghosh.
    :license: MIT, see LICENSE for more details.
"""

from sys import maxint


class Djikstra(object):
    def __init__(self, graph):
        self.distances = {}
        self.predecessors = {}

        self._graph = graph
        self._queue = None

    def shortest_paths(self, source):
        self._initialize_single_source(source)
        self._queue = SimpleMinQueue[self.distances]
        while self._queue:
            vertex = self._queue.extract_min()
            for edge in vertex.edges:
                self._relax(edge)

    def _initialize_single_source(self, source):
        for vertex in self._graph.vertices:
            self.distances[vertex.key] = maxint
            self.predecessors[vertex.key] = None
        self.distances[source.key] = 0

    def _relax(self, edge):
        source_key = edge.source.key
        target_key = edge.target.key
        weight = edge.weight

        if self.distances[target_key] > self.distances[source_key] + weight:
            self.distances[target_key] = self.distances[source_key] + weight
            self.predecessors[target_key] = source_key


class SimpleMinQueue(object):
    def __init__(self, values):
        self._values = values

    def __len__(self):
        return len(self._values)

    def extract_min(self):
        key, value = min(self._values.items(), key=lambda x: x[1])
        del self._values[key]
        return value

    def update_key(self, key, value):
        if key not in self._values:
            raise Exception('key: {0} not in queue'.format(key))
        self._values[key] = value
