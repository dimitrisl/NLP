from spacy.en import English
from nltk.tokenize import sent_tokenize
from collections import Counter
from languagemodel import *
from spelling_corrector import viterbidecoder


nlp = English()
with open('europarl.txt', 'r') as f:
    content = f.read()

sentences = ['#start0 #start1 '+sent for sent in sent_tokenize(content[0:200000].decode('utf-8'))]
words = [str(token) for sent in sentences for token in nlp(sent, 'utf-8')]
lexicon = Counter(words)
lexicon = find_rare(lexicon)
logprob_bigrams = {}
bigrams, logprob_bigrams = lpbigrams(words, lexicon)
given_sentence = "#start0 #start1 You hve requstd a debte on ths sject in the crse of the nxt few days, dng this pt-session."
print ("The sentence given was"+given_sentence)
correct, b = viterbidecoder(given_sentence, lexicon, logprob_bigrams)
print ("THe sentence returned is " + correct)
