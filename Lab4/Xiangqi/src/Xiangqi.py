from pieces import *
from constants import *
import numpy as np


class Xiangqi(object):

    def __init__(self):
        self.piecesList = []

        # Player Black Pieces
        self.piecesList.append(Rook([0, 9], 'Black'))
        self.piecesList.append(Rook([8, 9], 'Black'))
        self.piecesList.append(Cannon([1, 7], 'Black'))
        self.piecesList.append(Cannon([7, 7], 'Black'))
        self.piecesList.append(Knight([1, 9], 'Black'))
        self.piecesList.append(Knight([7, 9], 'Black'))
        self.piecesList.append(Pawn([0, 6], 'Black'))
        self.piecesList.append(Pawn([2, 6], 'Black'))
        self.piecesList.append(Pawn([4, 6], 'Black'))
        self.piecesList.append(Pawn([6, 6], 'Black'))
        self.piecesList.append(Pawn([8, 6], 'Black'))
        self.piecesList.append(Elephant([2, 9], 'Black'))
        self.piecesList.append(Elephant([6, 9], 'Black'))
        self.piecesList.append(Mandarin([3, 9], 'Black'))
        self.piecesList.append(Mandarin([5, 9], 'Black'))
        self.piecesList.append(King([4, 9], 'Black'))

        # Player Red Pieces
        self.piecesList.append(Rook([0, 0], 'Red'))
        self.piecesList.append(Rook([8, 0], 'Red'))
        self.piecesList.append(Cannon([1, 2], 'Red'))
        self.piecesList.append(Cannon([7, 2], 'Red'))
        self.piecesList.append(Knight([1, 0], 'Red'))
        self.piecesList.append(Knight([7, 0], 'Red'))
        self.piecesList.append(Pawn([0, 3], 'Red'))
        self.piecesList.append(Pawn([2, 3], 'Red'))
        self.piecesList.append(Pawn([4, 3], 'Red'))
        self.piecesList.append(Pawn([6, 3], 'Red'))
        self.piecesList.append(Pawn([8, 3], 'Red'))
        self.piecesList.append(Elephant([2, 0], 'Red'))
        self.piecesList.append(Elephant([6, 0], 'Red'))
        self.piecesList.append(Mandarin([3, 0], 'Red'))
        self.piecesList.append(Mandarin([5, 0], 'Red'))
        self.piecesList.append(King([4, 0], 'Red'))

    def actionList(self):
        campArr = piecesListtoCampArr(self.piecesList)
        actionList = []
        for pieceIndex in range(len(self.piecesList)):
            for x in range(9):
                for y in range(10):
                    if self.piecesList[pieceIndex].moveable(campArr, (x, y)):
                        actionList.append((pieceIndex, (x, y)))
        return actionList

    def move(self, action, logger=False):
        if logger:
            self.printAction(action)

        pieceIndex, targetPos = action
        self.piecesList[pieceIndex].setPos(targetPos)
        for targetIndex in range(len(self.piecesList)):
            if self.piecesList[targetIndex].getPos(
            ) == targetPos and targetIndex != pieceIndex:
                self.piecesList.pop(targetIndex)
                break

    def searchPos(self, pos):
        for pieceIndex in range(len(self.piecesList)):
            if self.piecesList[pieceIndex].getPos() == pos:
                return pieceIndex
        return -1

    def terminated(self):
        count = 0
        for piece in self.piecesList:
            if type(piece) == King:
                count += 1
        if count != 2:
            return True

    def printAction(self, action):
        pieceIndex, targetPos = action
        piecePos = self.piecesList[pieceIndex].getPos()
        print(self.piecesList[pieceIndex].keys, 'from', piecePos, 'to',
              targetPos)


if __name__ == '__main__':
    state = Xiangqi()
    print(np.array(piecesListtoCampArr(state.piecesList)))