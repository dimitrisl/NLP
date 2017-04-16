from __future__ import division
from utilities.data_manipulation import tokenize_and_pre_process

from collections import Counter

import json
import os

with open(os.path.join(os.path.dirname(__file__), 'resources', 'idf_terms.json')) as f:
    idf = json.load(f)


def term_frequencies(text):
    return Counter(tokenize_and_pre_process(text, lemma=False))


def feature_vector(text):
    tf_dict = term_frequencies(text)
    vector = []

    for term in idf:
        vector.append(tf_dict[term] * (1 / idf[term]))

    return vector


def main():
    pass

if __name__ == "__main__":
    main()
