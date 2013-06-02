import urllib2
import urllib
import os.path
import cookielib
import socket
from retry import retry

data_dir = os.path.dirname(__file__) +'/../../data/'

@retry(socket.error, tries=3, delay=2, backoff=2)
@retry(urllib2.URLError, tries=3, delay=2, backoff=2)
def Login(uname,passwd):
    url = 'https://wse1.webcorp.org.uk/login/seredirect.php'
    values = {'username' : uname,
    	      'password' : passwd }
    data = urllib.urlencode(values)
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(
		urllib2.HTTPRedirectHandler(),
		urllib2.HTTPHandler(debuglevel=0),
		urllib2.HTTPSHandler(debuglevel=0),
		urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [
				('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
						'Windows NT 5.2; .NET CLR 1.1.4322)'))
			]
    print '\nLogging in as %s' % uname
    opener.open(url,data)
    print '\nDone'
    return cookie
