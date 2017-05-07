from ldistance import get_dist
from math import log
from nltk.tokenize import word_tokenize


def levenstein(word, lexicon):
    ldistance = {}
    for i in lexicon.keys():
        ldistance[i] = get_dist(word, i)
    min_val = min(ldistance.itervalues())
    correct_word = [(k, word) for word, k in ldistance.iteritems() if k == min_val]
    correct_word.sort()
    correct_word = [(y, x) for (x, y) in correct_word]
    return correct_word[:5]


def viterbidecoder(sentence, lexicon, logprob_bigrams):
    vit = dict()
    correct_sequence = []
    vit[(0, "#start1")] = log(1) # we decided to have the level of viterbi and the word as a tuple in a dict.
    tokens = [token.lower() for token in word_tokenize(sentence) if token.isalnum()]
    possible_words = dict()
    for level, token in enumerate(tokens,1):
        possible_words[(level, token)] = levenstein(token, lexicon) # we get from 1 to 5 pairs of correct words and distances
    wpl = dict()
    maximum_word, maximum_prob = "#start1", vit[(0,"#start1")]
    for level in range(1, len(tokens)+1):
        words_per_level = []
        distances_per_word = []
        for x, y in possible_words.keys():
            if x == level:
                for word, distance in possible_words[(x, y)]:
                    words_per_level.extend([word])
                    distances_per_word.extend([distance])

        wpl[level] = words_per_level
        #at this point we have the valid words of in each level within the list words_per_level
        #we now have to find the previous minimum and store the mininum word the sequence
        for word, dist in zip(words_per_level, distances_per_word):
            if (maximum_word,word) in logprob_bigrams.keys():
                vit[(level, word)] = -log(dist+1) + logprob_bigrams[(maximum_word, word)] + maximum_prob
            else:
                vit[(level, word)] = -log(dist+1) + 1/float(len(lexicon)) + maximum_prob

        #find the minimum of this level in order to feed the next loop
        maximum_prob, maximum_word = vit[(level, words_per_level[0])], words_per_level[0]
        for x, y in vit.keys():
            for word in words_per_level:
                if x == level and maximum_prob < vit[(level, word)]:
                    maximum_prob = vit[(level, word)]
                    maximum_word = y

    #we have to iterate through each level to get the best sequence
    pr = dict()
    keep = dict()

    for level in range(1, len(tokens)+1):
        pr[level] = []
        for lvl, tup in vit.keys():
            if lvl == level:
                pr[level].append((vit[(lvl, tup)], tup))
        pr[level].sort(reverse=True)
        print pr[level]
        keep[level] = pr[level][0][0]
        correct_sequence.append(pr[level][0][1])

    return correct_sequence, keep


