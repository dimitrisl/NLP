# Tune the feature set and hyperparameters (e.g., regularization weight l) on a held-out part
# of the training data or using a cross-validation (slide 25) on the training data.

from datahandling import open_files_inpath
import os
import numpy
from vectorizer import feature_vector
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import time
from graphics import plot_learning_curve, rpcurves
from sklearn.model_selection import ShuffleSplit



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
logisticregr_model.fit(train_x, train_y ) #training of logistic regression
#Naive Bayes
mgausbay_model= MultinomialNB()
mgausbay_model.fit(train_x,train_y)

#learning curves

# Algorithm Dictionary
estimators = {'LR':logisticregr_model, 'NB':mgausbay_model}
predictions = {}
for (name,estimator) in estimators.items():
    title = "Learning Curves " + name
    # Random permutation cross-validator
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
    predictions[name] = estimator.predict(test_x)
    plt = plot_learning_curve(estimator, title, test_x, predictions[name], (0.1, 1.01), cv=cv, n_jobs=-1)
    plt.savefig('%s.png' % name, bbox_inches='tight')
    plt.show()
    plt.close()
    plt2 = rpcurves(estimator,test_ham_y, test_spam_y, test_ham_x, test_spam_x)
    plt2.savefig('%s-rc.png' % name, bbox_inches='tight')
    plt2.show()
    plt2.close()

print "it lasted : %s seconds" % (time.time()-start)
