import numpy as np
import time
import queue

direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]

# Weight value of weighted manhattan
weight = [0, 9, 8, 7, 6, 8, 6, 5, 4, 7, 5, 3, 2, 6, 4, 2, 1]

# Weight rate
sigma = 0.9101

# End state definition
end = np.array(list(range(1, 16)) + [0]).reshape(4, 4)


# Evaluate function based on euclid distance
def evaluate_euclid(state, end):
    key = 0
    for val in range(1, 16):
        loca, locb = np.where(state == val), np.where(end == val)
        key += ((loca[0][0] - locb[0][0])**2 +
                (loca[1][0] - locb[1][0])**2)**0.5
    return key


# Evaluate function based on manhattan distance
def evaluate_manhattan(state, end):
    key = 0
    for val in range(1, 16):
        loca, locb = np.where(state == val), np.where(end == val)
        key += abs(loca[0][0] - locb[0][0]) + abs(loca[1][0] - locb[1][0])
    return key


# Evaluate function based on weighted manhattan distance
def evaluate(state, end):
    global weight, sigma
    key = 0
    for val in range(1, 16):
        loca, locb = np.where(state == val), np.where(end == val)
        key += (abs(loca[0][0] - locb[0][0]) +
                abs(loca[1][0] - locb[1][0])) * weight[val]
    return key * sigma


# Fetch near state
def move(current_state):
    global direction
    x, y = np.array(np.where(current_state == 0)).reshape(2)
    next_states = []
    for dx, dy in direction:
        _x, _y = x + dx, y + dy
        if _x in range(4) and _y in range(4):
            next_state = np.copy(current_state)
            next_state[x][y], next_state[_x][_y] = next_state[_x][
                _y], next_state[x][y]
            next_states.append(np.copy(next_state))
    return next_states


def A_star(start, evaluate=evaluate, move=move, time_limit=10):
    global end
    # Time counter
    base = time.time()
    if (start == end).all():
        return 0

    open = queue.PriorityQueue()
    open.put((evaluate(start, end), 0, start.tolist()))
    close = set()
    while not open.empty():
        key, step, state = open.get()
        state = np.array(state)
        close.add(tuple(state.reshape(1, -1)[0]))

        # Timeout handler
        if time.time() - base > time_limit:
            return -1

        for cur in move(state):
            if tuple(cur.reshape(1, -1)[0]) in close:
                continue
            open.put((evaluate(cur, end) + step + 1, step + 1, cur.tolist()))
            if (cur == end).all():
                return step + 1
    return -1


# Iterative deepening, Limit open list length < customize argument "Len"
def expand(state, step, open, close, lim, evaluate, move, Len):
    global end
    close.add(tuple(state.reshape(1, -1)[0]))

    tag = False
    ans = -1

    # open list length limiter
    if len(open) < Len:
        for cur in move(state):
            if tuple(cur.reshape(1, -1)[0]) in close:
                continue

            if evaluate(cur, end) + step + 1 > lim:
                continue

            _tag, _ans = expand(cur, step + 1, open, close, lim, evaluate,
                                move, Len)
            tag = True
            ans = _ans if _ans != -1 else ans

    if not tag:
        open.append([tuple(state.reshape(1, -1)[0]), step])

    if (state == end).all():
        ans = step

    return tag, ans


def IDA_star(start, evaluate=evaluate, move=move, time_limit=10, Len=5000):
    # Time counter
    base = time.time()
    open = []
    open.append([tuple(start.reshape(1, -1)[0]), 0])
    close = set()
    lim = 0

    while True:
        lim += 1
        new_open = []
        for state, step in open:
            state = np.array(start).reshape(4, 4)
            tag, ans = expand(state, step, new_open, close, lim, evaluate,
                              move, Len)

            # Timeout handler
            if time.time() - base > time_limit:
                return -1

            if ans != -1:
                return ans

        if len(new_open) > Len:
            lim = 0
        open = new_open


if __name__ == '__main__':
    start = []
    while len(start) != 16:
        start += input().split()
    start = np.array(start, dtype=int).reshape(4, 4)
    # print(A_star(start, time_limit=10))
    print(IDA_star(start, time_limit=10))
