import os

def createDir(f):
    try:
        os.makedirs(f)
        os.chdir(f)
    except OSError:
        os.chdir(f)
        pass
