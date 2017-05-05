from ldistance import get_dist
from math import log
from nltk.tokenize import word_tokenize


def levenstein(word, lexicon):
    ldistance = {}
    for i in lexicon.keys():
        ldistance[i] = get_dist(word, i)
    min_val = min(ldistance.itervalues())
    correct_word = [(word, k) for word, k in ldistance.iteritems() if k == min_val]
    return correct_word[0]


def viterbidecoder(sentence, lexicon, logprob_bigrams):
    V = {}
    tokens = [token for token in word_tokenize(sentence)]
    word, dist = levenstein(tokens[0], lexicon)
    correct_sequence = ['#start0', "#start1"]
    print word
    correct_sequence.append(word)
    V[0] = 0
    V[1] = log(1/float(dist + 1.1)) + logprob_bigrams[(correct_sequence[0], correct_sequence[1])]
    for i in range(2, len(tokens)):
        next_word, dist = levenstein(tokens[i-1], lexicon)
        correct_sequence.append(next_word)
        if (correct_sequence[i-1], correct_sequence[i]) in logprob_bigrams.keys():
            V[i] = log(1 / float(dist + 1.1)) + logprob_bigrams[(correct_sequence[i-1], correct_sequence[i])] + V[i-1]
        else:
            V[i] = log(1 / float(dist + 1.1)) + 1/float(len(lexicon)) + V[i - 1]
    return correct_sequence, V


