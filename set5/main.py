import numpy as np

def check_grammar(word):
    pass

sentence = "I saw the man with the telescope"
words = sentence.split(" ")
rows = len(words)
collumns = len(words)+1
matrix = np.chararray((rows, collumns), itemsize=5)
matrix[:] = "" #initialize

for j in range(collumns):
    for i in range(rows):
        if j > i:
            if i+1 == j:
                matrix[i, j] = "match" #first match
                #check_grammar(words[0])
            else:
                for k in range(1, j):
                    con = matrix[i, k] + " " + matrix[k, j] #concatenation of the two states
                    status = check_grammar(con)
                    matrix[i, j] = status
print matrix