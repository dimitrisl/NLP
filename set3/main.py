from spacy.en import English
from nltk.tokenize import sent_tokenize
from collections import Counter

nlp = English()
with open('europarl.txt', 'r') as f:
    content = f.read()

sentences = [sent for sent in sent_tokenize(content[0:200000].decode('utf-8'))]
words = [token for sent in sentences for token in nlp(sent, 'utf-8')]
lexicon = Counter(words)

