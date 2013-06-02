import json
import urllib
import re
from retry import retry
import urllib2
import socket
#import binascii

def asciirepl(match):
  s = match.group()
  return '\\u00' + match.group()[2:]

@retry(socket.error, tries=3, delay=2, backoff=2)
@retry(urllib2.URLError, tries=3, delay=2, backoff=2)
def getForms(tword):
    p = urllib.urlopen('http://www.google.com/dictionary/json?callback=a&q='+tword+'&sl=en&tl=en&restrict=pr,de&client=te')
    page = p.read()[2:-10] #As its returned as a function call
    #To replace hex characters with ascii characters
    p = re.compile(r'\\x(\w{2})')
    ascii_string = p.sub(asciirepl, page)

    #Now decoding cleaned json response
    data = json.loads(ascii_string)
    qset=set()
    qset.add(tword)
    prim = data['primaries']
    for i in prim:
        term=i['terms'][0]['text']
        qset.add(term.encode("ascii", "ignore").lower())
        if i['entries'][0]['type'] == 'related':
            forms=i['entries'][0]['terms']
            for form in forms:
                qset.add(form['text'].encode("ascii", "ignore").lower())
    return qset

def getQuery(tword):
    qset = getForms(tword)
    query='['+qset.pop()
    while qset:
        query+='|'+qset.pop()
    query+=']'
    return query