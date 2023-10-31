import numpy as np
import random

direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def generate(step_limit=500):
    global direction
    state = np.array(list(range(1, 16)) + [0]).reshape(4, 4)
    expectation = random.randint(1, step_limit)
    for step in range(expectation):
        x, y = np.array(np.where(state == 0)).reshape(2)
        dx, dy = direction[random.randint(0, 3)]
        _x, _y = x + dx, y + dy
        if _x in range(4) and _y in range(4):
            state[x][y], state[_x][_y] = state[_x][_y], state[x][y]
    return state, expectation
