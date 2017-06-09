#import numpy as np


def left_child(row, collumn, names, follow_trails):#get the coords
    temp = follow_trails[row][collumn]
    if temp == "end":
        print "leftmost", names[row][collumn]
    else:
        # then we have to guess that temp contains two lists [[a1,a2],[b1,b2]]
        print "we are in left subtree", names[row][collumn]
        [left1, left2], [right1, right2] = temp
        print "left %s right %s" % (names[left1][left2], names[right1][right2])
        left_child(left1, left2, names, follow_trails)
        right_child(right1, right2, names, follow_trails)


def right_child(row, collumn, names, follow_trails):#get the coords
    temp = follow_trails[row][collumn]
    if temp == "end":
        print "rightmost", names[row][collumn]
    else:
        # then we have to guess that temp contains two lists [[a1,a2],[b1,b2]]
        print "we are in right sub-tree", names[row][collumn]
        [left1, left2], [right1, right2] = temp
        print "left %s right %s" % (names[left1][left2], names[right1][right2])
        left_child(left1, left2, names, follow_trails)
        right_child(right1, right2, names, follow_trails)



def check_grammar(turn, word, ternary, non_ternary):
    if turn == "first":
        for line in ternary:
            if line[1] == word:
                return line[0]#  the type!
    else:
        states = word.split(",")
        left = states[0]
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
trails = [[[] for j in range(collumns)] for i in range(rows)]

# matrix = np.chararray((rows, collumns), itemsize=15)
# matrix[:] = " " #initialize

ternary, non_ternary = grammar()
for j in range(0, collumns):
    for i in range(rows):
        if j > i:
            if i+1 == j:
                matrix[i][j] = check_grammar("first", words[i], ternary, non_ternary)#check_grammar(words[i]) #first match
                trails[i][j] = "end"
                #check_grammar(words[0])
        else:
            matrix[i][j] = "X"

concat = []
for j in range(1, collumns):
    for i in range(rows, -1, -1):
        if j > i+1:
            concat = ""
            for k in range(1, j):
                if (matrix[i][k] != "X" and matrix[k][j] != "X") and (matrix[i][k] != "" and matrix[k][j] != ""):
                        concat = matrix[i][k] + "," + matrix[k][j]
                        if matrix[i][j] == check_grammar("second", concat, ternary, non_ternary):
                            matrix[i][j] = check_grammar("second", concat, ternary, non_ternary)
                        elif check_grammar("second", concat, ternary, non_ternary) != "":
                            trails[i][j].extend([[i, k], [k, j]])
                            matrix[i][j] += check_grammar("second", concat, ternary, non_ternary)
#show the cky array
for i in range(len(matrix)):
    print matrix[i]

#follow the trails to get the syntactic tree
[a1, a2], [b1, b2] = trails[0][-1]#these are the elements that created the S

print "The sentence begins"
print "S"

left_child(a1, a2, matrix, trails)
right_child(b1, b2, matrix, trails)
