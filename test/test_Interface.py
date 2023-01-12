import networkx as nx
from typing import Union

from handy_graph.nx import nx2dict


def gen_graphs():
    """
    generate a graph and a digraph for testing
    """
    edge_list = [(1, 2), (2, 3), (1, 3), (3, 1), (3, 4), (4, 5), (5, 1)]
    node_list = [0, 1, 2, 3, 4, 5, 6]

    graph = nx.Graph()
    graph.add_nodes_from(node_list)
    graph.add_edges_from(edge_list)

    digraph = nx.DiGraph()
    digraph.add_nodes_from(node_list)
    digraph.add_edges_from(edge_list)

    return graph, digraph


def test_nx2dict():
    """
    Test nx2dict function
    """

    def _test_nx2dict(test_graph: Union[nx.Graph, nx.DiGraph], adj_list: dict = None):
        _dict = nx2dict(test_graph)
        assert _dict == adj_list

    graph, digraph = gen_graphs()
    graph_adj_list = {
        0: [],
        1: [2, 3, 5],
        2: [1, 3],
        3: [1, 2, 4],
        4: [3, 5],
        5: [1, 4],
        6: [],
    }
    digraph_adj_list = {0: [], 1: [2, 3], 2: [3], 3: [1, 4], 4: [5], 5: [1], 6: []}

    _test_nx2dict(graph, graph_adj_list)
    _test_nx2dict(digraph, digraph_adj_list)
