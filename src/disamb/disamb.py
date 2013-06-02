import sys,os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)
from wsdlib import disambiguate

disambiguate(sys.argv[1],sys.argv[2],sense='True')