from constants import *
import copy
import numpy as np


class Piece(object):
    posVal = np.array(POS_VAL[0]).reshape(9, 10)

    def __init__(self, pos, player='None'):
        self.setPos(pos)
        self.player = player
        self.keys = self.getKeys()

    def displayPiece(self, screen):
        self.calcRect()
        screen.blit(self.img, self.rect)

    def moveable(self, campArr, targetPos):
        pass

    def getKeys(self):
        return 'None'

    def getScoreWeight(self):
        x, y = self.getPos()
        if self.player == 'Black':
            x, y = -x - 1, -y - 1
        return pieceScore[self.keys]

    def setPos(self, pos):
        self.x, self.y = pos

    def getPos(self):
        return (self.x, self.y)

    def getPosWeight(self, pos=(-1, -1)):
        if pos == (-1, -1):
            x, y = self.getPos()
        else:
            x, y = pos
        if self.player == 'Black':
            x, y = -x - 1, -y - 1
        return type(self).posVal[x][y]


class Rook(Piece):
    posVal = np.array(POS_VAL[2]).reshape(9, 10)

    def __init__(self, pos, player):
        Piece.__init__(self, pos, player)

    def getKeys(self):
        return 'b_rook' if self.player == 'Black' else 'r_rook'

    def moveable(self, campArr, targetPos):
        x, y = self.getPos()
        _x, _y = targetPos
        if x == _x and y == _y:
            return False
        if campArr[_x][_y] == self.player:
            return False

        dx, dy = sgn(_x - x), sgn(_y - y)
        if dx and dy:
            return False
        while x != _x or y != _y:
            x += dx
            y += dy
            if campArr[x][y] != 'None':
                break
        if x != _x or y != _y:
            return False

        return True


class Knight(Piece):
    posVal = np.array(POS_VAL[3]).reshape(9, 10)

    def __init__(self, pos, player):
        Piece.__init__(self, pos, player)

    def getKeys(self):
        return 'b_knight' if self.player == 'Black' else 'r_knight'

    def moveable(self, campArr, targetPos):
        x, y = self.getPos()
        _x, _y = targetPos
        if x == _x and y == _y:
            return False
        if campArr[_x][_y] == self.player:
            return False

        dx, dy = _x - x, _y - y
        if (abs(dx) == 1 and abs(dy) == 2) or (abs(dx) == 2 and abs(dy) == 1):
            dx = abs(dx) // 2 * sgn(dx)
            dy = abs(dy) // 2 * sgn(dy)
            if campArr[x + dx][y + dy] == 'None':
                return True
        return False


class Elephant(Piece):
    posVal = np.array(POS_VAL[5]).reshape(9, 10)

    def __init__(self, pos, player='None'):
        Piece.__init__(self, pos, player)

    def getKeys(self):
        return 'b_elephant' if self.player == 'Black' else 'r_elephant'

    def moveable(self, campArr, targetPos):
        x, y = self.getPos()
        _x, _y = targetPos
        if x == _x and y == _y:
            return False
        if campArr[_x][_y] == self.player:
            return False

        dx, dy = _x - x, _y - y
        if abs(dx) != abs(dy) or abs(dx) != 2:
            return False
        if campArr[x + sgn(dx)][y + sgn(dy)] != 'None':
            return False
        return True


class Mandarin(Piece):
    posVal = np.array(POS_VAL[6]).reshape(9, 10)

    def __init__(self, pos, player='None'):
        Piece.__init__(self, pos, player)

    def getKeys(self):
        return 'b_mandarin' if self.player == 'Black' else 'r_mandarin'

    def moveable(self, campArr, targetPos):
        x, y = self.getPos()
        _x, _y = targetPos
        if x == _x and y == _y:
            return False
        if campArr[_x][_y] == self.player:
            return False

        dx, dy = _x - x, _y - y
        if _x not in range(3, 6) or _y in range(3, 7):
            return False
        if abs(dx) != abs(dy) or abs(dx) != 1:
            return False
        return True


class King(Piece):
    posVal = np.array(POS_VAL[1]).reshape(9, 10)

    def __init__(self, pos, player='None'):
        Piece.__init__(self, pos, player)

    def getKeys(self):
        return 'b_king' if self.player == 'Black' else 'r_king'

    def moveable(self, campArr, targetPos):
        x, y = self.getPos()
        _x, _y = targetPos
        if x == _x and y == _y:
            return False
        if campArr[_x][_y] == self.player:
            return False

        dx, dy = _x - x, _y - y
        if _x not in range(3, 6) or _y in range(3, 7):
            return False
        if abs(dx) + abs(dy) != 1:
            return False
        return True


class Cannon(Piece):
    posVal = np.array(POS_VAL[4]).reshape(9, 10)

    def __init__(self, pos, player='None'):
        Piece.__init__(self, pos, player)

    def getKeys(self):
        return 'b_cannon' if self.player == 'Black' else 'r_cannon'

    def moveable(self, campArr, targetPos):
        x, y = self.getPos()
        _x, _y = targetPos
        if x == _x and y == _y:
            return False
        if campArr[_x][_y] == self.player:
            return False

        dx, dy = sgn(_x - x), sgn(_y - y)
        if dx and dy:
            return False
        tag = 0
        while x != _x or y != _y:
            x += dx
            y += dy
            if campArr[x][y] != 'None':
                tag += 1
        if tag == 2 and campArr[_x][_y] != 'None':
            return True
        if tag == 0:
            return True
        return False


class Pawn(Piece):
    posVal = np.array(POS_VAL[7]).reshape(9, 10)

    def __init__(self, pos, player='None'):
        Piece.__init__(self, pos, player)

    def getKeys(self):
        return 'b_pawn' if self.player == 'Black' else 'r_pawn'

    def moveable(self, campArr, targetPos):
        x, y = self.getPos()
        _x, _y = targetPos
        if x == _x and y == _y:
            return False
        if campArr[_x][_y] == self.player:
            return False

        dx, dy = _x - x, _y - y
        if abs(dx) + abs(dy) != 1:
            return False
        if self.player == 'Red':
            if dy < 0:
                return False
            if y < 5 and dx:
                return False
        else:
            if dy > 0:
                return False
            if y > 4 and dx:
                return False
        return True


def piecesListtoCampArr(piecesList):
    campArr = copy.deepcopy(noneArr)
    for piece in piecesList:
        x, y = piece.getPos()
        campArr[x][y] = piece.player
    return campArr
