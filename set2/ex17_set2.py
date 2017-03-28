# -*- coding: utf-8 -*-
"""
17. Develop a text classifier for a kind of texts of your choice (e.g., e-mail messages, tweets,
customer reviews) and at least two classes (e.g., spam/ham, positive/negative/neutral). 2 You
should write your own code to convert each (training, validation, or test) text to a feature
vector. You may use Boolean, TF, or TF-IDF features corresponding to words or n-grams, to
which you can also add other features (e.g., length of the text). 3 You may apply any feature
selection (or dimensionality reduction) method you consider appropriate. You may also want
2
For e-mail spam filtering, you may want to use the Ling-Spam or Enron-Spam datasets (available
from http://nlp.cs.aueb.gr/software.html). For tweets, you may want to use datasets from
http://alt.qcri.org/semeval2016/task4/. For customer reviews, you may want to use datasets from
http://alt.qcri.org/semeval2016/task5/. Consult the instructor for further details.
3
See related publications at http://nlp.cs.aueb.gr/publications.html and related theses at
http://nlp.cs.aueb.gr/theses.html for possible features and other ideas.to try using centroids of pre-trained word embeddings (slide 35). 4 You can write your own
code to perform feature selection (or dimensionality reduction) and to train the classifier (e.g.,
using SGD and the tricks of slides 58 and 59, in the case of logistic regression), or you can
use existing implementations. 5 You should experiment with at least logistic regression, and
optionally other learning algorithms (e.g., Naive Bayes, k-NN, SVM). Draw learning curves
(slides 64, 67) with appropriate measures (e.g., accuracy, F1) and precision-recall curves
(slide 23). Include experimental results of appropriate baselines (e.g., majority classifiers).
Make sure that you use separate training and test data. Tune the feature set and hyper-
parameters (e.g., regularization weight λ) on a held-out part of the training data or using a
cross-validation (slide 25) on the training data. Document clearly in a short report (max. 10
pages) how your system works and its experimental results.
4
Pre-trained word embeddings are available, for example, from http://nlp.stanford.edu/projects/glove/.
See also word2vec (https://code.google.com/archive/p/word2vec/).
5
For example, LIBSVM (http://www.csie.ntu.edu.tw/~cjlin/libsvm/), scikit-learn (http://scikit-
learn.org/stable/), SVMlight (http://svmlight.joachims.org/), Weka
(http://www.cs.waikato.ac.nz/ml/weka/).
"""

