# -*- coding: utf-8 -*-
#
#Develop a text classifier for a kind of texts of your choice (e.g., e-mail messages, tweets,
#customer reviews) and at least two classes (e.g., spam/ham, positive/negative/neutral).
#You should write your own code to convert each (training, validation, or test) text to a feature
#vector. You may use Boolean, TF, or TF-IDF features corresponding to words or n-grams, to
#which you can also add other features (e.g., length of the text).3 You may apply any feature
#selection (or dimensionality reduction) method you consider appropriate. You may also want
#to try using centroids of pre-trained word embeddings (slide 35). You can write your own
#code to perform feature selection (or dimensionality reduction) and to train the classifier (e.g.,
#using SGD and the tricks of slides 58 and 59, in the case of logistic regression), or you can
#use existing implementations.5 You should experiment with at least logistic regression, and
#optionally other learning algorithms (e.g., Naive Bayes, k-NN, SVM). Draw learning curves
#(slides 64, 67) with appropriate measures (e.g., accuracy, F1) and precision-recall curves
#(slide 23). Include experimental results of appropriate baselines (e.g., majority classifiers).
#Make sure that you use separate training and test data. Tune the feature set and hyperparameters
#(e.g., regularization weight λ) on a held-out part of the training data or using a
#cross-validation (slide 25) on the training data. Document clearly in a short report (max. 10
#pages) how your system works and its experimental results.

import codecs
import os
import nltk
from nltk.stem.snowball import SnowballStemmer
from math import log
import string

def tokenizer(text):
    stemmer = SnowballStemmer("english")
    tokens = [stemmer.stem(word.lower()) for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    return tokens

def count_occur(words): #find the occurences of each token
    counter={}
    for i in set(words):
        counter[i] = 0
    for token in words:
        counter[token]+=1
    return counter


def create_voc(email_files):
    stopwords = nltk.corpus.stopwords.words("english")
    f_tokens = []
    symbols = ["//","_","``","#","{",'}',"@","(",")","[","]",".",":",";","+","-","*","/","&","|","<",">","=","~",'"',",","'","?","etc","ect"]
    extras = ["www","mail","http","forward","Re","to","cc","subject","sent","hotmail","gmail","yahoo","msn","outlook","enron","com","gov","net"]
    months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
    extras.extend(months+[i[:3] for i in months])
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    extras.extend(days + [i[:3] for i in days]) #days + days in 3 letters
    extras.extend(list(string.ascii_lowercase))
    stopwords.extend(extras)
    tokens = []
    for i in email_files:
        mid = tokenizer(i)
        tokens.extend([k for k in mid if not str(k).isdigit() and k not in symbols and k not in stopwords])
    counter = count_occur(tokens)
    counter = sorted(zip(counter.values(),counter.keys()),reverse=True)[:2000]
    for x,y in counter:
        f_tokens.append(y)
    return f_tokens,counter

def tf(word,text): # i pass the stemmer object
    tokens=tokenizer(text)
    return float(tokens.count(word))/len(tokens)

def idf(word,corpus):
    docfreq=0
    for i in corpus:
        if word in tokenizer(i):
            docfreq+=1
    return log(float(len(corpus)/docfreq))

def freq_vector(emails,vocabulary):
    dt = {}
    counter = 0 
    for i,j in emails:
        for l in vocabulary:
            dt[(l,counter,j)] = tf(l,i)
        counter+=1
    return dt

stopwords = nltk.corpus.stopwords.words('english')
ham_path = os.path.join(os.getcwd(),"enron1","ham" )
spam_path= os.path.join(os.getcwd(),"enron1","spam" )

ham_files = []
spam_files = []

for root,directories,files in  os.walk(ham_path):
    for f in files:
        f1 = codecs.open(ham_path+os.sep+f,"r","utf-8",errors='ignore')
        ham_files.append(f1.read())
        f1.close()
        
for root,directories,files in  os.walk(spam_path):
    for f in files:
        f2 = codecs.open(spam_path+os.sep+f,"r","utf-8",errors='ignore')
        spam_files.append(f2.read())
        f2.close()

vocabulary,occurences= create_voc(ham_files+spam_files)
print vocabulary[:10]
all_mail = [(i,"ham") for i in ham_files]
all_mail.extend([(j,"spam") for j in spam_files])
d = freq_vector(all_mail,vocabulary)