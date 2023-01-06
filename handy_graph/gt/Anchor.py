import graph_tool.all as gt
import networkx as nx
import numpy as np
from tqdm import tqdm
import pickle

from Interface import nx2gt
from Relabel import RelabelNX


def GenAnchor(subgraph: nx.Graph, graph: nx.Graph, method="random") -> tuple[int, int]:
    """
    input: subgraph and graph
    output: subgraph anchor and graph anchor
    Note that graph must be relabeled by Relabel.RelabelNX to ensure no isolated point exists
    """
    # convert to gt
    subgraph = nx2gt(subgraph, sort=False, map=False)
    graph = nx2gt(graph, sort=False, map=False)

    # check the mapping of subgraph
    vmaps = gt.subgraph_isomorphism(subgraph, graph, induced=True)
    # pick the anchor from vmaps
    if len(vmaps) == 0:
        print(subgraph.vertices(), subgraph.get_edges().tolist())
        print(graph.vertices(), graph.get_edges().tolist())
        raise RuntimeError
    subgraph_anchor, graph_anchor = map2anchors(vmaps, subgraph, method=method)

    return subgraph_anchor, graph_anchor


def GenVMap(subgraph: nx.Graph, graph: nx.Graph) -> list[map]:
    """
    input: subgraph and graph in nx.graph
    output: vmaps
    Note that graphs must be relabeled by Relabel.RelabelNX to ensure no isolated point exists
    """
    # convert to gt
    subgraph = nx2gt(subgraph, sort=False, map=False)
    graph = nx2gt(graph, sort=False, map=False)

    # check the mapping of subgraph
    vmaps = gt.subgraph_isomorphism(subgraph, graph, induced=True)

    # map from subgraph to graph, v_sub: v_graph
    maps = []
    for vmap in vmaps:
        map = dict(
            (zip(list(subgraph.get_vertices()), [vmap[v] for v in subgraph.vertices()]))
        )
        maps.append(map)

    return maps


def map2anchors(vmaps, subgraph: gt.Graph, method="random"):
    """
    input: vmaps generate by gt.subgraph_isomorphism()
    output: subgraph_anchor, graph_anchor
    """
    vmap = vmaps[0]
    # map from subgraph to graph, v_sub: v_graph
    map = dict(
        (zip(list(subgraph.get_vertices()), [vmap[v] for v in subgraph.vertices()]))
    )

    # choose anchor
    if method == "random":
        # randomly pick one
        subgraph_anchor = list(map.keys())[0]
    elif method == "largest_degree":
        # pick node with largest degree in subgraph
        degrees = subgraph.get_out_degrees(subgraph.get_vertices())
        index = np.argmax(degrees)
        subgraph_anchor = list(map.keys())[index]
    elif method == "smallest_degree":
        # pick node with smallest degree in subgraph
        degrees = subgraph.get_out_degrees(subgraph.get_vertices())
        index = np.argmin(degrees)
        subgraph_anchor = list(map.keys())[index]

    graph_anchor = map[subgraph_anchor]
    return subgraph_anchor, graph_anchor


def relabelMotifs():
    """
    example on how to use RelabelNX to treat nx object before using GenAnchor
    """
    range = 1000
    with open("playground/vars/" + str(range) + "/motifs", "rb") as f:
        motifs = pickle.load(f)

    motifs = [RelabelNX(m) for m in motifs]

    with open("playground/vars/" + str(range) + "/motifs", "wb") as f:
        pickle.dump(motifs, f, pickle.HIGHEST_PROTOCOL)


def genAnchorMatrix():
    """
    example on how to generate anchorMatrix.
    call relabelMotifs first
    motifs in vars are relabeled
    """
    import pickle

    data_range = 100
    method = "smallest_degree"

    lessSMatrix = np.load("playground/vars/" + str(data_range) + "/lessSMatrix.npy")
    matrix_shape = lessSMatrix.shape
    anchorMarix = np.empty(shape=(matrix_shape[0], matrix_shape[1], 2))
    anchorMarix[:] = np.NaN

    with open("playground/vars/" + str(data_range) + "/motifs", "rb") as f:
        motifs = pickle.load(f)

    for i in tqdm(range(matrix_shape[0])):
        for j in range(matrix_shape[1]):
            if lessSMatrix[i, j] == 1:
                subgraph_anchor, graph_anchor = GenAnchor(
                    motifs[i], motifs[j], method=method
                )
                anchorMarix[i, j, 0] = subgraph_anchor
                anchorMarix[i, j, 1] = graph_anchor

    np.save(
        "playground/vars/" + str(data_range) + "/anchorMatrix." + method, anchorMarix
    )


if __name__ == "__main__":
    genAnchorMatrix()
    """
    graph = nx.Graph(directed = False)
    graph.add_edges_from([(0,1),(0,2),(1,2),(2,3)])

    subgraph1 = nx.Graph(directed = False)
    subgraph1.add_edges_from([(0,1),(0,2)])

    subgraph_anchor, graph_anchor = GenAnchor(subgraph1,graph)

    print("done")
    """
