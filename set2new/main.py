from datahandling import *
import os
import numpy
from vectorizer import feature_vector


train_ham_path = os.path.join(os.path.dirname(__file__), "training", "ham")
train_spam_path = os.path.join(os.path.dirname(__file__), "training", "spam")
test_ham_path=''
test_spam_path=''

#Create the feature vectures using feature_vector from vectorizer and putting 0 if ham 1 if spam
ham_x = numpy.array([feature_vector(txt) for txt in open_files_inpath(train_ham_path)])
ham_y = numpy.array(numpy.ones(len(ham_x)))
spam_x = numpy.array([feature_vector(txt) for txt in open_files_inpath(train_spam_path)])
spam_y = numpy.array(numpy.zeros(len(spam_x)))

train_x = numpy.concatenate((ham_x, spam_x), axis=0)
train_y = numpy.concatenate((ham_y, spam_y), axis=0)
