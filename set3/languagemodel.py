from math import log
from nltk import ngrams


def find_rare(diction):  # find and delete rare tokens from dictionary
    for x in diction.keys():
        if diction[x] < 10:
            del diction[x]
    return diction


def lpbigrams(words, lexicon):  # log probabilities for bigrams
    valid_unigrams, valid_bigrams = create_bigrams(words, lexicon)
    lpbi = {}
    for (x, y) in set(valid_bigrams):
        lpbi[(x, y)] = log((valid_bigrams.count((x, y))+1)/(float((valid_unigrams.count(x))+len(set(valid_unigrams)))))
    return valid_bigrams, lpbi


def create_bigrams(words, lexicon):
    valid_unigrams = []
    valid_bigrams = []
    for i in words:
        if i in lexicon.keys():
            valid_unigrams.append(i)
    bigrams = ngrams(words, 2)

    for x, y in bigrams:
        if x in lexicon.keys() and y in lexicon.keys():
            if valid_bigrams == []:
                valid_bigrams.append(("#start0", "#start1"))
                valid_bigrams.append(("#start1", x))
                valid_bigrams.append((x, y))
            else:
                valid_bigrams.append((x, y))
    return valid_unigrams, valid_bigrams
