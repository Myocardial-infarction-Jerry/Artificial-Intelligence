import matplotlib.pyplot as plt
from constants import *
import random
import math


def optSwap(sol, i, j):
    newSol = sol[:]
    newSol[i], newSol[j] = newSol[j], newSol[i]
    return newSol


def optInverse(sol, i, j):
    rev = sol[i:j]
    rev.reverse()
    newSol = sol[:i] + rev + sol[j:]
    return newSol


def optInsert(sol, i, j):
    newSol = sol[:i] + [sol[j]] + sol[i:j] + sol[j + 1:]
    return newSol


def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def calcDis(coords, sol):
    dis = 0
    for i in range(len(sol)):
        dis += distance(coords[sol[i]], coords[sol[i - 1]])
    return dis


def drawPath(coords, sol, title=''):
    x = [coord[0] for coord in coords]
    y = [coord[1] for coord in coords]
    for i in range(len(sol)):
        start = sol[i - 1]
        end = sol[i]
        plt.plot([coords[start][0], coords[end][0]],
                 [coords[start][1], coords[end][1]], 'c')
    plt.plot(x, y, 'bo')
    plt.title(title)
    plt.show()


def showLogger(logger):
    for k in range(1, len(logger)):
        plt.plot([k - 1, k], [logger[k - 1], logger[k]], 'c')
    plt.xlabel('Times')
    plt.ylabel('Current optimal')
    plt.title('TSP Problem')
    plt.show()