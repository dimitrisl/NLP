# -*- coding: utf-8 -*-


#[Optional material for the TEA course.] (i) Check the Levenshtein distance calculations
#of the table on slide 21. (ii) Implement (in any programing language) the dynamic programing
#algorithm that computes the Levenshtein distance (slides 16–21); your implementation should
#print tables like the one of slide 21 (without the arrows). (iii) Optionally extend your
#implementation to accept as input a word w, a vocabulary V (e.g., words that occur at least 10
#times in a corpus), and a maximum distance d, and return the words of V whose Levenshtein
#distance to w is up to d


word1 = "παίζετε"
word2 = "πέζοιται"
listoflists = []
first = ""
second = ""
for i in word1:
    first+=i # word1 iterated so far
    for j in word2:
        second+=j # word2 iterated so far



def measure(first,second):
    