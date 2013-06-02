import pickle

def get_POS_TAGS(infile):
    'returns a list of all POS tags found in a tagged corpus'
    fin=open(infile,"r")
    corpus=pickle.load(fin)
    POS=[]
    for paragraph in corpus:
        for word in paragraph:
            if word[1] not in POS: POS.append(word[1])
    return POS

def get_unique_words(infile,noun=False,verb=False,adjective=False,adverb=False,others=False):
    'returns a set of  all words of a given POS in corpus'
    def addtolist(inlist,item):
        if len(item)==0:return
        item=item.lower()
        inlist.add(item)
    fin=open(infile,"r")
    corpus=pickle.load(fin)
    words=set()
    for paragraph in corpus:
        for word in paragraph:
            if noun==True:
                if word[1] in ('NN','NNS','NP','NPS'):
                    addtolist(words,word[0])
                elif word[1] in ('NP+VBZ','NP+POS','NNS+VBZ','NNS+POS','NN+VHZ','NN+VBZ','NN+POS'):
                    addtolist(words,word[0][:-2])
                elif word[1] in ('NN+VM'):
                    addtolist(words,word[0][:-3])
            if verb==True:
                if word[1] in ('VV','VVZ','VVG','VVP','VVN','VVD','VB','VBZ','VBG','VBP','VBN','VBD','VH','VHZ','VHG','VHP','VHN','VHD'):
                    addtolist(words,word[0])
                elif word[1] in ('VVP+VBZ','NP+VBZ','NNS+VBZ','NN+VHZ','NN+VBZ'):
                    addtolist(words,word[0][:-2])
            if adverb==True:
                if word[1] in ('ADV','ADVC','ADVS','ADVW'):
                    addtolist(words,word[0])
            if adjective==True:
                if word[1] in ('ADJ','ADJC','ADJS'):
                    addtolist(words,word[0])
                elif word[1] in ('ADJ+POS'):
                    addtolist(words,word[0][:-2])
            if others==True:
                if word[1] in ('NUM','CC','CS','DT','DTW','EX','INT','LS','VM','PT','POS','PDT','PP','PP$','PW','PW$','TO'):
                    addtolist(words,word[0])
            if noun==False and verb==False and adverb==False and adjective==False and others==False:
                addtolist(words,word[0])
    return words

def get_word_frequency(infile,noun=False,verb=False,adjective=False,adverb=False,others=False):
    'returns a dictionary of frequency of words(of specified POS) in corpus. Key is the word and value is its frequency'
    def add(frequency_list,item):
        if len(item)==0:return
        item=item.lower()
        if frequency_list.get(item,0)==0:frequency_list[item]=1
        else:frequency_list[item]=frequency_list[item]+1
        return
    fin=open(infile,"r")
    corpus=pickle.load(fin)
    word_frequency={}
    for paragraph in corpus:
        for word in paragraph:
            if noun==True:
                if word[1] in ['NN','NNS','NP','NPS']:
                    add(word_frequency,word[0])
                elif word[1] in ['NP+VBZ','NP+POS','NNS+VBZ','NNS+POS','NN+VHZ','NN+VBZ','NN+POS']:
                    add(word_frequency,word[0][:-2])
                elif word[1] in ['NN+VM']:
                    add(word_frequency,word[0][:-3])
            if verb==True:
                if word[1] in ('VV','VVZ','VVG','VVP','VVN','VVD','VB','VBZ','VBG','VBP','VBN','VBD','VH','VHZ','VHG','VHP','VHN','VHD'):
                    add(word_frequency,word[0])
                elif word[1] in ('VVP+VBZ','NP+VBZ','NNS+VBZ','NN+VHZ','NN+VBZ'):
                    add(word_frequency,word[0][:-2])
            if adverb==True:
                if word[1] in ('ADV','ADVC','ADVS','ADVW'):
                    add(word_frequency,word[0])
            if adjective==True:
                if word[1] in ('ADJ','ADJC','ADJS'):
                    add(word_frequency,word[0])
                elif word[1] in ('ADJ+POS'):
                    add(word_frequency,word[0][:-2])
            if others==True:
                if word[1] in ('NUM','CC','CS','DT','DTW','EX','INT','LS','VM','PT','POS','PDT','PP','PP$','PW','PW$','TO'):
                    add(word_frequency,word[0])
            if noun==False and verb==False and adverb==False and adjective==False and others==False:
                add(word_frequency,word[0])

    return word_frequency


