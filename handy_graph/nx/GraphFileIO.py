#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:03:58 2020

@author: futianyu
"""

from typing import Any, Optional, Tuple, List, Set, Union
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
def ReadEdgeFile(file: str, edge_list: List = None, node_set: Set = None) -> Optional[Tuple[List, Set]]:
    '''
    Read edge list and sort in ascending order.
    If edge_list and node_set is given, increamental add is used with inplace replacement.
    If not, return new edge_list and node_set
    '''
    with open(file, 'r') as f:
        rawlines = f.readlines()
    f.close()  

    if (edge_list == None) and (node_set == None):
        incremental = False
        edge_list = list()
        node_set = set()
    elif (edge_list != None) and (node_set != None):
        incremental = True
    else:
        print("GraphFileIO: Either both edge_list and node_set are not given or both are given")
        raise NotImplementedError

    for line in rawlines:
        if not line.startswith("#"):
            splitted = line.strip('\n').split()

            from_node = int(splitted[0])
            to_node   = int(splitted[1])
            
            node_set.add(from_node)
            node_set.add(to_node)

            edge_list.append([from_node, to_node])

    num_E = len(edge_list)
    
    # to make the first node smaller than the second in every edge
    # for j in range(num_E): 
    #     if edge_list[j][0]>edge_list[j][1]:
    #         t = edge_list[j][0]
    #         edge_list[j][0] = edge_list[j][1]
    #         edge_list[j][1] = t
    
    # sort the edges
    edge_list = sorted(edge_list,key=lambda x:(x[0],x[1])) 
    
    print('GraphFileIO: edge_num of the whole graph is',len(edge_list))
    print('GraphFileIO: node_num of the graph is',len(node_set))

    if not incremental:
        return (edge_list, node_set)

def WriteEdgeList(filename: Union[str, Any], Edge_list: List[Union[List, Tuple]], first_line: str = None) -> None:
    '''
    write list of edges to file. e.g.
    (optional) first_line
    0 1
    0 2
    1 2
    '''
    num_E = len(Edge_list)
    print('GraphFileIO: write edge of the whole graph is',num_E)

    with open(filename, 'w') as f:
        if first_line:
            f.write(first_line)
            if first_line[-1] != '\n':
                f.write('\n')
        for edge in Edge_list:
            f.write( str(edge[0])+" "+str(edge[1])+"\n" )
    f.close()

def WriteLabeledGraph(filename: Union[str, Any], graph: nx.Graph, node_label_key: str = None) -> None:
    '''
    write labeled graphs to file. the format is defined by https://github.com/RapidsAtHKUST/SubgraphMatching; e.g.
    t N M
    v VertexID LabelId Degree
    ...
    e VertexId VertexId
    ...
    '''
    num_N = len(graph.nodes)
    num_E = len(graph.edges)
    print('GraphFileIO: write node of the whole graph is',num_N)
    print('GraphFileIO: write edge of the whole graph is',num_E)

    with open(filename, 'w') as f:
        f.write('t '+str(num_N)+' '+str(num_E)+'\n')
        for node in sorted(graph.nodes):
            if node_label_key:
                f.write('v '+str(node)+' '+str(int(graph.nodes[node][node_label_key]))+' '+str(int(graph.degree(node)))+'\n')
            else:
                f.write('v '+str(node)+' '+str(0)+' '+str(graph.degree(node))+'\n')
        for edge in sorted(graph.edges):
            f.write('e '+str(edge[0])+' '+str(edge[1])+'\n')
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

