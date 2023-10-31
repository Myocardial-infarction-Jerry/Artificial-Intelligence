import random
from queue import PriorityQueue
from lib import *
from constants import *
from dataclasses import dataclass, field
from typing import Any
import time


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


def decoding(chro):
    N = len(chro)
    path = [(chro[k], k) for k in range(N)]
    path.sort()
    sol = [path[k][1] for k in range(N)]
    return sol


def PMX(chroA, chroB):
    N = len(chroA)
    i, j = sorted(random.sample(range(N), 2))
    return chroA[:i] + chroB[i:j] + chroA[j:]


def PBX(chroA, chroB):
    N = len(chroA)
    t = sorted(random.sample(range(N), N // 2))
    newChro = [chroA[i] if i in t else chroB[i] for i in range(N)]
    return newChro


def mutation(coords, initChro):
    mutateOpt = [optSwap, optInsert, optInverse]
    i, j = sorted(random.sample(range(len(initChro)), 2))
    newChro, newDis = None, INF
    for opt in mutateOpt:
        chro = opt(initChro, i, j)
        dis = calcDis(coords, decoding(chro))
        if dis < newDis:
            newChro, newDis = chro[:], dis
    return newChro


def crossover(coords, chroA, chroB):
    crossOpt = [PMX, PBX]
    newChro, newDis = None, INF
    for opt in crossOpt:
        chro = opt(chroA, chroB)
        dis = calcDis(coords, decoding(chro))
        if dis < newDis:
            newChro, newDis = chro[:], dis
    return newChro


def reproduction(coords, chros, population):
    crossOpt = [PMX, PBX]

    while chros.qsize() < population * REPROD_RATE:
        i, j = sorted(random.sample(range(chros.qsize()), 2))
        chroA, chroB = chros.queue[i].item, chros.queue[j].item
        newChro = crossover(coords, chroA, chroB)
        if random.random() < MUTATEPROD:
            newChro = mutation(coords, newChro)
        chros.put(
            PrioritizedItem(priority=-calcDis(coords, decoding(newChro)),
                            item=newChro[:]))


def GA(coords):
    # Time counter
    baseTime = time.time()

    N = len(coords)
    population = POPULATION

    # Generate initial generation
    chros = PriorityQueue()
    for k in range(population):
        chro = [random.random() for tmp in range(N)]
        chros.put(
            PrioritizedItem(priority=-calcDis(coords, decoding(chro)),
                            item=chro[:]))

    # Generation iterate
    logger = []
    for it in range(GENERATION_ITER):
        reproduction(coords, chros, population)
        while chros.qsize() > population:
            chros.get()

        logger.append(-chros.get().priority)

        # Terminate condition
        if len(logger) > LIMIT and logger[-LIMIT] - logger[-1] < 1:
            break

        print(logger[-1])

    usedTime = time.time() - baseTime

    # Output the winner
    while chros.qsize() > 1:
        chros.get()
    item = chros.get()

    showLogger(logger)
    return decoding(item.item), -item.priority, usedTime
