#!/usr/bin/python
import sys
import os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)
from wsdlib import Login,getTotCount, getCorpusLen
corpus_dir = os.getenv("HOME")+'/WSD/data/Corpus/Span20'

def corpusLen(uname,passwd,tword):
    cookie=Login(uname,passwd)
    totcount=0
    fetchcount=0
    for corpus in ['BLOG','DIA','SYN']:
        totcount+=getTotCount(cookie,tword,corpus,verbose=False)
        fetchcount+=getCorpusLen(tword,corpus)
    print '[%s][Total Count]%s' %(tword,totcount)
    print '[%s][Feched Count]%s' %(tword,totcount)


uname=sys.argv[1]
passwd=sys.argv[2]
tword=sys.argv[3]
corpusLen(uname,passwd,tword)


