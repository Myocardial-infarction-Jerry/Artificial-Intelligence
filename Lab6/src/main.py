import os
import pandas as pd
import numpy as np
from neural_network import DNN
from word2vec import word2vec
from constants import *
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(__file__) + '/../')


def drawPath(coords):
    x = [coord[0] for coord in coords]
    y = [coord[1] for coord in coords]
    for i in range(len(coords) - 1):
        plt.plot([x[i], x[i + 1]], [y[i], y[i + 1]], 'c')
    plt.plot(x, y, 'bo')
    # plt.show()
    plt.savefig('res/DNN_Loss.png')
    plt.close()


def initialize(file_dir):
    try:
        dataframe = pd.read_csv(file_dir)
    except OSError:
        print('Error: file not found')
        exit()
    else:
        datas = []
        model = word2vec()
        print('Reading datas from ' + os.getcwd() + '/' + file_dir)
        for index, data in dataframe.iterrows():
            # datas.append((data[1].split(), np.array(data[2:])))
            word_vec = np.zeros(num_features)
            for word in data[1].split():
                word_vec += model.query(word)
            datas.append((word_vec.reshape([1, -1]),
                          np.array(data[2:], dtype=np.float64).reshape([1,
                                                                        -1])))
    return datas


if __name__ == '__main__':
    train_datas = initialize(file_dir='dataset/Regression/Dataset_train.csv')
    test_datas = initialize(
        file_dir='dataset/Regression/Dataset_validation.csv')
    net = DNN([300, 42, 6], step=50, alpha=0.01, n_iter=500)
    print('Training DNN...')
    net.train(train_datas)
    net.save('300-42-6-sigmoid')
    net.load('300-42-6-sigmoid')
    Eval = net.predict([data[0] for data in test_datas])
    for i in range(5):
        print(Eval[i], test_datas[i][1])
    miss = 0
    for index in range(len(Eval)):
        for num in range(len(Eval[0])):
            if abs(Eval[index][0][num] - test_datas[index][1][0][num]) > 0.1:
                miss += 1
    miss /= len(Eval) * len(Eval[0])
    print('accuracy =', 1 - miss)

    test = []
    rates = [1E-3, 1E-2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for rate in rates:
        net = DNN([300, 42, 6], step=50, alpha=rate, n_iter=500)
        net.train(train_datas)
        Eval = net.predict([data[0] for data in test_datas])
        miss = 0
        for index in range(len(Eval)):
            for num in range(len(Eval[0])):
                if abs(Eval[index][0][num] -
                       test_datas[index][1][0][num]) > 0.1:
                    miss += 1
        miss /= len(Eval) * len(Eval[0])
        test.append((len(test), 1 - miss))
        print(Eval[-1], test_datas[-1][1])
        print('accuracy = %8f  rate = %8f' % (1 - miss, rate))
    drawPath(test)
