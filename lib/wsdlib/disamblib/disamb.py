import sys,os
lib_dir = os.getenv("HOME")+'/WSD/lib/'
sys.path.append(lib_dir)
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import networkx as nx
import os
from wsdlib import find_root_hubs

data_dir = os.getenv("HOME")+'/WSD/data/'
mst_dir=data_dir+'MST/'

def extract_words(tword,context):
    'Returns the filtered set of words in the given context'
    def addtolist(inlist,target_word,item):
       	item=item.lower()
        item=lmtzr.lemmatize(item)
       	if item not in inlist and item!=target_word and item not in stopwords:
       	    inlist.append(item)
    stopwords=set(['time','secondly', 'all', 'whoever', 'imho', 'edu', 'go', 'evermore', 'causes', 'seemed', 'whose', 'certainly', "when's", 'vs', 'to', 'th', 'under', 'sorry', "a's", 'far', 'every', 'yourselves', 'did', 'fewer', 'someday', 'http', 'yourself', 'past', 'second', 'notwithstanding', 'further', 'even', 'what', 'sub', 'brief', 'HTML', 'goes', 'sup', 'new', 'ever', 'full', "c'mon", 'never', 'here', 'let', 'others', 'alone', 'along', 'IMAP', 'ahead', 'k', 'allows', 'usually', 'whereupon', 'makes', 'thats', 'hither', 'via', 'regardless', 'merely', 'while', 'till', 'ninety', 'viz', 'everybody', 'from', 'would', 'contains', 'next', 'few', 'therefore', 'themselves', 'thru', 'until', 'more', 'becomes', 'hereby', 'herein', 'everywhere', 'particular', "who'll", 'must', 'me', 'none', 'this', 'getting', 'anywhere', 'nine', 'can', 'mr', 'my', 'give', 'neverf', 'something', 'want', 'needs', 'end', 'rather', 'meanwhile', 'how', 'low', 'instead', 'okay', 'may', 'after', 'them', 'hereupon', 'whilst', 'such', 'a', 'whenever', 'maybe', 'ones', 'so', 'allow', 'things', 'indeed', 'over', 'move', 'soon', 'course', 'through', 'still', 'its', 'before', 'thence', 'selves', 'inward', 'actually', 'better', 'ours', 'might', 'versus', 'then', 'non', 'someone', 'somebody', 'thereby', 'ownpart', 'they', 'half', 'front', 'now', 'nor', 'gets', 'hereafter', 'always', 'reasonably', 'whither', 'each', "mustn't", 'everyone', 'eg', 'ex', 'our', 'beyond', 'out', "needn't", 'furthermore', 'since', 'rd', 're', 'got', 'cause', 'thereupon', 'given', 'quite', "what'll", 'que', 'besides', 'anyhow', 'BTW', 'could', 'thing', 'ltd', 'hence', 'onto', 'already', 'seeming', "youa'd", 'thereafter', 'one', 'another', 'says', 'little', 'ASP', 'top', 'least', 'anyone', 'their', 'too', 'gives', 'mostly', 'behind', 'nobody', 'regards', 'somewhat', 'believe', 'herself', 'than', 'gotten', 'zero', 'i', 'amid', 'toward', 'anyways', 'and', 'alongside', 'beforehand', 'say', 'have', 'need', 'seen', 'seem', 'saw', 'any', 'latter', 'that', 'downwards', 'aside', 'also', 'which', 'begin', 'exactly', 'unless', 'shall', 'who', 'most', 'but', 'nothing', 'why', 'forever', 'Hypertext', 'later', 'mrs', 'neverless', 'came', 'saying', 'particularly', 'show', 'anyway', 'ending', 'outside', 'should', 'only', 'going', "there've", 'his', 'hit', 'above', 'get', 'overall', "oughtn't", 'cannot', 'nearly', 'during', 'him', 'regarding', 'qv', 'she', 'contain', "what've", 'where', 'theirs', 'see', 'are', "that've", 'no-one', 'best', 'wonder', 'said', "there'd", 'away', 'please', 'enough', 'various', 'between', 'probably', 'neither', 'across', 'co.', 'available', 'we', 'recently', 'were', 'however', 'come', 'both', 'last', 'many', 'whereafter', 'according', 'against', 'etc', 'became', 'MOO', 'com', 'comes', 'otherwise', 'among', 'presumably', 'co', 'afterwards', 'seems', 'whatever', 'hers', 'moreover', 'throughout', 'meantime', 'due', 'been', 'whom', "there're", 'much', 'hardly', "it'd", 'wants', 'latterly', 'else', 'former', 'those', 'myself', 'these', 'near', 'almost', 'wherever', 'is', 'thus', 'it', 'cant', 'itself', 'in', 'ie', 'if', 'containing', 'perhaps', 'insofar', 'make', 'FAQ', 'same', 'wherein', 'beside', 'several', 'somewhere', 'upon', 'yours', 'recent', 'lower', 'off', 'whereby', 'nevertheless', 'whole', 'well', 'anybody', 'obviously', 'without', 'very', 'the', 'self', 'inc.', 'lest', 'just', 'less', 'being', 'when', 'not', 'farther', 'yet', 'unto', 'had', 'except', 'has', 'adj', 'ought', "t's", 'around', 'possible', 'whichever', 'apart', 'necessary', 'either', 'become', 'whomever', 'towards', 'therein', "why's", 'because', 'old', 'often', 'some', 'back', 'sure', 'ourselves', 'for', 'though', 'per', 'everything', 'be', "mightn't", 'nowhere', 'although', 'by', 'on', 'about', 'ok', 'anything', 'oh', 'of', 'v', 'side', 'whence', 'plus', 'or', 'seeing', 'own', 'formerly', 'into', 'within', 'three', 'down', 'right', 'couldnt', 'your', "how's", 'her', 'there', 'amidst', 'accordingly', 'inner', 'forward', 'was', 'himself', 'elsewhere', "i've", 'becoming', 'amongst', 'somehow', 'hi', 'with', 'he', 'whether', 'inside', 'up', 'us', 'below', 'un', 'empty', 'gone', 'sometimes', 'certain', 'am', 'an', 'as', 'sometime', 'at', 'et', 'inc', 'again', 'hasnt', 'no', 'whereas', 'nd', 'lately', 'other', 'you', 'really', 'upwards', 'ago', 'together', 'having', 'once','home','menu','link','http','state','pm','lot','year'])
    lmtzr = WordNetLemmatizer()
    text=nltk.word_tokenize(context)
    tword=tword.lower()
    tagged_text=nltk.pos_tag(text)
    words=[]
    for each_word in tagged_text:
            if each_word[1] in ('NN','NNS','NNP','NNPS','JJ','JJR','JJS'):
                addtolist(words,tword,each_word[0])
    return words


