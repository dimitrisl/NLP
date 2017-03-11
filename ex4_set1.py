# -*- coding: utf-8 -*-
# (iii) Check the log-probabilities that your trained models return when given (correct)
# sentences from the test subset vs. (incorrect) sentences of the same length (in words)
# consisting of randomly selected vocabulary words. Rely on
# smoothing to cope with unknown words in the test subset.
# (iv) Demonstrate how your models
# could predict the next (vocabulary) word, as in a predictive keyboard (slide 31, center). (v)
# Estimate the language cross-entropy and perplexity of your models on the test subset of the
# corpus. (vi) Optionally combine your two models using linear interpolation (slide 13) and
# check if the combined model performs better. You are allowed to use NLTK
# (http://www.nltk.org/) or other tools for sentence splitting, tokenization, and counting ngrams,
# but otherwise you should write your own code.
from math import log
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import ngrams
import codecs
def find_rare(diction):
    for x in diction:
        if diction[x]<10:
            diction[x]= '*rare*'
    return diction

f = codecs.open("europarl.txt","r","utf-8")
europarlg = f.read() #it reads bytes so we wont have a problem with any other language
sentences= [sent for sent in sent_tokenize(europarlg[0:100000])]
words=[word_tokenize(w) for w in sentences]
words = sum(words,[])  
counter ={}
words=[i.lower() for i in words]
for token in words:
    if token not in counter.keys():
        counter[token]= 1
    else:
        counter[token]+=1 #find the occurences of each token
counter= find_rare(counter) #find and delete rare tokens from dictionary
counter["#start1"]=1
counter["#start2"]=1
valid_unigrams = []
valid_bigrams = []
valid_trigrams = []

for i in words:
    if counter[i]!="*rare*":
        valid_unigrams.append(i)

bigrams = ngrams(["#start1"]+words,2)
for x,y in bigrams:
    if counter[x]!="*rare*" and counter[y]!="*rare*":
        if valid_bigrams == []:
            if x!="#start1":
                valid_bigrams.append(("#start1",x))
                valid_bigrams.append((x,y))
        else:
            valid_bigrams.append((x,y))

trigrams = ngrams(["#start1","#start2"]+words,3)
for x,y,z in trigrams:
    if counter[x]!="*rare*" and counter[y]!="*rare*" and counter[z]!="*rare*":
        if valid_trigrams == []:
            if x!="start1":
                valid_trigrams.append(("#start1","#start2",x))
                valid_trigrams.append(("#start2",x,y))
                valid_trigrams.append((x,y,z))
        else:
            valid_trigrams.append((x,y,z))

print "the distinct words are {0}".format(len(set(valid_unigrams))) , "and the valid unigrams",len(valid_unigrams)

print "valid trigrams",len(valid_trigrams),"valid bigrams",len(valid_bigrams),"and words {0}".format(len(words))

lpuni = {}
for i in set(valid_unigrams):
    lpuni[i] = log((valid_unigrams.count(i)+1)/(float(len(words)+len(set(valid_unigrams)))))
lpbi = {}
for i in set(valid_bigrams):
    lpbi[i] = log((valid_bigrams.count(i)+1)/(float(len(words)+len(set(valid_unigrams)))))
lptri = {}
for i in set(valid_trigrams):
    lptri[i] = log((valid_trigrams.count(i)+1)/(float(len(valid_bigrams)+len(set(valid_bigrams)))))
