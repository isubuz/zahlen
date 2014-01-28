

class BFS(object):
    def __init__(self, graph, source):
        self.parents = {node: -1 for node in graph.nodes}
        self.level = {node: 0 for node in graph.nodes}
        self.source = source
        self.graph = graph

    def traverse(self):
        """Run BFS on the graph at the source vertex.

        This algorithm is based on the BFS algorithm suggested by Erik Demaine
        in MIT class 6.006, Introduction to Algorithm, 2011.
        The intuition for this algorithm is that at each iteration all vertices
        at a certain "level" is explored.
        Level 0 contains a single vertex which is the source vertex.
        Level 1 contains all the neighbors of the source vertex.
        Level 2 contains all the neighbors of the neighbors of the source
        vertex and so on.
        """

        frontier = [self.source]
        curr_level = 1
        while frontier:
            next_level = []
            for node in frontier:
                for neighbor in self.graph.nodes[node]:
                    if neighbor not in self.level:
                        self.level[neighbor] = curr_level
                        self.parent[neighbor] = node
                        next_level.append(neighbor)
            frontier = next_level
            curr_level += 1

    def print_shortest_path(self, vertex):
        """Print the shortest from the input vertex to the source vertex."""

        path = [vertex]
        while vertex != self.source:
            vertex = self.parent[vertex]
            if vertex == -1:
                path = []
                break
            else:
                path.append(vertex)

        if path:
            print ' -->'.join(path)
        else:
            print 'No path exists'
