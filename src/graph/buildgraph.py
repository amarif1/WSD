#!/usr/bin/python
import sys,os
lib_dir=os.getenv("HOME")+'/WSD/lib'
sys.path.append(lib_dir)
from wsdlib import createGraph


tword=sys.argv[1]
if len(sys.argv)>2:
    minabsfreq=int(sys.argv[2])
    mincofreq=int(sys.argv[3])
    contextlen=int(sys.argv[4])
    createGraph(tword,minabsfreq,mincofreq,contextlen)
else:
    createGraph(tword)