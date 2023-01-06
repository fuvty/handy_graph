# Relabel nodes to start from 0

import graph_tool.all as gt
import networkx as nx
from networkx.generators import directed


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


def RelabelGT(graph: gt.Graph) -> gt.Graph:
    """
    return the reordered graph gt
    """
    edge_list = graph.get_edges().tolist()
    node_set = set(graph.get_vertices())
    edge_list = RelabelEdgeList(edge_list)
    graph_gt = gt.Graph(graph.is_directed())
    graph_gt.add_edge_list(edge_list)
    return graph_gt


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
