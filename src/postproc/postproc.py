#!/usr/bin/python
import sys,os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)
from wsdlib import  convert_to_nx, find_root_hubs, create_mst, assign_scores, write_mst, createDir,clean_graph, reduce_root_hubs
data_dir = os.getenv("HOME")+'/WSD/data/'
graph_dir = data_dir+'/Graph/'
mst_dir=data_dir+'/MST/'

def postprocess(target_word):
	graphml_path=graph_dir+target_word+'.graphml'
	word_graph=convert_to_nx(graphml_path)
	new_graph=clean_graph(word_graph)
	root_hubs=find_root_hubs(new_graph)
	reduced_root_hubs=reduce_root_hubs(new_graph,root_hubs,2)
	word_mst=create_mst(new_graph,target_word,reduced_root_hubs)
	assign_scores(word_mst,reduced_root_hubs,target_word)
	createDir(mst_dir)
	mst_path=mst_dir+target_word+'.graphml'
	write_mst(word_mst,mst_path)

postprocess(sys.argv[1])
