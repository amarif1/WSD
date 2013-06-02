#!/usr/bin/python
import sys
import os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)
from wsdlib import Login,getSpanCorpus

def spancorp(username,passwd,word,corp,span=20,step=50,tnum=10,tlag=2):
	try:
		cookie = Login(username,passwd)
	except Exception as e:
		print '[ERROR]:[%s][%s][span20]Unable to login!\n[ERROR]:%s'%(word,corp,str(e))
	try:
		getSpanCorpus(cookie,word,corp,span,step,tnum,tlag)
	except Exception as e:
		print '[ERROR]:[%s][%s][span20]Unable to fetch corpus!\n[ERROR]:%s'%(word,corp,str(e))

def buildcorp(username,passwd,word,span=20,step=50,tnum=10,tlag=2):
    corpora = ['BLOG','DIA','SYN']
    for corpus in corpora:
        spancorp(username,passwd,word,corpus,span,step,tnum,tlag)

uname=sys.argv[1]
pwd=sys.argv[2]
word=sys.argv[3]
corpus=sys.argv[4]
if len(sys.argv)>5:
    span=int(sys.argv[5])
    step=int(sys.argv[6])
    tnum=int(sys.argv[7])
    tlag=int(sys.argv[8])
#   buildcorp(uname,pwd,word,span,step,tnum,tlag)
    spancorp(uname,pwd,word,corpus,span,step,tnum,tlag)
else:
#   buildcorp(uname,pwd,word)
    spancorp(uname,pwd,word,corpus)