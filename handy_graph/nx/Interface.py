import networkx as nx
from typing import Union

# convert graphtool, node set edge_list and networkx


def nx2dict(graph: Union[nx.Graph, nx.DiGraph]):
    adj_dict = dict()
    for node in graph.nodes():
        neighbor = [n for n in graph.neighbors(node)]
        neighbor.sort()
        # if len(neighbor) != 0:
        adj_dict[node] = neighbor
    return adj_dict


def nx2csr(graph: nx.Graph):
    """
    convert nx to csr
    """
    adj_dict = nx2dict(graph)
    max_node = max(adj_dict.keys())

    # stupidly iter through
    for v in range(max_node):
        if v not in adj_dict.keys():
            adj_dict[v] = []

    adj_tuple = list(adj_dict.items())
    adj_tuple.sort()

    row_list = []
    neigh_list = []

    iter = 0
    for node, neighs in adj_tuple:
        assert node == iter
        row_list.append(len(neigh_list))
        for neigh in neighs:
            neigh_list.append(neigh)
        iter += 1
    row_list.append(len(neigh_list))

    return row_list, neigh_list


def nx2el(graph: nx.Graph, sort=True):
    if sort:
        edge_list = [(min(e), max(e)) for e in graph.edges]
        edge_list.sort()
    else:
        edge_list = [(e[0], e[1]) for e in graph.edges]
    return edge_list


def el2nx(edge_list: list, directed=False) -> nx.Graph:
    """
    convert edge_list to networkx graphs
    """
    graph = nx.Graph(directed=directed)
    graph.add_edges_from(edge_list)
    return graph


def file2nx(filename: str) -> nx.Graph:
    """
    read edge_list file and convert to networkx graphs
    """
    edge_list = list()

    with open(filename, "r") as f:
        rawlines = f.readlines()
    f.close()

    for line in rawlines:
        if not line.startswith("#"):
            splitted = line.strip("\n").split()
            from_node = int(splitted[0])
            to_node = int(splitted[1])
            edge_list.append((from_node, to_node))

    return el2nx(edge_list)
