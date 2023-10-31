from Xiangqi import *
from pieces import *
from constants import *
import copy
import numpy as np
import random
import time


def evaluate(state):
    value = 0
    campNone = 'None'
    campArr = piecesListtoCampArr(state.piecesList)
    for piece in state.piecesList:
        value += (piece.getScoreWeight() +
                  piece.getPosWeight()) * camp[piece.player]
        for x in range(9):
            for y in range(10):
                targetPos = (x, y)
                if piece.moveable(campArr, targetPos):
                    targetIndex = state.searchPos(targetPos)
                    if targetIndex == -1:
                        value += piece.getPosWeight(targetPos) * camp[
                            piece.player] * SIGMA
                    else:
                        targetPiece = state.piecesList[targetIndex]
                        value += targetPiece.getScoreWeight(
                        )**2 / piece.getScoreWeight() * camp[piece.player]

    return value


def alpha_beta(state, depth, alpha=-INF, beta=INF):
    if state.terminated():
        return -1E8, None
    if depth == SEARCH_DEPTH:
        return evaluate(state) * (-1)**(depth + 1), None
    val, chosenAction = -INF, None
    actionList = state.actionList()
    random.shuffle(actionList)
    for action in actionList:
        pieceIndex, targetPos = action
        if state.piecesList[pieceIndex].player != camp[(-1)**(depth + 1)]:
            continue

        nextState = copy.deepcopy(state)
        nextState.move(action)
        _val, _action = alpha_beta(nextState, depth + 1, -beta, -alpha)
        if -_val > val:
            val, chosenAction = -_val, action
        if val >= beta:
            return val, chosenAction
        alpha = max(alpha, val)
    print('alpha=%15.2f beta=%15.2f' % (alpha, beta))
    return val, chosenAction


if __name__ == '__main__':
    state = Xiangqi()
    global timeCount
    base = time.time()
    timeCount = 0
    val, action = alpha_beta(state, 0)
    state.printAction(action)
    print(timeCount, timeCount / (time.time() - base))
