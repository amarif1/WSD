# Word Sense Disambiguation

Word sense disambiguation (WSD) is the task of selecting the appropriate senses of a word in a given context. It is essence of communication 
in natural language. It is motivated by its use in many crucial applications such as Information retrieval, Information extraction, Machine 
Translation, Part of Speech tagging, etc. Various issues like scalability, ambiguity, diversity (of languages) and evaluation pose challenges to WSD solutions.

Véronis, J. (2004) had proposed an innovative unsupervised algorithm for word sense disambiguation based on small-world graphs called HyperLex. We extend this work by optimizing the free parameters and mapping the induced senses to a standard lexicon (WordNet). Also we adapt this algorithm, which was originally designed to tackle WSD problems in information retrieval systems, as a human language disambiguation aid.

A large corpus for the target word was extracted from Web and it was clustered following Hyperlex algorithm. The resulting graph was further analyzed. Even from the wide junk of data, the small world property was found to hold. But the performance was poor with regard to commercial applications.Hence we had to modify various parameters and apply further consolidation techniques. The resultant system provided around 87% accuracy on real world data. Also mapping the clusters into senses found in standard lexicon was done by hand.

The resultant graph for each word contributes to a wide knowledge base that can be used to study and to analyze the real world occurrences and patterns in the language.

### Architecture
![alt text](https://github.com/amarif1/WSD/blob/master/architecture.png "Architecture")


### Python dependencies
* NLTK
* NetworkX
* Numpy
* BeautifulSoup4
* Bleach
* PyEnchant

### Contributors:
* [Muhammad Arif](https://github.com/amarif1)
* [Nafseer K](https://github.com/nafseerk)
* [Alphy Elsa Sebastian](https://github.com/alphyelsa)
* [Krishna Priya M](https://github.com/krishnamuraleedharan)
