from typing import List
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
from datetime import datetime
from numpy import ceil
import csv
import numpy as np
from typing import Union


def draw_nxgraphs(graphs: List[nx.Graph], outpath="tmp.jpg", nrows=2):
    ncols = int(ceil(len(graphs) / nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25, 10))
    ax = axes.flatten()

    for i, graph in enumerate(graphs):
        # node_color = [ 'red' if anchor==1 else 'blue' for anchor in nx.get_node_attributes(graph, 'anchor').values() ]
        pos = nx.circular_layout(graph)
        nx.draw(graph, ax=ax[i], with_labels=True, pos=pos)
        # ax[i].title.set_text('count='+str(counts[i]))
    plt.suptitle(str(datetime.now().strftime("%D - %H:%M:%S")))
    plt.savefig(outpath)


def draw_adjmatrix(graph: nx.Graph, outpath="tmp.jpg", figsize=(20, 20)):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    edges = np.array(graph.edges)
    ax.scatter(edges[:, 0], edges[:, 1])
    ax.title.set_text(outpath.split(".")[0:-2])
    plt.gca().invert_yaxis()
    plt.savefig(outpath)


def draw_adjmatricies(graphs: List[nx.Graph], outpath="tmp.jpg", nrows=2):
    ncols = int(ceil(len(graphs) / nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25, 10))
    ax = axes.flatten()

    for i, graph in enumerate(graphs):
        edges = np.array(graph.edges)
        ax[i].scatter(edges[:, 0], edges[:, 1])
    plt.suptitle(str(datetime.now().strftime("%D - %H:%M:%S")))
    plt.savefig(outpath)


def draw_adjmatrix_edge(edge_lists: List[List], outpath="tmp.jpg", nrows=2):
    ncols = int(ceil(len(edge_lists) / nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25, 10))
    ax = axes.flatten()
    for i, edges in enumerate(edge_lists):
        edges = np.array(edges)
        ax[i].scatter(edges[:, 1], edges[:, 0], s=1)
        ax[i].set_aspect("equal", "box")
    plt.suptitle(str(datetime.now().strftime("%D - %H:%M:%S")))
    plt.savefig(outpath)


def get_degree_distribution(
    graphs: List[nx.Graph], draw=False, to_csv=False
) -> List[List[int]]:
    """
    get the degree of all nodes in graph in descending order
    """
    degrees = []
    for graph in graphs:
        degree = [graph.degree[v] for v in graph.nodes]
        degree.sort(reverse=True)
        degrees.append(degree)
    if draw:
        outname = "tmp"
        nrows = 1
        ncols = int(ceil(len(graphs) / nrows))
        _, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25, 10))
        _ = axes.flatten()
        for i in range(len(graphs)):
            degree = degrees[i]
            x = [i for i in range(len(degree))]
            y = degree
            plt.plot(x, y)
        plt.savefig(outname + ".jpg")
    if to_csv:
        with open(outname + ".csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(degrees)
    return degrees


class DynamicAdjMatrix:
    def __init__(self, fig_size_x, fig_size_y, graph_size, marker_size) -> None:
        self.fig_size_x = fig_size_x
        self.fig_size_y = fig_size_y
        self.fig, self.ax = plt.subplots(
            nrows=1, ncols=1, figsize=(self.fig_size_x, self.fig_size_y)
        )
        self.edge_lists = []
        self.graph_size = graph_size
        self.marker_size = marker_size
        plt.xlim(0, self.graph_size)
        plt.ylim(0, self.graph_size)
        plt.gca().invert_yaxis()

    def __call__(self, i):
        self.scat.set_offsets(self.edge_lists[i])
        self.ax.set_title(str(i))
        return (self.scat,)

    def __len__(self):
        return len(self.edge_lists)

    def init_graph(self):
        # self.ax.invert_yaxis()
        self.scat = self.ax.scatter([], [], s=self.marker_size)
        return (self.scat,)

    def add_graph(self, graph: Union[nx.Graph, nx.DiGraph]):
        if not graph.is_directed():
            graph = graph.to_directed()
        edges = np.array(graph.edges).reshape(-1, 2)
        self.edge_lists.append(edges)

    def save_animation(self, fps: int, path, name):
        anim = animation.FuncAnimation(
            self.fig,
            self.__call__,
            frames=len(self.edge_lists),
            blit=True,
            repeat_delay=1000,
            init_func=self.init_graph,
        )
        anim.save(path + "/" + name + ".gif", animation.FFMpegWriter(fps=fps))
