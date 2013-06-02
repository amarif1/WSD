from bs4 import BeautifulSoup
import urllib2
import pickle
import os
import bleach
import socket
import re
import threading
import time
from count import getTotCount
from retry import retry
from query import getQuery
from directory import createDir


data_dir = os.getenv("HOME")+'/WSD/data/'

@retry(socket.error, tries=3, delay=2, backoff=2)
@retry(urllib2.URLError, tries=3, delay=2, backoff=2)
def getChunk(cookie,tword,corp,span,start,step,totcount):
	if corp == 'BLOG':
		url = 'http://wse1.webcorp.org.uk/cgi-bin/'+corp+'/results.cgi?q='+tword+',english-any,0,0,0-0-0&span='+str(span)+'&limit=0&pos=1&step='+str(step)+'&info=num&start='+str(start)
	else:
		url = 'http://wse1.webcorp.org.uk/cgi-bin/'+corp+'/results.cgi?q='+tword+',any,0,0,0-0-0&span='+str(span)+'&limit=0&pos=1&step='+str(step)+'&info=num&start='+str(start)
	opener = urllib2.build_opener(
   		urllib2.HTTPRedirectHandler(),
   		urllib2.HTTPHandler(debuglevel=0),
   		urllib2.HTTPSHandler(debuglevel=0),
   		urllib2.HTTPCookieProcessor(cookie))
	opener.addheaders = [
	 	        ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
       	                   'Windows NT 5.2; .NET CLR 1.1.4322)'))
       		]
	print '\n[%s][%s][span%s][%s][%s:%s][page open]Start'% (tword,corp,span,totcount,start,step)
	response = opener.open(url)
	html = response.read()
	print '\n[%s][%s][span%s][%s][%s:%s][page open]Done'% (tword,corp,span,totcount,start,step)
	print '\n[%s][%s][span%s][%s][%s:%s][extraction]Start'% (tword,corp,span,totcount,start,step)
	html=html.replace('</BODY','')
	soup = BeautifulSoup(html)
	tables = soup.find('table',width=True)
	rows = tables.findAll('tr')
	count=0
	sentences=list()
	for row in rows:
		txt = row.td.nextSibling
		clean_txt = bleach.clean(txt, tags=[], strip=True)
		txt = txt.nextSibling
		clean_txt+= bleach.clean(txt, tags=[], strip=True)
		txt = txt.nextSibling
		clean_txt+= bleach.clean(txt, tags=[], strip=True)
		tokens = re.findall(r'\w[\w.:\'-/]+{[\w+$]+}',clean_txt)
		tagged=[]
		for words in tokens:
			word,pos = words.strip('}').split('{')
			tagged.append((word,pos))
		sentences.append(tagged)
		count+=1
	if count != step:
		if count+start != totcount:
			raise socket.error
	print '\n[%s][%s][span%s][%s][%s:%s][extraction]Done'% (tword,corp,span,totcount,start,step)
	print '\n[%s][%s][span%s][%s][%s:%s][save file]Start'% (tword,corp,span,totcount,start,step)
	pickle_file = open(str(start).zfill(6),'w')
	pickle.dump(sentences,pickle_file)
	pickle_file.close()
	print '\n[%s][%s][span%s][%s][%s:%s][save pickle]Done'% (tword,corp,span,totcount,start,step)

def threadChunks(cookie,word,corp,span,start,end,step,totcount,tlag):
	if end > totcount:
		end = totcount
	threads=list()
	for i in range(start,end,step):
		t = threading.Thread(target=getChunk,args=(cookie,word,corp,span,i,step,totcount))
		threads.append(t)
		t.start()
		time.sleep(tlag)
	for thread in threads:
		thread.join()

def getSpanCorpus(cookie,tword,corp,span,step,tnum,tlag):
    word=getQuery(tword)
    print '\n[%s][%s][span%s][corpus fetch]Start'% (word,corp,span)
    totcount=getTotCount(cookie,word,corp,span)
    word_dir = data_dir+'/Corpus/'+corp+'/Span'+str(span)+'/'+tword
    createDir(word_dir)
    file_list = sorted(map(int,os.listdir('./')),reverse=True)
    if not file_list:
        start=0
    else:
        step=int(file_list[0])-int(file_list[1])
        start=int(file_list[0])+step
    size=tnum*step
    for i in range(start,totcount,size):
        threadChunks(cookie,word,corp,span,i,i+size,step,totcount,tlag)
    print '\n[%s][%s][span%s][%s][corpus fetch]Done'% (word,corp,span,totcount)








