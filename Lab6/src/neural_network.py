import pandas as pd
import numpy as np
import os
import pickle
import random
from copy import deepcopy
import matplotlib.pyplot as plt
import time

os.chdir(os.path.dirname(__file__) + '/../')


def showLogger(logger, alpha):
    for k in range(1, len(logger)):
        plt.plot([k - 1, k], [logger[k - 1], logger[k]], 'c')
    plt.xlabel('Iteration times')
    plt.ylabel('Loss')
    # plt.show()
    plt.savefig('res/DNN_Loss alpha=%8f.png' % (alpha))
    plt.close()


def sigmoid(val, d=0):
    val = np.minimum(val, 2)
    if d == 0:
        return 1 / (1 + np.exp(-val))
    elif d == 1:
        return np.exp(val) / (1 + np.exp(val))**2


def relu(val, d=0):
    if d == 0:
        return np.maximum(0, val)
    elif d == 1:
        return np.heaviside(val, 0.5)


def mean_square(a, b):
    return (a - b)**2 * np.sign(a - b) / 2


class layer(object):

    def __init__(self, in_size, out_size, active_func):
        self.in_size = in_size
        self.out_size = out_size
        self.active_func = active_func
        self.w = np.random.randn(in_size, out_size)
        self.b = np.random.randn(1, out_size)

    def forward(self, x):
        return self.active_func(np.matmul(x, self.w) + self.b)


class DNN(object):

    def __init__(self,
                 layer_shape,
                 active_func=sigmoid,
                 loss_func=mean_square,
                 alpha=0.05,
                 step=100,
                 n_iter=30000,
                 epi=1E-6):
        self.layer_shape = layer_shape
        self.active_func = active_func
        self.loss_func = loss_func
        self.alpha = alpha
        self.step = step
        self.n_iter = n_iter
        self.epi = epi
        self.train_logger = []

        self.layer_num = len(layer_shape) - 1
        self.layers = []
        for index in range(len(layer_shape) - 1):
            self.layers.append(
                layer(layer_shape[index], layer_shape[index + 1], active_func))

    def train(self, datas):
        for it in range(self.n_iter):
            self.train_logger.append(0)
            delta_w = [np.zeros_like(layer.w) for layer in self.layers]
            delta_b = [np.zeros_like(layer.b) for layer in self.layers]
            samples = random.sample(datas, min(len(datas), self.step))
            for data in samples:
                z = loss = [
                    np.zeros([1, self.layers[-1].out_size], dtype=np.float64)
                ] * (self.layer_num + 1)
                x, y = data

                z[-1] = x
                for index in range(self.layer_num):
                    z[index] = self.layers[index].forward(z[index - 1])

                loss[self.layer_num - 1] = self.loss_func(
                    z[self.layer_num - 1], y)
                self.train_logger[-1] += abs(np.sum(loss[self.layer_num - 1]))

                for index in reversed(range(self.layer_num - 1)):
                    loss[index] = np.matmul(
                        loss[index + 1], self.layers[index + 1].w.transpose()
                    ) * self.active_func(z[index], d=1)

                for index in range(self.layer_num):
                    delta_w[index] -= np.matmul(z[index - 1].transpose(),
                                                loss[index])
                    delta_b[index] -= loss[index]

            tag = True
            for index in range(self.layer_num):
                delta_w[index] *= self.alpha
                delta_b[index] *= self.alpha
                tag &= np.max(np.abs(delta_w[index])) < self.epi
            if tag:
                break
            for index in range(self.layer_num):
                self.layers[index].w += delta_w[index]
                self.layers[index].b += delta_b[index]
            # print('%4d %.12f' % (it, self.train_logger[-1]))
        showLogger(self.train_logger, self.alpha)

    def predict(self, datas):
        Eval = []
        for data in datas:
            Eval.append(data)
            for layer in self.layers:
                Eval[-1] = layer.forward(Eval[-1])
        return Eval

    def save(self, agent_name):
        file = open('models/' + agent_name + '.agent', 'wb')
        pickle.dump(self.layers, file)
        file.close()

    def load(self, agent_name):
        try:
            file = open('models/' + agent_name + '.agent', 'rb')
        except:
            print('File', agent_name, 'not found')
            exit()
        self.layers = pickle.load(file)
        file.close()


if __name__ == '__main__':
    net = DNN(layer_shape=[300, 42, 6], active_func=relu)
    net.save('Testing')
    net.load('Testing')
