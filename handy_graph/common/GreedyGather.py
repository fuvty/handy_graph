#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Feb 24 2021

@author: Tianyu Fu
"""

from typing import Dict, List, Tuple


def GreedyGather(Node_set: set, Edge_list: list, offset = 0) -> Tuple[List[List], Dict]:
    '''
    Relabel node index using greedy gather of edges.
    inputs: node set; edge list; offset: the number of the first output node label
    outputs: gathered edge list; the node mapping dictionary
    '''
    num_N = len(Node_set)
    accPoint = offset
    index = {key:-1 for key in Node_set}
    for edge in Edge_list:
        n0 = edge[0]
        n1 = edge[1]
        if index[n0] == -1:
            index[n0] = accPoint
            accPoint = accPoint + 1
        if index[n1] == -1:
            index[n1] = accPoint
            accPoint = accPoint + 1
    Edge_list_new = list()
    node_map = dict()
    for edge in Edge_list:
        n0 = edge[0]
        n1 = edge[1]
        i0 = index[n0]
        i1 = index[n1]
        node_map[n0] = i0
        node_map[n1] = i1
        if i0==-1 or i1==-1:
            print("GreedyGather: reindex error")
        Edge_list_new.append( [i0,i1] )

    return Edge_list_new, node_map


if __name__ == '__main__':
    from GraphFileIO import  ReadEdgeFile, WriteEdgeList

    Node_set = set()
    Edge_list = list()
    ReadEdgeFile("/home/futy18/data/graph_data/edge_list/citeseer.txt", Edge_list, Node_set)
    Edge_list_new, node_map = GreedyGather(Node_set, Edge_list)

    # WriteEdgeList("/home/futy18/data/graph_data/greedyGather_edge_list/citeseer.txt", Edge_list_new)
    print("done")
