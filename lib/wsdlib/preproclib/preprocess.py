import sys,os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)

from nltk.stem.wordnet import WordNetLemmatizer
import threading
import enchant
import pickle
import Queue

def extract_unique_words(infile,target_word_list,noun=False,verb=False,adjective=False,adverb=False,others=False,verbose=False):
    'Returns a list of lists where each inner list contains all unique words(of specified POS) as (word,POS) tuple in the corresponding paragraph of the corpus'
    'Filtering Applied:- 1)lemmatization,2)checking in dictionary, 3)stopwords elimination'
    if verbose==True:print 'Fetching pickle from file:',infile
    def addtolist(inlist,target_word_list,item):
        if len(item)==0:return
        item=item.lower()
        item=lmtzr.lemmatize(item)
        if item not in target_word_list and item not in stopwords and dictionary.check(item)==True:
            inlist.add(item)
    lmtzr = WordNetLemmatizer()
    dictionary=enchant.Dict('en_US')
    stopwords=set(['time','secondly', 'all', 'whoever', 'imho', 'edu', 'go', 'evermore', 'causes', 'seemed', 'whose', 'certainly', "when's", 'vs', 'to', 'th', 'under', 'sorry', "a's", 'far', 'every', 'yourselves', 'did', 'fewer', 'someday', 'http', 'yourself', 'past', 'second', 'notwithstanding', 'further', 'even', 'what', 'sub', 'brief', 'HTML', 'goes', 'sup', 'new', 'ever', 'full', "c'mon", 'never', 'here', 'let', 'others', 'alone', 'along', 'IMAP', 'ahead', 'k', 'allows', 'usually', 'whereupon', 'makes', 'thats', 'hither', 'via', 'regardless', 'merely', 'while', 'till', 'ninety', 'viz', 'everybody', 'from', 'would', 'contains', 'next', 'few', 'therefore', 'themselves', 'thru', 'until', 'more', 'becomes', 'hereby', 'herein', 'everywhere', 'particular', "who'll", 'must', 'me', 'none', 'this', 'getting', 'anywhere', 'nine', 'can', 'mr', 'my', 'give', 'neverf', 'something', 'want', 'needs', 'end', 'rather', 'meanwhile', 'how', 'low', 'instead', 'okay', 'may', 'after', 'them', 'hereupon', 'whilst', 'such', 'a', 'whenever', 'maybe', 'ones', 'so', 'allow', 'things', 'indeed', 'over', 'move', 'soon', 'course', 'through', 'still', 'its', 'before', 'thence', 'selves', 'inward', 'actually', 'better', 'ours', 'might', 'versus', 'then', 'non', 'someone', 'somebody', 'thereby', 'ownpart', 'they', 'half', 'front', 'now', 'nor', 'gets', 'hereafter', 'always', 'reasonably', 'whither', 'each', "mustn't", 'everyone', 'eg', 'ex', 'our', 'beyond', 'out', "needn't", 'furthermore', 'since', 'rd', 're', 'got', 'cause', 'thereupon', 'given', 'quite', "what'll", 'que', 'besides', 'anyhow', 'BTW', 'could', 'thing', 'ltd', 'hence', 'onto', 'already', 'seeming', "youa'd", 'thereafter', 'one', 'another', 'says', 'little', 'ASP', 'top', 'least', 'anyone', 'their', 'too', 'gives', 'mostly', 'behind', 'nobody', 'regards', 'somewhat', 'believe', 'herself', 'than', 'gotten', 'zero', 'i', 'amid', 'toward', 'anyways', 'and', 'alongside', 'beforehand', 'say', 'have', 'need', 'seen', 'seem', 'saw', 'any', 'latter', 'that', 'downwards', 'aside', 'also', 'which', 'begin', 'exactly', 'unless', 'shall', 'who', 'most', 'but', 'nothing', 'why', 'forever', 'Hypertext', 'later', 'mrs', 'neverless', 'came', 'saying', 'particularly', 'show', 'anyway', 'ending', 'outside', 'should', 'only', 'going', "there've", 'his', 'hit', 'above', 'get', 'overall', "oughtn't", 'cannot', 'nearly', 'during', 'him', 'regarding', 'qv', 'she', 'contain', "what've", 'where', 'theirs', 'see', 'are', "that've", 'no-one', 'best', 'wonder', 'said', "there'd", 'away', 'please', 'enough', 'various', 'between', 'probably', 'neither', 'across', 'co.', 'available', 'we', 'recently', 'were', 'however', 'come', 'both', 'last', 'many', 'whereafter', 'according', 'against', 'etc', 'became', 'MOO', 'com', 'comes', 'otherwise', 'among', 'presumably', 'co', 'afterwards', 'seems', 'whatever', 'hers', 'moreover', 'throughout', 'meantime', 'due', 'been', 'whom', "there're", 'much', 'hardly', "it'd", 'wants', 'latterly', 'else', 'former', 'those', 'myself', 'these', 'near', 'almost', 'wherever', 'is', 'thus', 'it', 'cant', 'itself', 'in', 'ie', 'if', 'containing', 'perhaps', 'insofar', 'make', 'FAQ', 'same', 'wherein', 'beside', 'several', 'somewhere', 'upon', 'yours', 'recent', 'lower', 'off', 'whereby', 'nevertheless', 'whole', 'well', 'anybody', 'obviously', 'without', 'very', 'the', 'self', 'inc.', 'lest', 'just', 'less', 'being', 'when', 'not', 'farther', 'yet', 'unto', 'had', 'except', 'has', 'adj', 'ought', "t's", 'around', 'possible', 'whichever', 'apart', 'necessary', 'either', 'become', 'whomever', 'towards', 'therein', "why's", 'because', 'old', 'often', 'some', 'back', 'sure', 'ourselves', 'for', 'though', 'per', 'everything', 'be', "mightn't", 'nowhere', 'although', 'by', 'on', 'about', 'ok', 'anything', 'oh', 'of', 'v', 'side', 'whence', 'plus', 'or', 'seeing', 'own', 'formerly', 'into', 'within', 'three', 'down', 'right', 'couldnt', 'your', "how's", 'her', 'there', 'amidst', 'accordingly', 'inner', 'forward', 'was', 'himself', 'elsewhere', "i've", 'becoming', 'amongst', 'somehow', 'hi', 'with', 'he', 'whether', 'inside', 'up', 'us', 'below', 'un', 'empty', 'gone', 'sometimes', 'certain', 'am', 'an', 'as', 'sometime', 'at', 'et', 'inc', 'again', 'hasnt', 'no', 'whereas', 'nd', 'lately', 'other', 'you', 'really', 'upwards', 'ago', 'together', 'having', 'once','home','menu','link','http'])
    fin=open(infile,"r")
    corpus=pickle.load(fin)
    collection=[]
    for paragraph in corpus:
        words=set()
        for word in paragraph:
            if noun==True:
                if word[1] in ['NN','NNS','NP','NPS']:
                    addtolist(words,target_word_list,word[0])
                elif word[1] in ['NP+VBZ','NP+POS','NNS+VBZ','NNS+POS','NN+VHZ','NN+VBZ','NN+POS']:
                    addtolist(words,target_word_list,word[0][:-2])
                elif word[1] in ['NN+VM']:
                    addtolist(words,target_word_list,word[0][:-3])
            if verb==True:
                if word[1] in ('VV','VVZ','VVG','VVP','VVN','VVD','VB','VBZ','VBG','VBP','VBN','VBD','VH','VHZ','VHG','VHP','VHN','VHD'):
                    addtolist(words,target_word_list,word[0])
                elif word[1] in ('VVP+VBZ','NP+VBZ','NNS+VBZ','NN+VHZ','NN+VBZ'):
                    addtolist(words,target_word_list,word[0][:-2])
            if adverb==True:
                if word[1] in ('ADV','ADVC','ADVS','ADVW'):
                    addtolist(words,target_word_list,word[0])
            if adjective==True:
                if word[1] in ('ADJ','ADJC','ADJS'):
                    addtolist(words,target_word_list,word[0])
                elif word[1] in ('ADJ+POS'):
                    addtolist(words,target_word_list,word[0][:-2])
            if others==True:
                if word[1] in ('NUM','CC','CS','DT','DTW','EX','INT','LS','VM','PT','POS','PDT','PP','PP$','PW','PW$','TO'):
                    addtolist(words,target_word_list,word[0])
            if noun==False and verb==False and adverb==False and adjective==False and others==False:
                addtolist(words,target_word_list,word[0])
        collection.append(words)
        del words
    fin.close()
    return collection


def extract_words_seq(file_list,target_word_list,queue):
    'Calls extract_unique_words on all files in the file list sequentially'
    result=list()
    for each_file in file_list:
        result+=extract_unique_words(each_file,target_word_list,noun=True,adjective=True)
    queue.put(result)


def extract_words_thread(directory,target_word_list,nthreads=10,verbose=False):
    'Calls extract_words_seq on files in the directory parallelly'
    os.chdir(directory)
    all_files=sorted(os.listdir('./'))
    tot_file_count=len(all_files)
    if tot_file_count<nthreads:
        chunk_count=tot_file_count
    else:
        chunk_count = int(tot_file_count/nthreads)
    file_chunks = [all_files[i:i+chunk_count] for i in range(0, tot_file_count, chunk_count)]
    threads=list()
    q=Queue.Queue()
    result=list()
    for chunk in file_chunks:
        t=threading.Thread(extract_words_seq(chunk,target_word_list,q))
        threads.append(t)
        if verbose==True:print 'Starting ',t
        t.start()
    for thrd in threads:
        if verbose==True:print 'Quitting ',t
        thrd.join()
        result+=q.get()
    return result

