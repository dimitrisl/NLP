from spacy.en import English
from nltk.tokenize import sent_tokenize
from collections import Counter
from languagemodel import *
from spelling_corrector import viterbidecoder,baseline
from word_change import change
from nltk.tokenize import word_tokenize

nlp = English()
with open('europarl.txt', 'r') as f:
    content = f.read()

sentences = [sent for sent in sent_tokenize(content[0:200000].decode('utf-8'))]
words = [str(token).lower() for sent in sentences for token in nlp(sent, 'utf-8') if str(token).isalnum()]
lexicon = Counter(words)
lexicon = find_rare(lexicon)
logprob_bigrams = {}
bigrams, logprob_bigrams = lpbigrams(words, lexicon)


given_sentence = " ".join([change(token) for token in word_tokenize(sentences[11]) if token.isalnum()])
print "the true sentence is : ", sentences[11]
print "The sentence given was : %s" % given_sentence
correct, b = viterbidecoder(given_sentence, lexicon, logprob_bigrams)
true = [str(token).lower() for token in word_tokenize(sentences[11]) if str(token).isalnum()]
counter = 0
for x, y in zip(true, correct):
    if x == y:
        counter += 1
print "the similarity is %s per cent" % (100 * counter/len(correct))

print "dynamic : ", correct

ct, b = baseline(given_sentence, lexicon, logprob_bigrams)
counter = 0
for x, y in zip(true, ct):
    if x == y:
        counter += 1
print "the similarity of the baseline is %s per cent" % (100 * counter/len(ct))
print "greedy : ", ct