def disambiguate(tword,context,sense=False):
    path=mst_dir+tword+".graphml"
    G=nx.read_graphml(path)
    words=extract_words(tword,context)
    print '\n\nExtracted words:',words,'\n\n'  
    roothub=G.neighbors(tword)
    print 'Root hubs:',roothub,'\n\n'
    count_roothub=len(roothub)
    print 'Root hub count:',count_roothub,'\n\n'
    nodes=G.nodes()
    score_vector_sum=[]
    i=0
    for i in range(count_roothub):
         score_vector_sum.insert(i,0)
    
    words_found=[]
    for each_word in words:
        if each_word in nodes:
            words_found.append([each_word,G.node[each_word]['roothub']])
            root_hub=G.node[each_word]['roothub']
            pos=roothub.index(root_hub)
            #print each_word,'    Roothub- ',root_hub,'   Postion-',pos
            score_vector_sum[pos]=score_vector_sum[pos]+G.node[each_word]['score']

    if len(words_found)==0:
        print 'Insufficient information\n'
        return
        
    max_value=max(score_vector_sum)
    pos=score_vector_sum.index(max_value)
    print words_found,'\n\n'
    print 'Roothub:',roothub[pos],'\n\n'
    #print roothub[pos]
    #print 'Neighbors:\n\n',G.neighbors(roothub[pos]),'\n\n'
    if sense:
        print 'Sense:',G.node[roothub[pos]]['meaning']
  
