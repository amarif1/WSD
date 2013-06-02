import urllib2
import sys,os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)
from bs4 import BeautifulSoup
from retry import retry

def populateWord(login_cookie,word,corp,span=20):
    'Function to populate the search query'
    url = 'http://wse1.webcorp.org.uk/cgi-bin/'+corp+'/types.cgi?from_index=from_index&lang=english&qf=&q='+word+'&dom=any&sent=0&f=&f_type=0&concord=Get+Concordances&min_freq=&show_num='
    opener = urllib2.build_opener(
    	urllib2.HTTPRedirectHandler(),
    	urllib2.HTTPHandler(debuglevel=0),
    	urllib2.HTTPSHandler(debuglevel=0),
    	urllib2.HTTPCookieProcessor(login_cookie))
    opener.addheaders = [
    	        ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        	]
    print '\n[%s][%s][span%s][search population]Start'% (word,corp,span)
    opener.open(url,timeout=10)
    if corp == 'BLOG':
		url = 'http://wse1.webcorp.org.uk/cgi-bin/'+corp+'/search.cgi?q='+word+',english-any,0,0,0-0-0'
    else:
		url = 'http://wse1.webcorp.org.uk/cgi-bin/'+corp+'/search.cgi?q='+word+',any,0,0,0-0-0'
    opener.open(url,timeout=10)
    print '\n[%s][%s][span%s][search population]Done'% (word,corp,span)

@retry(Exception, tries=10, delay=2, backoff=2)
def getTotCount(cookie,word,corp,span=20):
    'Function to retrieve total number of available contexts for a query'
    populateWord(cookie,word,corp,span)
    print '\n[%s][%s][span%s][count fetch]Start'% (word,corp,span)
    if corp == 'BLOG':
		url='http://wse1.webcorp.org.uk/cgi-bin/'+corp+'/progress.cgi?q='+word+',english-any,0,0,0-0-0'
    else:
        url='http://wse1.webcorp.org.uk/cgi-bin/'+corp+'/progress.cgi?q='+word+',any,0,0,0-0-0'
    opener = urllib2.build_opener(
	 		urllib2.HTTPRedirectHandler(),
    		urllib2.HTTPHandler(debuglevel=0),
    		urllib2.HTTPSHandler(debuglevel=0),
    		urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [
	        	('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                       	'Windows NT 5.2; .NET CLR 1.1.4322)'))
	    	]
    response = opener.open(url)
    html=response.read()
    response = opener.open(url)
    html=response.read()
    soup=BeautifulSoup(html)
    totCount = int(soup.find("body").find("p").find("b").renderContents())
    print '\n[%s][%s][span%s][count fetch]Done'% (word,corp,span)
    return totCount