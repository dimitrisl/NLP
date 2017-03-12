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
def find_rare(diction):#find and delete rare tokens from dictionary
    for x in diction:
        if diction[x]<10:
            diction[x]="*rare*"
    return diction

def lpunigrams(valid_unigrams, words):#log probabilities for unigrams
    lpuni = {}
    for i in set(valid_unigrams):
        lpuni[i] = log((valid_unigrams.count(i)+1)/(float(len(words)+len(set(valid_unigrams)))))
    return lpuni
def lpbigrams(valid_unigrams, valid_bigrams,words):#log probabilities for bigrams
    lpbi = {}
    for (x,y) in set(valid_bigrams):
        lpbi[(x,y)] = log((valid_bigrams.count((x,y))+1)/(float((valid_unigrams.count(x))+len(set(valid_unigrams)))))
    return lpbi
def lptrigrams (valid_trigrams, valid_bigrams):#log probabilities for trigrams
    lptri = {}
    for (x,y,z) in set(valid_trigrams):
        lptri[(x,y,z)] = log((valid_trigrams.count((x,y,z))+1)/(float((valid_bigrams.count((x,y)))+len(set(valid_bigrams)))))
    return lptri
def count_occur(words, counter): #find the occurences of each token
    words=[i.lower() for i in words]
    for token in words:
        if token not in counter.keys():
            counter[token]= 1
        else:
            counter[token]+=1
    return counter

f = codecs.open("europarl.txt","r","utf-8")
europarl = f.read() #it reads bytes so we wont have a problem with any other language
sentences= [sent for sent in sent_tokenize(europarl[0:100000])]
words=[word_tokenize(w) for w in sentences]
words = sum(words,[])  
counter={}
counter= count_occur(words, counter)
counter= find_rare(counter)

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

#print "the distinct words are {0}".format(len(set(valid_unigrams))) , "and the valid unigrams",len(valid_unigrams)

#print "valid trigrams",len(valid_trigrams),"valid bigrams",len(valid_bigrams),"and words {0}".format(len(words))

#test 

b = codecs.open("europarl.txt","r","utf-8")
test_europarl = b.read() #it reads bytes so we wont have a problem with any other language
test_sentences= [sent for sent in sent_tokenize(test_europarl[100010:110015])]
test_words=[word_tokenize(w) for w in test_sentences]
test_words = sum(test_words,[])  
test_counter={}
test_counter= count_occur(test_words, test_counter)

test_unigrams = []
test_bigrams = []
test_trigrams = []
test_counter["#start1"]=1
test_counter["#start2"]=1

for i in test_words:
    test_unigrams.append(i)

tbigrams = ngrams(["#start1"]+test_words,2)
for x,y in tbigrams:
        if test_bigrams == []:
            if x!="#start1":
                test_bigrams.append(("#start1",x))
                test_bigrams.append((x,y))
        else:
            test_bigrams.append((x,y))

ttrigrams = ngrams(["#start1","#start2"]+test_words,3)
for x,y,z in ttrigrams:
        if test_trigrams == []:
            if x!="start1":
                test_trigrams.append(("#start1","#start2",x))
                test_trigrams.append(("#start2",x,y))
                test_trigrams.append((x,y,z))
        else:
            test_trigrams.append((x,y,z))
print test_trigrams