import numpy as np


def check_grammar(turn, word, ternary, non_ternary):
    if turn == "first":
        for line in ternary:
            if line[1] == word:
                return line[0]#  the type!
    else:
        states = word.split(",")
        left = states[0]
        print "left",left
        print "right",states[1]
        right = states[1]
        goals = []
        for line in non_ternary:
            if left == line[1] and right == line[2]:
                goals.append(line[0])
        return ','.join(goals)

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

matrix = [["" for j in range(collumns)] for i in range(rows)]
# matrix = np.chararray((rows, collumns), itemsize=15)
# matrix[:] = " " #initialize

ternary, non_ternary = grammar()
validcoords = []
for j in range(0, collumns):
    for i in range(rows):
        if j > i:
            if i+1 == j:
                matrix[i][j] = check_grammar("first", words[i], ternary, non_ternary)#check_grammar(words[i]) #first match
                #check_grammar(words[0])
        else:
            matrix[i][j] = "X"

concat = []
for j in range(1, collumns):
    for i in range(rows, -1, -1):
        if j > i+1:
            concat = ""
            #check left
            for k in range(1, j):
                if matrix[i][k] != "X" and matrix[k][j] != "X":
                    concat = matrix[i][k] + "," + matrix[k][j]
                    if matrix[i][j] == check_grammar("second", concat, ternary, non_ternary):
                        matrix[i][j] = check_grammar("second", concat, ternary, non_ternary)
                    else:
                        matrix[i][j] += check_grammar("second", concat, ternary, non_ternary)
                    print k, matrix[i][j]
for i in range(len(matrix)):
    print matrix[i]
print matrix[1][-1]
