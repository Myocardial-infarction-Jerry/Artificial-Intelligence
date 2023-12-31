import os
import tkinter as tk
import numpy as np

SEARCH_DEPTH = 3
INF = 1E7
SIGMA = 0.3

pieceScore = {
    'None': 0,
    'r_rook': 13,
    'b_rook': 13,
    'r_knight': 6,
    'b_knight': 6,
    'r_elephant': 2,
    'b_elephant': 2,
    'r_mandarin': 2,
    'b_mandarin': 2,
    'r_king': 1000,
    'b_king': 1000,
    'r_cannon': 6,
    'b_cannon': 6,
    'r_pawn': 3,
    'b_pawn': 3,
}

camp = {'None': 0, 'Black': -1, 'Red': 1, -1: 'Black', 0: 'None', 1: 'Red'}

POS_VAL = [
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    # 将
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, -8, -9, 0, 0, 0, 0, 0, 0, 0],
     [5, -8, -9, 0, 0, 0, 0, 0, 0, 0], [1, -8, -9, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    # 车
    [[-6, 5, -3, 4, 8, 8, 6, 6, 6, 6], [6, 8, 8, 9, 12, 11, 13, 8, 12, 8],
     [4, 6, 4, 4, 12, 11, 13, 7, 9,
      7], [12, 12, 12, 12, 14, 14, 16, 14, 16, -2],
     [0, 0, 12, 14, 15, 15, 16, 16, 33, 14],
     [12, 12, 12, 12, 14, 14, 16, 14, 16, -2],
     [4, 6, 4, 4, 12, 11, 13, 7, 9, 7], [6, 8, 8, 9, 12, 11, 13, 8, 12, 8],
     [-6, 5, -3, 4, 8, 8, 6, 6, 6, 6]],
    # 马
    [[0, -3, 5, 4, 2, 2, 5, 4, 2, 2], [-3, 2, 4, 6, 10, 12, 20, 10, 8, 2],
     [2, 4, 6, 10, 13, 11, 12, 11, 15, 2], [0, 5, 7, 7, 14, 15, 19, 15, 9, 8],
     [2, -10, 4, 10, 15, 16, 12, 11, 6, 2], [0, 5, 7, 7, 14, 15, 19, 15, 9, 8],
     [2, 4, 6, 10, 13, 11, 12, 11, 15, 2], [-3, 2, 4, 6, 10, 12, 20, 10, 8, 2],
     [0, -3, 5, 4, 2, 2, 5, 4, 2, 2]],
    # 炮
    [[0, 0, 1, 0, -1, 0, 0, 1, 2, 4], [0, 1, 0, 0, 0, 0, 3, 1, 2, 4],
     [1, 2, 4, 0, 3, 0, 3, 0, 0, 0], [3, 2, 3, 0, 0, 0, 2, -5, -4, -5],
     [3, 2, 5, 0, 4, 4, 4, -4, -7, -6], [3, 2, 3, 0, 0, 0, 2, -5, -4, -5],
     [1, 2, 4, 0, 3, 0, 3, 0, 0, 0], [0, 1, 0, 0, 0, 0, 3, 1, 2, 4],
     [0, 0, 1, 0, -1, 0, 0, 1, 2, 4]],
    # 象
    [[0, 0, -2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, -2, 0, 0, 0, 0, 0, 0, 0]],
    # 士
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    # 兵
    [[0, 0, 0, -2, 3, 10, 20, 20, 20, 0], [0, 0, 0, 0, 0, 18, 27, 30, 30, 0],
     [0, 0, 0, -2, 4, 22, 30, 45, 50, 0], [0, 0, 0, 0, 0, 35, 40, 55, 65, 2],
     [0, 0, 0, 6, 7, 40, 42, 55, 70, 4], [0, 0, 0, 0, 0, 35, 40, 55, 65, 2],
     [0, 0, 0, -2, 4, 22, 30, 45, 50, 0], [0, 0, 0, 0, 0, 18, 27, 30, 30, 0],
     [0, 0, 0, -2, 3, 10, 20, 20, 20, 0]],
]

noneArr = [
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
    [
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
        'None',
    ],
]

pieceDic = {
    'r_pawn': '兵',
    'r_cannon': '炮',
    'r_knight': '馬',
    'r_rook': '車',
    'r_elephant': '相',
    'r_mandarin': '仕',
    'r_king': '帅',
    'b_pawn': '卒',
    'b_cannon': '砲',
    'b_knight': '馬',
    'b_rook': '車',
    'b_elephant': '象',
    'b_mandarin': '士',
    'b_king': '将'
}


def sgn(val):
    if val > 0:
        return 1
    elif val == 0:
        return 0
    else:
        return -1


if __name__ == '__main__':
    for posVal in POS_VAL:
        print(np.array(posVal).reshape(9, 10).tolist(), ',')
