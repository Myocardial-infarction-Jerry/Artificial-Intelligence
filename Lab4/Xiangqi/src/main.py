from Xiangqi import *
from pieces import *
from AI_brain import *
from constants import *
import tkinter as tk
from tkinter.messagebox import showinfo


class XiangqiGame(Xiangqi):

    def __init__(self):
        self.env = Xiangqi()
        self.lastPos = (-1, -1)

        self.window = tk.Tk()
        self.window.title('中国象棋')
        self.window.resizable(False, False)
        self.board = tk.Canvas(self.window,
                               width=630,
                               height=700,
                               background='lightgrey')
        self.board.pack()
        self.refreshBoard()
        self.board.bind('<Button -1>', self.click)
        self.window.mainloop()

    def drawChessBoard(self):
        for i in range(0, 9):
            if i == 0 or i == 8:
                self.board.create_line(i * 70 + 35, 35, i * 70 + 35, 665)
            else:
                self.board.create_line(i * 70 + 35, 35, i * 70 + 35, 315)
                self.board.create_line(i * 70 + 35, 385, i * 70 + 35, 665)
        for i in range(0, 10):
            self.board.create_line(35, i * 70 + 35, 595, i * 70 + 35)

        self.board.create_line(245, 35, 385, 175)
        self.board.create_line(385, 35, 245, 175)
        self.board.create_line(245, 525, 385, 665)
        self.board.create_line(385, 525, 245, 665)
        self.board.create_text(175, 350, text='楚   河', font=('华文隶书', 50))
        self.board.create_text(455, 350, text='汉   界', font=('华文隶书', 50))

    def drawChessPieces(self):
        for piece in self.env.piecesList:
            piecePos = piece.getPos()
            i, j = piecePos
            j = 9 - j
            if piecePos == self.lastPos:
                self.board.create_oval(70 * i + 5,
                                       70 * j + 5,
                                       70 * i + 65,
                                       70 * j + 65,
                                       fill='green')
                self.board.create_oval(70 * i + 9,
                                       70 * j + 9,
                                       70 * i + 61,
                                       70 * j + 61,
                                       fill='green')
            else:
                self.board.create_oval(70 * i + 5,
                                       70 * j + 5,
                                       70 * i + 65,
                                       70 * j + 65,
                                       fill='white')
                self.board.create_oval(70 * i + 9,
                                       70 * j + 9,
                                       70 * i + 61,
                                       70 * j + 61,
                                       fill='white')
            self.board.create_text(70 * i + 35,
                                   70 * j + 35,
                                   text=pieceDic[piece.keys],
                                   fill=piece.player,
                                   font=('华文中宋', 25))

    def click(self, event):
        clickPos = (event.x // 70, 9 - event.y // 70)
        if self.lastPos == (-1, -1):
            pieceIndex = self.env.searchPos(clickPos)
            if pieceIndex == -1:
                return
            piece = self.env.piecesList[pieceIndex]
            if piece.player == 'Black':
                return
            self.lastPos = clickPos
        else:
            pieceIndex = self.env.searchPos(self.lastPos)
            self.lastPos = (-1, -1)
            piece = self.env.piecesList[pieceIndex]
            if piece.moveable(piecesListtoCampArr(self.env.piecesList),
                              clickPos):
                self.env.move([pieceIndex, clickPos], logger=True)
                self.refreshBoard()
                val, action = alpha_beta(self.env, 0)
                if action == None:
                    showinfo('红方获胜')
                    self.window.destroy()
                else:
                    self.env.move(action, logger=True)
                self.refreshBoard()
                if self.env.terminated():
                    showinfo('黑方获胜')
                    self.window.destroy()
        self.refreshBoard()

    def refreshBoard(self):
        self.board.delete('all')
        self.drawChessBoard()
        self.drawChessPieces()


if __name__ == '__main__':
    mainGame = XiangqiGame()
    print("game over")
