# -*- coding: utf-8 -*-
"""
@author: FuTianyu
@coauthor: WanZiqian
"""
import copy


def MakeDictionary(edge_list: list):
    """
    input: list of edges list([n0,n1])
    output: dict(node:[neighbor_node]), a.k.a adjacency list of the input edge_list.
    treat the edge_list as a directed graph, allow double edge
    """
    dict_node = dict()  # document the neighbor nodes of the first node in the edge_list

    for i in range(len(edge_list)):
        if edge_list[i][0] not in dict_node:
            dict_node[edge_list[i][0]] = [edge_list[i][1]]
        else:
            # prevent double edge
            # if edge_list[i][1] not in dict_node[edge_list[i][0]]:
            dict_node[edge_list[i][0]].extend([edge_list[i][1]])

    return dict_node


def MakeFullDictionary(edge_list_input: list):
    # Alert: Will Double Edge-List
    # edge_list has to be undirected one-way edge ;
    # e.g if [1,2] in edge_list,then [2,1] can't be in it
    dict_node = dict()  # document the neighbor nodes of the first node in the edge_list
    reverse_edge_list = [[e[1], e[0]] for e in edge_list_input]
    edge_list = copy.deepcopy(edge_list_input)
    edge_list.extend(reverse_edge_list)

    for i in range(len(edge_list)):
        if edge_list[i][0] not in dict_node:
            dict_node[edge_list[i][0]] = [edge_list[i][1]]
        else:
            # prevent double edge
            # if edge_list[i][1] not in dict_node[edge_list[i][0]]:
            dict_node[edge_list[i][0]].extend([edge_list[i][1]])
    return dict_node


if __name__ == "__main__":
    print("nothing")
