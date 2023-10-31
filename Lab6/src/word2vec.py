import numpy as np
import pandas as pd
import os
from gensim import models
from constants import *

os.chdir(os.path.dirname(__file__) + '/../')


def train(file_dir='dataset/Regression/Dataset_words.csv'):
    # Read datas from selected file
    try:
        dataframe = pd.read_csv(file_dir)
    except OSError:
        print('Error: file not found')
        return
    else:
        print('Reading datas from ' + os.getcwd() + '/' + file_dir)

    datas = []
    for index, data in dataframe.iterrows():
        datas.append(data[1].split())
        # print(datas[-1])

    # Train 'word2vec' model in genism
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    min_word_count = 0  # Remove the low-frequency words
    num_workers = 4  # Workers number
    context = 3  # Context sliding window
    model_ = 0  # Model type (0=CBW)

    model_name = 'word2vec.model'

    print('Training model...')
    model = models.Word2Vec(datas,
                            workers=num_workers,
                            vector_size=num_features,
                            min_count=min_word_count,
                            window=context,
                            sg=model_)

    # Model saving
    print('Saving model...')
    model.save(os.path.join('models', model_name))

    print('Done')


class word2vec(object):

    def __init__(self):
        try:
            self.model = models.Word2Vec.load('models/word2vec.model')
        except OSError:
            print('Model not found, training...')
            train()
            self.model = models.Word2Vec.load('models/word2vec.model')

    def query(self, word):
        return self.model.wv[word]


if __name__ == '__main__':
    train()
