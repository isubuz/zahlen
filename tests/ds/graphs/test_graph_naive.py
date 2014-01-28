from zahlen.ds.graph.naive_graph import Graph
import unittest


class TestGraphCreation(unittest.TestCase):

    def test_nodes_after_add_edge(self):
        """Test that nodes are added after calls to add_edge()."""

        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 1)
        graph.add_edge(2, 5)
        graph.add_edge(3, 4)

        nodes = [node for node in graph.nodes]
        nodes.sort()

        self.assertEqual(nodes, [1, 2, 3, 4, 5])

    def test_nodes_after_add_edges(self):
        """Test that nodes are added after add_edges() is called."""

        graph = Graph()
        graph.add_edges([(1, 2), (1, 3), (2, 1), (2, 5), (3, 4)])

        nodes = [node for node in graph.nodes]
        nodes.sort()

        self.assertEqual(nodes, [1, 2, 3, 4, 5])


if __name__ == '__main__':
    unittest.main()
