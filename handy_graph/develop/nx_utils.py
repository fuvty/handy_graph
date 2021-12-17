from typing import List
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from numpy import ceil
import csv
import numpy as np

def draw_nxgraphs(graphs: List[nx.Graph], outpath= "tmp.jpg", nrows= 2):
    ncols = int(ceil(len(graphs)/nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25,10))
    ax = axes.flatten()

    for i,graph in enumerate(graphs):
        # node_color = [ 'red' if anchor==1 else 'blue' for anchor in nx.get_node_attributes(graph, 'anchor').values() ]
        pos = nx.circular_layout(graph)
        nx.draw(graph, ax=ax[i], with_labels=True, pos=pos)
        # ax[i].title.set_text('count='+str(counts[i]))
    plt.suptitle(str(datetime.now().strftime("%D - %H:%M:%S")))
    plt.savefig(outpath)

def draw_adjmatrix(graphs: List[nx.Graph], outpath= "tmp.jpg", nrows= 2):
    ncols = int(ceil(len(graphs)/nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25,10))
    ax = axes.flatten()

    for i,graph in enumerate(graphs):
        edges = np.array(graph.edges)
        ax[i].scatter(edges[:,0], edges[:,1])
    plt.suptitle(str(datetime.now().strftime("%D - %H:%M:%S")))
    plt.savefig(outpath)

def draw_adjmatrix_edge(edge_lists: List[nx.Graph], outpath= "tmp.jpg", nrows= 2):
    ncols = int(ceil(len(edge_lists)/nrows))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25,10))
    ax = axes.flatten()
    for i,edges in enumerate(edge_lists):
        edges = np.array(edges)
        ax[i].scatter(edges[:,1], edges[:,0], s=1)
        ax[i].set_aspect('equal', 'box')
    plt.suptitle(str(datetime.now().strftime("%D - %H:%M:%S")))
    plt.savefig(outpath)

def get_degree_distribution(graphs: List[nx.Graph], draw= False, to_csv= False) -> List[List[int]]:
    '''
    get the degree of all nodes in graph in descending order
    '''
    degrees = []
    for graph in graphs:
        degree = [graph.degree[v] for v in graph.nodes]
        degree.sort(reverse= True)
        degrees.append(degree)
    if draw:
        outname = "tmp"
        nrows = 1
        ncols = int(ceil(len(graphs)/nrows))
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(25,10))
        ax = axes.flatten()
        for i in range(len(graphs)):
            degree = degrees[i]
            x = [i for i in range(len(degree))]
            y = degree
            plt.plot(x, y)
        plt.savefig(outname+".jpg")
    if to_csv:
        with open(outname+".csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerows(degrees)
    return degrees