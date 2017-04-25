from utilities.data_manipulation import main as build_idf, open_files_in_path as load_files, ham_path, spam_path
from utilities.vectorizer import feature_vector
from tqdm import tqdm


import dill

import numpy
import os

train_ham_path = ham_path
train_spam_path = spam_path
train_data_fp = os.path.join(os.path.dirname(__file__), 'utilities', 'resources', 'train_data')
# test_ham_path = ''
# test_spam_path = ''


def pipeline():
    ham_x = numpy.array([feature_vector(txt) for txt in tqdm(load_files(train_ham_path))])
    ham_y = numpy.array(numpy.ones(len(ham_x)))
    spam_x = numpy.array([feature_vector(txt) for txt in tqdm(load_files(train_spam_path))])
    spam_y = numpy.array(numpy.zeros(len(spam_x)))

    train_x = numpy.concatenate((ham_x, spam_x), axis=0)
    train_y = numpy.concatenate((ham_y, spam_y), axis=0)


    with open(train_data_fp, 'w') as f:
        dill.dump((train_x, train_y), f)



def build_indexes():
    build_idf()


def load_train_data():
    with open(train_data_fp, 'rb') as f:
        train_data = dill.load(f)
    print('Loaded training data set: {0} records'.format(len(train_data[0])))
    return train_data


if __name__ == "__main__":
    pipeline()
    t=load_train_data()