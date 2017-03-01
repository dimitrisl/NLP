# -*- coding: utf-8 -*-

#[Optional material for the TEA course.] (i) Check the Levenshtein distance calculations
#of the table on slide 21. (ii) Implement (in any programing language) the dynamic programing
#algorithm that computes the Levenshtein distance (slides 16–21); your implementation should
#print tables like the one of slide 21 (without the arrows). (iii) Optionally extend your
#implementation to accept as input a word w, a vocabulary V (e.g., words that occur at least 10
#times in a corpus), and a maximum distance d, and return the words of V whose Levenshtein
#distance to w is up to d

def count_distance(lettertarget,lettersource,listoflists,x,y):
    cost = 0
    if lettertarget == lettersource:
        return cost + listoflists[x-1][y-1]
    else:
        cost = min(listoflists[x-1][y]+1,listoflists[x][y-1]+1,listoflists[x-1][y-1]+2)
        return cost


word1 = "paizete"  # target string
word2 = "pezoitai" # source string
listoflists = [] # "array" that contains the distances

listoflists = [[i for i in range(len(word1)+1)]] # initialization of the first vector,vectors are lines!
for i in range(1,len(word2)+1):
    listoflists.append([i])
    listoflists[-1].extend([0 for k in range(len(word2)-1)])


#we wont iterate line 0 at all!!

for w1,x in zip(word2,range(1,len(word2)+1)):
    for w2,y in zip(word1,range(1,len(word1)+1)):
        listoflists[x][y] = count_distance(w1,w2,listoflists,x,y)

for i in listoflists:
    print i
