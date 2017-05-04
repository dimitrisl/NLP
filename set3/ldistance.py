# -*- coding: utf-8 -*-


def count_distance(lettertarget,lettersource,listoflists,x,y):
    cost = 0
    if lettertarget == lettersource:
        return cost + listoflists[x-1][y-1]
    else:
        cost = min(listoflists[x-1][y]+1,listoflists[x][y-1]+1,listoflists[x-1][y-1]+2)
        return cost


def get_dist(word1,word2):
    listoflists = []  # "array" that contains the distances
    listoflists = [[i for i in range(len(word1) + 1)]]  # initialization of the first vector,vectors are lines!
    for i in range(1,len(word2)+1):
        listoflists.append([i])
        listoflists[-1].extend([0 for k in range(len(word1))])

    for x,w2 in enumerate(word2, 1):
        for y,w1 in enumerate(word1, 1):
            listoflists[x][y] = count_distance(w1,w2,listoflists,x,y)

    return listoflists[-1][-1]
