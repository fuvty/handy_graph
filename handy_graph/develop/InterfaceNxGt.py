import graph_tool.all as gt
import networkx as nx

from Relabel import RelabelEdgeList

# convert graphtool, node set edge_list and networkx


def nx2el(graph: nx.Graph, sort=True):
    if sort:
        edge_list = [(min(e), max(e)) for e in graph.edges]
        edge_list.sort()
    else:
        edge_list = [(e[0], e[1]) for e in graph.edges]
    return edge_list


def gt2el(graph: gt.Graph, sort=True):
    edge_list = graph.get_edges().tolist()
    if sort:
        edge_list = [(min(e[0], e[1]), max(e[0], e[1])) for e in edge_list]
        edge_list.sort()
    else:
        edge_list = [(e[0], e[1]) for e in edge_list]
    return edge_list


def nx2gt(graph: nx.Graph, sort=True, map=True) -> gt.Graph:
    if sort:
        edge_list = [(min(e), max(e)) for e in graph.edges]
        edge_list.sort()
    else:
        edge_list = [(e[0], e[1]) for e in graph.edges]
    if map:
        node_set = set(graph.nodes)
        edge_list = RelabelEdgeList(node_set, edge_list)
    graph_gt = gt.Graph(directed=graph.is_directed())
    graph_gt.add_edge_list(edge_list)
    return graph_gt


def el2nx(edge_list: list):
    graph = nx.Graph()
    graph.add_edges_from(edge_list)
    return graph


def file2nx(filename: str):
    edge_list = list()

    with open(filename, "r") as f:
        rawlines = f.readlines()
    f.close()

    for line in rawlines:
        splitted = line.strip("\n").split()

        from_node = int(splitted[0])
        to_node = int(splitted[1])

        edge_list.append((from_node, to_node))

    return el2nx(edge_list)
