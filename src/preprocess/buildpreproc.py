#!/usr/bin/python
import os
import pickle
import sys
lib_dir=os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)

from wsdlib import extract_words_thread, createDir, getForms
data_dir=os.getenv("HOME")+'/WSD/data/'
preproc_dir = data_dir+'/Preprocessed'

def write_filtered_pickle(target_word):
    forms=getForms(target_word)
    corpus_dir=data_dir+"Corpus/"
    combined_corpus=[]
    for corpus in ['SYN','DIA','BLOG']:
        try:
            directory_path=corpus_dir+corpus+'/Span20/'+target_word
            combined_corpus+=extract_words_thread(directory_path,forms)
        except IOError as e:
            print 'Error in%s:%s'%(corpus,str(e))
    createDir(preproc_dir)
    fout=open(target_word,"w")
    pickle.dump(combined_corpus,fout)
    fout.close()

tword=sys.argv[1]
write_filtered_pickle(tword)