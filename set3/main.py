from spacy.en import English
from nltk.tokenize import sent_tokenize
from collections import Counter
from languagemodel import *
from spelling_corrector import levenstein


nlp = English()
with open('europarl.txt', 'r') as f:
    content = f.read()

sentences = [sent for sent in sent_tokenize(content[0:200000].decode('utf-8'))]
words = [str(token) for sent in sentences for token in nlp(sent, 'utf-8')]
lexicon = Counter(words)
lexicon = find_rare(lexicon)
logprob_bigrams={}
bigrams, logprob_bigrams = lpbigrams(words, lexicon)

print levenstein('the',lexicon)
