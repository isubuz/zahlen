from collections import defaultdict


class Graph(object):
    def __init__(self):
        self.nodes = defaultdict(list)

    def __str__(self):
        graph_str = []
        for node in self.nodes:
            graph_str.append('{0} --> {1}'.format(node, self.nodes[node]))

        return '\n'.join(graph_str)

    def add_edge(self, source, target):
        if target not in self.nodes:
            self.nodes[target] = []
        self.nodes[source].append(target)

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(*edge)
