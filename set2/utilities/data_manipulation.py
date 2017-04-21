from collections import Counter

import json
import os
import spacy

ham_path = os.path.join(os.path.dirname(__file__), "training", "ham")
spam_path = os.path.join(os.path.dirname(__file__), "training", "spam")
nlp = spacy.load('en')


def open_files_in_path(file_path):
    content = []
    files = os.listdir(file_path)
    print("Found {0} files...".format(len(files)))
    for file_ in files:
        with open(os.path.join(file_path, file_)) as f:
            content.append(f.read())
    print('Retrieved content from {0} files'.format(len(content)))
    return content


def tokenize_and_pre_process(text, del_digits=True, del_punct=True, del_urls_emails=True, del_space=True,
                             del_stop=True, del_symbols=True, lemma=True):
    tokens = []
    for token in nlp(unicode(text, 'utf-8')):
        if not((token.is_digit and del_digits) or (token.is_punct and del_punct) or
               ((token.like_url or token.like_email) and del_urls_emails) or (token.is_stop and del_stop) or
               (token.is_space and del_space)) or (token.pos_ in {'SYM', 'NUM', 'X'} and del_symbols):
            tokens.append(token.lemma_ if lemma else token.text.lower())
    return tokens


def build_lexicon(list_of_tokens, minimum_df=10):
    words = [num for elem in list_of_tokens for num in elem]
    words = Counter(words)
    print('Building lexicon from {0} tokens'.format(len(words.keys())))
    for word in words.keys():
        if words[word] <= minimum_df:
            del words[word]
    print('Lexicon composed of {0} tokens'.format(len(words.keys())))
    return words


def select_terms_by_distribution(ham_lexicon, spam_lexicon, threshold=0.75):
    selected_terms, idf_lexicon = [], {}
    for term, frequency in ham_lexicon.iteritems():
        if frequency / float(frequency + spam_lexicon[term]) >= threshold:
            selected_terms.append(term)
            idf_lexicon[term] = frequency + spam_lexicon[term]
    for term, frequency in spam_lexicon.iteritems():
        if frequency / float(frequency + ham_lexicon[term]) >= threshold:
            selected_terms.append(term)
            idf_lexicon[term] = frequency + ham_lexicon[term]
    return selected_terms, idf_lexicon



def main():
    ham = build_lexicon([list(tokenize_and_pre_process(text, lemma=True))
                         for text in open_files_in_path(ham_path)])
    spam = build_lexicon(list([tokenize_and_pre_process(text, lemma=True)
                               for text in open_files_in_path(spam_path)]))
    terms, idf = select_terms_by_distribution(ham, spam)

    with open(os.path.join(os.getcwd(), 'resources', 'idf_terms.json'), 'w') as f:
        json.dump(idf, f)


if __name__ == "__main__":
    main()
