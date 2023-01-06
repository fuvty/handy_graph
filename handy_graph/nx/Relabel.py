# Relabel nodes to start from 0

import networkx as nx


def RelabelEdgeListMap(node_set: set, edge_list: list):
    """
    return the mapping of vertices of edge_list
    """
    node_list = list(node_set)
    node_list.sort()
    map = dict(zip(node_list, [i for i in range(len(node_set))]))
    return map


def RelabelEdgeList(node_set: set, edge_list: list):
    """
    return the reordered edge_list
    """
    node_list = list(node_set)
    node_list.sort()
    map = dict(zip(node_list, [i for i in range(len(node_set))]))
    return [(map[e[0]], map[e[1]]) for e in edge_list]


def RelabelNX(graph: nx.Graph) -> nx.Graph:
    """
    return the reordered graph nx
    """
    edge_list = graph.edges
    node_set = set(graph.nodes)
    edge_list = RelabelEdgeList(node_set, edge_list)
    graph_nx = nx.Graph(directed=graph.is_directed())
    graph_nx.add_edges_from(edge_list)
    return graph_nx
