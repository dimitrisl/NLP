from collections import Counter
import os
import spacy
import json

ham_path = os.path.join(os.path.dirname(__file__), "training", "ham")
spam_path = os.path.join(os.path.dirname(__file__), "training", "spam")
nlp = spacy.load('en')

#read files from path
def open_files_inpath( filepath ):
    content = []
    files = os.listdir(filepath)
    print ("{0} files found in path".format(len(files)))
    for file_ in files:
        with open(os.path.join(filepath,file_)) as f:
            content.append(f.read())
    print("{0} files collected from path".format(len(content)))
    return content

#preprocess and tokenization.exclude tokens that are numbers,
    # punctuation,symbols,stopwords, email, url, space and perform lemmatization
def prep_and_tokenizer(text, lemma=True) :
    tokens = []
    for token in nlp(unicode(text,'utf-8')):
        if not(token.is_digit or token.like_num or token.is_punct or token.is_oov or
                   token.like_url or token.like_email or token.is_stop or
                   token.is_space or token.pos_ in {'SYM', 'NUM', 'X', 'PUNCT'}):
            tokens.append(token.lemma_ if lemma else token.text.lower())
    return tokens

#build vocabulary with words that have over 15 appearences
def build_voc(list_of_tokens, minimum_df=15):
    words = [num for elem in list_of_tokens for num in elem]
    words = Counter(words)
    print('Building vocabulary from {0} tokens'.format(len(words.keys())))
    for word in words.keys():
        if words[word] <= minimum_df:
            del words[word]
    print('Vocabulary composed of {0} tokens'.format(len(words.keys())))
    return words


#feature selection performed under the rule that a word should
    # appear more than 75% more in one category to provide information
def feature_selection(ham_voc, spam_voc, threshold = 0.75):

    selected_terms, idf_list = [], {}
    for term, freq in ham_voc.iteritems():
        if freq/float(freq+spam_voc[term]) >= threshold:
            selected_terms.append(term)
            idf_list[term] = freq + spam_voc[term]

    for term, freq in spam_voc.iteritems():
        if freq/float(freq+ham_voc[term]) >= threshold:
            selected_terms.append(term)
            idf_list[term] = freq+ham_voc[term]
    print("{0} terms selected".format(len(selected_terms)))
    return selected_terms, idf_list

def main():
    ham = build_voc([list(prep_and_tokenizer(text, lemma=True))
                         for text in open_files_inpath(ham_path)])
    spam = build_voc(list([prep_and_tokenizer(text, lemma=True)
                               for text in open_files_inpath(spam_path)]))
    terms, idf = feature_selection(ham, spam)

    #write idf scores on memory in the form of a json file
    with open(os.path.join(os.getcwd(),'idf_terms.json'), 'w') as f:
        json.dump(idf, f)
