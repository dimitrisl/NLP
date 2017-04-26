from datahandling import open_files_inpath
import os
import numpy
from vectorizer import feature_vector
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import time

start = time.time()

train_ham_path = os.path.join(os.path.dirname(__file__), "training", "ham")
train_spam_path = os.path.join(os.path.dirname(__file__), "training", "spam")
test_ham_path = os.path.join(os.path.dirname(__file__), "test", "ham")
test_spam_path = os.path.join(os.path.dirname(__file__), "test", "spam")

#Create the feature vectures using feature_vector from vectorizer and putting 0 if ham 1 if spam
ham_x = numpy.array([feature_vector(txt) for txt in open_files_inpath(train_ham_path)])
ham_y = numpy.array(numpy.ones(len(ham_x)))
spam_x = numpy.array([feature_vector(txt) for txt in open_files_inpath(train_spam_path)])
spam_y = numpy.array(numpy.zeros(len(spam_x)))

train_x = numpy.concatenate((ham_x, spam_x), axis=0)
train_y = numpy.concatenate((ham_y, spam_y), axis=0)


#test data

test_ham_x = numpy.array([feature_vector(txt) for txt in open_files_inpath(test_ham_path)])
test_ham_y = numpy.array(numpy.ones(len(test_ham_x)))
test_spam_x = numpy.array([feature_vector(txt) for txt in open_files_inpath(test_spam_path)])
test_spam_y = numpy.array(numpy.zeros(len(test_spam_x)))

test_x=numpy.concatenate((test_ham_x,test_spam_x), axis=0)
test_y=numpy.concatenate((test_ham_y,test_spam_y), axis=0)

#Logistic Regression

logisticregr_model = LogisticRegression()
logisticregr_model.fit(train_x,train_y) #training of logistic regression
print logisticregr_model.score(train_x,train_y), train_y.mean()

#prediction on test data using logistic regression

test_predicted_lg = logisticregr_model.predict(test_x)

print(metrics.classification_report(test_y, test_predicted_lg, digits=3))

#Naive Bayes
mgausbay_model= MultinomialNB()
mgausbay_model.fit(train_x,train_y)

test_predicted_gb= mgausbay_model.predict(test_x)

print(metrics.classification_report(test_y,test_predicted_gb,digits=3))
print "it lasted : ",time.time() - start