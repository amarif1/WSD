from __future__ import division
import pickle
import sys,os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)
import networkx as nx
from wsdlib import createDir

data_dir = os.getenv("HOME")+'/WSD/data/'
preproc_dir = data_dir+'/Preprocessed/'
graph_dir = data_dir+'/Graph/'

def createGraph(target_word,minabsfreq=10,mincofreq=5,contextlen=4):
    corpus_file = open(preproc_dir+'/'+target_word)
    corpus = pickle.load(corpus_file)
    abs_freq_table={}
    for context in corpus:
        for word in context:
            if  not abs_freq_table.get(word,False):
                abs_freq_table[word]=1
            else :
                abs_freq_table[word]+=1

    collection=[]
    for context in corpus:
        words=[]
        for word in context:
            if abs_freq_table[word]>= minabsfreq :
                words.append(word)
        collection.append(words)
    del corpus

    filtered_collection=[]
    for context in collection:
        if len(context)>=contextlen:
            filtered_collection.append(context)
    del collection

    co_freq_table={}
    for context in filtered_collection:
        for word in context:
            if not co_freq_table.get(word,False):
                co_freq_table[word]=[1,{}]
            else :
                co_freq_table[word][0]+=1
            for otherword in context:
                if otherword==word:
                	continue
                if not co_freq_table[word][1].get(otherword,False):
                    co_freq_table[word][1][otherword]=1
                else :
                    co_freq_table[word][1][otherword]+=1
    G=nx.Graph()
    for word in co_freq_table.keys():
        w_freq = co_freq_table[word][0]
        n_dict = co_freq_table[word][1]
        n_list=n_dict.keys()
        for neighbor in n_list:
            if n_dict[neighbor] >= mincofreq:
                n_freq = co_freq_table[neighbor][0]
                co_freq = n_dict[neighbor]
                pab=co_freq/n_freq
                pba=co_freq/w_freq
                weight=1-max(pab,pba)
                if weight<=.9:
                    G.add_edge(word,neighbor,weight=weight,freq=co_freq)
                    G.node[neighbor]['freq'] = n_freq
                    G.node[word]['freq'] = w_freq
    createDir(graph_dir)
    nx.write_graphml(G,target_word+'.graphml')