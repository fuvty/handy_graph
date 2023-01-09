"""
Example file on how to draw adjacent matrix animation to represent dynamic graphs with handy_graph
"""

from handy_graph.develop.nx_utils import DynamicAdjMatrix
import networkx as nx
import random


def random_reorder(graph: nx.Graph, seed=0):
    random.seed(seed)
    random_seq = [(v, random.random()) for v in graph.nodes]
    random_seq.sort(key=lambda x: x[1], reverse=True)
    node_mapping = {seq[0]: i for i, seq in enumerate(random_seq)}
    graph = nx.relabel_nodes(graph, node_mapping, copy=True)
    return node_mapping, graph


def main():
    graph = nx.graph_atlas(105)
    dam = DynamicAdjMatrix(
        fig_size_x=10, fig_size_y=10, graph_size=len(graph), marker_size=200
    )
    for i in range(10):
        _, graph = random_reorder(graph, i)
        dam.add_graph(graph)
    dam.save_animation(fps=3, path=".", name="atlas_105")


main()
