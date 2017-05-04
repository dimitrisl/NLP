from ldistance import get_dist


def levenstein(word, lexicon):
    ldistance = {}
    for i in lexicon.keys():
        ldistance[(word, i)] = get_dist(word, i)
    min_val = min(ldistance.itervalues())
    correct_word = [(words, k) for (words, k) in ldistance.iteritems() if k == min_val]
    return correct_word


def viterbidecoder():
    pass


