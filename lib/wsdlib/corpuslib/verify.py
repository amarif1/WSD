import pickle
import os
corpus_dir = os.getenv("HOME")+'/WSD/data/Corpus/'
def verifyCorpus(directory,count):
	l=0
	err=[]
	k=0
	file_list=os.listdir(directory)#returns list of files
	file_list=map(int,file_list)
	file_list.sort()
	length=len(file_list)
	diff=[file_list[n]-file_list[n-1] for n in range(1,length)]
	file_list=map(str,file_list)
	for i in file_list:
		file=os.path.join(directory,i)
        	text=open(file,'r')
		pick=pickle.load(text)
		l=len(pick)
		if(i==file_list[length-1]):
			x=count-int(i)
			if(x!=l):
				err.append(i);
			break;
		if(l!=diff[k]):
			err.append(i);k=k+1
		text.close()
	return err


def getCorpusLen(tword,corpus):
    directory=corpus_dir+corpus+'/Span20/'+tword
    os.chdir(directory)
    cfile_list=os.listdir('./')
    count = 0
    for cfile in cfile_list:
        pickle_file=open(cfile)
        corpus=pickle.load(pickle_file)
        count += len(corpus)
        pickle_file.close()
    return count

