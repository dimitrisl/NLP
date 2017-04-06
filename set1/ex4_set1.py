# -*- coding: utf-8 -*-
# (vi) Optionally combine your two models using linear interpolation (slide 13) and
# check if the combined model performs better. You are allowed to use NLTK
# (http://www.nltk.org/) or other tools for sentence splitting, tokenization, and counting ngrams,
# but otherwise you should write your own code.
from math import log #this is the log of e
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import ngrams
import codecs
import random

def random_sentences(length,words):
    w_sentence = []
    for j in range(length):
        w_sentence.append(random.choice(words))
    w_sentence = " ".join(w_sentence)
    return w_sentence

def cross_entropy(dictionary):
    sm = 0
    for i in dictionary:
        sm += dictionary[i]
    sm = (-1)*(sm/len(dictionary.keys()))
    return sm

def prob_creator(sentence,n,laplace,vocabulary):
    new_probability = 0
    to_tokens = word_tokenize(sentence)
    number_of_tokens = len(to_tokens)
    to_grams = ngrams(to_tokens, n)
    for i in to_grams:
        if i in laplace.keys():
            new_probability += laplace[i]
        else:
            new_probability += log(1/float(vocabulary))
    return (number_of_tokens,new_probability)

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

b = codecs.open("europarl.txt","r","utf-8", errors='ignore')
europarl = b.read() #it reads bytes so we wont have a problem with any other language
sentences= [sent for sent in sent_tokenize(europarl[0:200000])]
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
   if counter[i.lower()]!="*rare*":
       valid_unigrams.append(i)

bigrams = ngrams(words,2)
for x,y in bigrams:
    if counter[x.lower()]!="*rare*" and counter[y.lower()]!="*rare*":
        if valid_bigrams == []:
            valid_bigrams.append(("#start1",x))
            valid_bigrams.append((x,y))
        else:
            valid_bigrams.append((x,y))
trigrams = ngrams(words,3)
for x,y,z in trigrams:
    if counter[x.lower()]!="*rare*" and counter[y.lower()]!="*rare*" and counter[z.lower()]!="*rare*":
        if valid_trigrams == []:
            valid_trigrams.append(("#start1","#start2",x))
            valid_trigrams.append(("#start2",x,y))
            valid_trigrams.append((x,y,z))
        else:
            valid_trigrams.append((x,y,z))

test_sentences= [sent for sent in sent_tokenize(europarl[200010:220015])]

lp_uni1 = lpunigrams(valid_unigrams,words)
lp_bi1 = lpbigrams(valid_unigrams,valid_bigrams,words)
lp_tri1 = lptrigrams(valid_trigrams,valid_bigrams)

correct_bigrams_p = {}
for i in test_sentences:
    x,y = prob_creator(i,2,lp_bi1,len(set(words)))
    if x not in correct_bigrams_p.keys():
        correct_bigrams_p[x] = [y]
    else:
        correct_bigrams_p[x].append(y)

correct_trigrams_p = {}
for i in test_sentences:
    x,y = prob_creator(i,3,lp_tri1,len(set(words)))
    if x not in correct_trigrams_p.keys():
        correct_trigrams_p[x] = [y]
    else:
        correct_trigrams_p[x].append(y)

false_bigrams_p = {}
for i in correct_bigrams_p.keys():
    false_bigrams_p[i] = [] 
    for j in range(len(correct_bigrams_p[i])):
        false_sen = random_sentences(i,words)
        false_bigrams_p[i].append(prob_creator(false_sen,2,lp_bi1,len(set(words)))[1])

false_trigrams_p = {}
for i in correct_trigrams_p.keys():
    false_trigrams_p[i] = [] 
    for j in range(len(correct_trigrams_p[i])):
        false_sen = random_sentences(i,words)
        false_trigrams_p[i].append(prob_creator(false_sen,3,lp_tri1,len(set(words)))[1])

for i in correct_bigrams_p[:10]:
    print "Correct: ",correct_bigrams_p[i],"  False: ",false_bigrams_p[i]
for i in correct_trigrams_p[:10]:
    print "Correct: ",correct_trigrams_p[i],"   False: ",false_trigrams_p[i]

given_word = random.choice(words)
#given_word = 'ask'
probable = []
for x,y in valid_bigrams:
    if x == given_word:
        probable.append((lp_bi1[(given_word,y)],y))
print "the word  is : ",max(probable)

probable = []
for x,y,z in valid_trigrams:
    if x == given_word:
        probable.append((lp_tri1[(given_word,y,z)],y,z))
print "the word  is : ",max(probable)

cross1 = cross_entropy(lp_bi1)
print "bigrams",cross1
cross2 = cross_entropy(lp_tri1)
print "trigrams",cross2
