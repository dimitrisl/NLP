from datahandling import prep_and_tokenizer
from collections import Counter
import json
import os

#read from file that contains the idf for the terms of the voc after feature selection
with open(os.path.join(os.path.dirname(__file__), 'idf_terms.json')) as f:
    idf = json.load(f)

#create term frequencies
def term_frequencies(text):
    return Counter(prep_and_tokenizer(text, lemma=True))

#create feature vector for each email
def feature_vector(text):
    tf_dict = term_frequencies(text)
    vector = []

    for term in idf:
        vector.append(tf_dict[term] * (1 / idf[term]))

    return vector
