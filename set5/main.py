import numpy as np


def check_grammar(turn, word, ternary, non_ternary):
    if turn == "first":
        for line in ternary:
            if line[1] == word:
                return line[0]#  the type!
    else:
        states = word.split(" ")
        print states
        for symbol1, symbol2, symbol3 in non_ternary:
            if (states[0], states[1]) == (symbol2, symbol3) or (states[0], states[1]) == (symbol3, symbol2):
                return symbol1
            else:
                return ""

def grammar():
    f = open("grammar")
    rules = f.readlines()
    rules = [line.replace(" -> ", " ").split(" ") for line in rules]
    list1 = []
    list2 = []
    for line in rules:
        line = [i.strip() for i in line]
        if len(line) == 2:
            list1.append(line)
        else:
            list2.append(line)

    return list1, list2

sentence = "I saw the man with the telescope"
words = sentence.split(" ")
rows = len(words)
collumns = len(words)+1
matrix = np.chararray((rows, collumns), itemsize=5)
matrix[:] = " " #initialize

ternary, non_ternary = grammar()

for j in range(collumns):
    for i in range(rows):
        if j > i:
            if i+1 == j:
                matrix[i, j] = check_grammar("first", words[i], ternary, non_ternary)#check_grammar(words[i]) #first match
                #check_grammar(words[0])
            else:
                for k in range(1, j):
                    con = matrix[i, k] + " " + matrix[k, j-1] #concatenation of the two states
                    matrix[i, j] += check_grammar("second", con, ternary, non_ternary)
print matrix
