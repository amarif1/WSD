from __future__ import division
from operator import itemgetter
import sys,os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)

import networkx as nx
from mst import prim_mst

def convert_to_nx(infile):
    'Converts a graphml file into Networkx graph'
    return nx.read_graphml(infile)

def clean_graph(word_graph,min_neighbors=6):
    'Removes the isolated components of word_graph that will not be part of any cluster'
    word_graph_copy=word_graph.copy()
    subgraph_list=nx.connected_component_subgraphs(word_graph)
    for each_component in subgraph_list:
        vertices=sorted(each_component.degree_iter(),key=itemgetter(1),reverse=True)
        highest_degree_vertex=vertices[0]
        if highest_degree_vertex[1]<min_neighbors:
            nodes=each_component.nodes()
            word_graph_copy.remove_nodes_from(nodes)
    return word_graph_copy

def find_root_hubs(word_graph,min_neighbors=6,max_avg_weight=0.8):
    'Returns the root hubs of word graph. Parameters for a candidate root hub are min_neighbors and max_avg_weight'
    word_graph_copy=word_graph.copy()
    root_hubs=[]
    while True:
        vertices=sorted(word_graph_copy.degree_iter(),key=itemgetter(1),reverse=True)
        if not vertices:
            break
        vertex=vertices[0]
        if vertex[1]>=min_neighbors:
            neighbors_list=word_graph_copy.neighbors(vertex[0])
            neighbors_subgraph = word_graph_copy.subgraph(neighbors_list)
            neighbors = sorted(neighbors_subgraph.nodes(data=True),key=lambda x:x[1]['freq'],reverse=True)
            avg_weight=0
            for i in range(0,min_neighbors):
                avg_weight += word_graph_copy.get_edge_data(vertex[0],neighbors[i][0])['weight']
            avg_weight/=min_neighbors
            if avg_weight < max_avg_weight:
                root_hubs.append(vertex)
                word_graph_copy.remove_nodes_from(neighbors_list)
                if not word_graph_copy.nodes():
                    break
            word_graph_copy.remove_node(vertex[0])
        else:
            break
    return root_hubs

                                                                                                                                                                                                                               
def reduce_root_hubs(word_graph,root_hubs,count=5):
    stop_words=['pm','state']
    filtered_root_hubs=list()
    for root_hub in root_hubs:              #filter stop words
        if root_hub[0] not in stop_words:
            filtered_root_hubs.append(root_hub)

    checked_root_hubs=list()
    hub_dist=list()
    for hub1 in filtered_root_hubs:                  #find the most dissimilar root hubs
        for hub2 in filtered_root_hubs:
            if hub1[0]!=hub2[0] and hub2[0] not in checked_root_hubs:
                if nx.has_path(word_graph,hub1[0],hub2[0]):
                    dist,hop=nx.shortest_path_length(word_graph,hub1[0],hub2[0],weight='weight'),nx.shortest_path_length(word_graph,hub1[0],hub2[0])
                    deg_sum = hub1[1]*hub2[1]
                    hub_dist.append([(hub1[0],hub2[0]),hub1[1],hub2[1],dist*dist*(deg_sum)*hop])
        checked_root_hubs.append(hub1[0])
    degsum_dist2_hop=sorted(hub_dist,key=itemgetter(3),reverse=True)

    reduced_root_hubs=set()
    for each_pair in degsum_dist2_hop:
        reduced_root_hubs.add((each_pair[0][0],each_pair[1]))
        reduced_root_hubs.add((each_pair[0][1],each_pair[2]))
        if len(reduced_root_hubs)>=count:break
    return reduced_root_hubs



def create_mst(word_graph,target_word,root_hubs):
    'Builds minimum spanning tree from word graph. The children of target_word in MST represents the root hubs'
    for hub in root_hubs:
        word_graph.add_edge(target_word,hub[0],weight=0)
    mst=prim_mst(word_graph,target_word)
    #neighbours=mst.neighbors(target_word)
    #print neighbours
    return mst

def assign_scores(mst,root_hubs,target_word):
    'Assign scores and roothub to all nodes(other than target_word) in the MST'
    nodes=mst.nodes()
    nodes.remove(target_word)
    mst_copy=mst.copy()
    mst_copy.remove_node(target_word)
    for node in nodes:
        for root_hub in root_hubs:
            if nx.has_path(mst_copy,root_hub[0],node):
                 distance_to_hub=nx.shortest_path_length(mst_copy, source=node, target=root_hub[0], weight='weight')
                 node_score=1/(1+distance_to_hub)
       	         mst.add_node(node,score=node_score,roothub=root_hub[0])
                 break
    return mst


def write_mst(mst,path):
    'Converts the networkx MST into graphml file'
    nx.write_graphml(mst,path)
    return

