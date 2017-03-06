# -*- coding: utf-8 -*-
# (i) Implement (in any programming language) a bigram and a trigram language model (for
# word sequences), using Laplace smoothing (or better). (ii) Train your models on a training
# subset of a corpus (e.g., from the English or Greek part of Europarl), after replacing all the
# rare words of the training subset (e.g., words that do not occur at least 10 times in the training
# subset) by a special token *rare*. Do not store (during training) counts for the *rare* token
# and n-grams that contain the *rare* token. (iii) Check the log-probabilities that your trained
# models return when given (correct) sentences from the test subset vs. (incorrect) sentences of
# the same length (in words) consisting of randomly selected vocabulary words. Rely on
# smoothing to cope with unknown words in the test subset. (iv) Demonstrate how your models
# could predict the next (vocabulary) word, as in a predictive keyboard (slide 31, center). (v)
# Estimate the language cross-entropy and perplexity of your models on the test subset of the
# corpus. (vi) Optionally combine your two models using linear interpolation (slide 13) and
# check if the combined model performs better. You are allowed to use NLTK
# (http://www.nltk.org/) or other tools for sentence splitting, tokenization, and counting ngrams,
# but otherwise you should write your own code.

#from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import ngrams
from nltk.probability import FreqDist
import codecs
#n will be added by the user
def find_rare(diction):
    for x in diction:
        if diction[x]<5:
            diction[x]= '*rare*'
    return diction

f = codecs.open("europarl.txt","r","utf-8")
europarlg = f.read() #it reads bytes so we wont have a problem with any other language
sentences= [sent for sent in sent_tokenize(europarlg[0:90005])]
words=[word_tokenize(w) for w in sentences]
words = sum(words,[])  
counter ={}
words=[i.lower() for i in words]
for token in words:
    if token not in counter.keys():
        counter[token]= 1
    else:
        counter[token]+=1

#find the occurences of each token

#find and delete rare tokens from dictionary


counter= find_rare(counter)
print counter


