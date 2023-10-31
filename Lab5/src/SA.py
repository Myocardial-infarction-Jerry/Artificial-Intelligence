import math
import random
from constants import *
from queue import PriorityQueue
from lib import *
import time


def perturbSol(coords, sol):
    bestSol, bestDis = [], INF
    methods = [optSwap, optInverse, optInsert]
    i, j = sorted(random.sample(range(len(coords)), 2))
    for method in methods:
        # i, j = sorted(random.sample(range(len(coords)), 2))
        newSol = method(sol, i, j)
        newDis = calcDis(coords, newSol)
        if newDis < bestDis:
            bestSol, bestDis = newSol[:], newDis

    return bestSol, bestDis


def SA(coords, p0=ACCEPTPROD, showImg=False):
    # Time counter
    baseTime = time.time()

    # Generate inittial temperature list
    x = list(range(len(coords)))
    random.shuffle(x)
    xDis = calcDis(coords, x)  # Generate initial sol x
    L = PriorityQueue(maxsize=MAX_L * 2)  # Generate temperature list
    for k in range(MAX_L):
        y, yDis = perturbSol(coords, x)
        if yDis < xDis:
            x, xDis = y, yDis
        temp = -abs(yDis - xDis) / math.log(p0)
        L.put(-temp)

    logger = []  # Distance logger
    solLogger = []  # Solution logger

    # List-based Simulated Annealing
    for k in range(MAX_L):
        t_max = -L.get()
        t = 0
        c = 0
        for it in range(MAX_ITER):
            y, yDis = perturbSol(coords, x)
            r = random.random()
            if r > acceptProb(xDis, yDis, t_max):
                continue
            if yDis > xDis:
                t = (t - (yDis - xDis)) / math.log(r)
                c += 1
            x, xDis = y, yDis

            if showImg and len(logger) % 10000 == 0:
                solLogger.append(x)
            logger.append(xDis)

        if c:
            L.put(-t / c)
        else:
            L.put(-t_max)

    # Time counter
    usedTime = time.time() - baseTime

    # Show the image of soluts in process
    if showImg:
        for index in range(len(solLogger)):
            drawPath(coords, solLogger[index],
                     'Sol after ' + str(index * 10000) + ' times of annealing')

    # Show the image of annealing process
    showLogger(logger)
    return x, xDis, usedTime


def acceptProb(dis, newDis, temp):
    if newDis < dis:
        return 1.0
    else:
        return math.exp((dis - newDis) / temp)
