#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:03:58 2020

@author: futianyu
"""

from typing import Tuple, List, Set
from networkx.classes.function import selfloop_edges
from networkx.generators import directed
from scipy.io import mmread
from scipy.sparse.coo import coo_matrix
import scipy.sparse as sparse
import networkx as nx


def ReadMtxFile(file: str) -> Tuple[List, Set]:
    mtx = mmread(file)
    shape_x, shape_y = mtx.shape
    if shape_x < shape_y:
        zeros = coo_matrix((shape_y-shape_x, shape_y))
        mtx = sparse.vstack([mtx,zeros], dtype= mtx.dtype)
    if shape_x > shape_y:
        zeros = coo_matrix((shape_x, shape_x-shape_y))
        mtx = sparse.hstack([mtx,zeros], dtype= mtx.dtype)

    mtx = nx.from_scipy_sparse_matrix(mtx)
    graph = nx.Graph(directed= False)
    graph.add_edges_from(mtx.edges)
    graph.remove_edges_from(nx.selfloop_edges(graph))
    nx.selfloop_edges(graph)

    return [e for e in graph.edges], {n for n in graph.nodes}
    # raise NotImplementedError



# read edge list and sort in ascending order
def ReadEdgeFile(file:str, Edge_list: list, nodes:set):
    '''
    read edge list and sort in ascending order
    '''
    with open(file, 'r') as f:
        rawlines = f.readlines()
    f.close()  

    for line in rawlines:
        if not line.startswith("#"):
            splitted = line.strip('\n').split()

            from_node = int(splitted[0])
            to_node   = int(splitted[1])
            
            nodes.add(from_node)
            nodes.add(to_node)

            Edge_list.append([from_node, to_node])

    num_E = len(Edge_list)
    
    # to make the first node smaller than the second in every edge
    for j in range(num_E): 
        if Edge_list[j][0]>Edge_list[j][1]:
            t = Edge_list[j][0]
            Edge_list[j][0] = Edge_list[j][1]
            Edge_list[j][1] = t
    

    # sort the edges
    Edge_list = sorted(Edge_list,key=lambda x:(x[0],x[1])) 
    
    print('GraphFileIO: edge_num of the whole graph is',len(Edge_list))
    print('GraphFileIO: node_num of the graph is',len(nodes))

def WriteEdgeList(filename: str, Edge_list: list):
    '''
    write list of edges to file. e.g.
    0 1
    0 2
    1 2
    '''
    num_E = len(Edge_list)
    print('GraphFileIO: write edge of the whole graph is',num_E)

    with open(filename, 'x') as f:
        for edge in Edge_list:
            f.write( str(edge[0])+" "+str(edge[1])+"\n" )
    f.close()

def WriteAdjList(filename: str, adj_dict: dict):
    '''
    write adj list to file. Note that the key of dict myst be continues. Each line is the adj_list of a node. e.g
    1 2
    2
    '''
    num_N = len(adj_dict)
    assert sorted(adj_dict.keys()) == list(range(num_N)) # make sure the key is consecutive
    print('GraphFileIO: write node of the whole graph is',num_N)

    adj_list = [sorted(adj_dict[i]) for i in range(num_N)]

    with open(filename, 'w') as f:
        for adj_nodes in adj_list:
            for node in adj_nodes:
                f.write(str(node)+str(' '))
            f.write('\n')
    f.close()


if __name__=='__main__':
    edge_list, node_set = ReadMtxFile("/home/futy18/data/graph_data/mtx_list/econ-beaflw.mtx")
    WriteEdgeList("/home/futy18/data/graph_data/edge_list/econ-beaflw.txt", edge_list)