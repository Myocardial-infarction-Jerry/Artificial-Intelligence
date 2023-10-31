# 中山大学 本科生实验报告

实验课程：人工智能

实验名称：Lab3 启发式搜索

专业名称：计算机科学与技术

学生姓名：刘森元

学生学号：21307289

实验地点：广州校区东校园 实验中心 D501

报告时间：2023-04-05



***本人使用的环境如下：***

***Apple Inc. MacBook Pro 2021***

***M1 Pro (Apple Silicon)***

***使用的文献、软件、包大部分以超连接形式给出了原址。***



## 一、实验题目

使用 [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) 与 [IDA*](https://en.wikipedia.org/wiki/Iterative_deepening_A*) 算法解决 [15-Puzzle](https://en.wikipedia.org/wiki/15_puzzle) 问题，启发式函数可以自己选取，最好多尝试几种不同的启发式函数。

## 二、实验内容

### 1. A* 

**1) 算法原理**

从起始节点开始，不断查询周围可到达节点的状态并计算它们的 f(x), h(x), g(x) 的值，选取估价函数 f(x) 最小的节点进行下一步扩展，并同时更新已经被访问过的节点的 g(x)，直到找到目标节点。其中 f(x) = g(x) + h(x)

**2) 算法流程**

```pseudocode
open add start_state
while open is not empty:
	state = min f(state) in open
	close add state
	open remove state
	
	for next_state near state:
		if next_state not in close:
			open add next_state
			if next_state = end_state:
				return ans
```

**3) 关键代码展示**

*def A_star*

```python
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
```

### 2. IDA*

**1) 算法原理**

在算法迭代的每一步，IDA* 都进行深度优先搜索，在某一步所有可访问节点对应的最小可估价函数值大于某个给定的阈值的时候，将会剪枝。

**2) 算法流程**

```pseudocode
open add start_state
new_open = open
while open = new_open:
	for state in open:
		expand state till f(state) > lim
	lim increase
	open = new_open
	
	if state = end_state
		return ans
```

**3) 关键代码展示**

*def IDA_star*

```python
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
```

*def expand*

```python
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
```

### 3. 创新点 & 优化

1. 在 Euclid distance & Manhattan distance 的 Evaluate function 实现之上，增加了 Weighted Manhattan 的实现方法，在求解速度上有了极大提升

   **Weighted Manhattan**

   针对 15-Puzzle 问题进行分析，tile 之间的移动可视作 “空格” 这个位置的上下左右移动。根据最终状态的特征，我们可以发现对于 tile 之间的复原优先级是不一样的。

   ![img](https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/15-puzzle-loyd.svg/220px-15-puzzle-loyd.svg.png)

   对于左上方的 tile 显然优先级更高，而右下方的 tile 优先级相对较低，故我们易得出 Weighted Manhattan 这一方法，经过反复调参尝试最后有参数如下：

   ```python
   # Weight value of weighted manhattan
   weight = [0, 9, 8, 7, 6, 8, 6, 5, 4, 7, 5, 3, 2, 6, 4, 2, 1]
   
   # Weight rate
   sigma = 0.9101
   ```

   

2. 函数对 evaluate, move 等方法以接口方式提供，使得代码复用性高，面对其他类型的问题时，仅需修改 evaluate, move 等函数即可

3. 引入了 time_limit 参数，使得程序在运行时可控

## 三、实验结果及分析

### 1. 实验结果展示示例

**1) A***

![image-20230405163538049](/Users/qiu_nangong/Library/Application Support/typora-user-images/image-20230405163538049.png)

**2) IDA***

![image-20230405172119195](/Users/qiu_nangong/Library/Application Support/typora-user-images/image-20230405172119195.png)

### 2. 实验指标展示及分析

针对部分随机生成数据进行分析

```
Test 74      18   0.003005    A*   with weighted manhattan
Test 74      18   0.005782    A*   with euclid
Test 74      18   0.003857    A*   with manhattan
Test 74      68   1.385930    IDA* with weighted manhattan
Test 74      -1   Timeout     IDA* with euclid
Test 74      18   0.005950    IDA* with manhattan
```

```
Test 220     49   0.269482    A*   with weighted manhattan
Test 220     33   6.334663    A*   with euclid
Test 220     33   1.155782    A*   with manhattan
Test 220     103  1.416961    IDA* with weighted manhattan
Test 220     -1   Timeout     IDA* with euclid
Test 220     -1   Timeout     IDA* with manhattan
```

```
Test 212     62   0.512010    A*   with weighted manhattan
Test 212     -1   Timeout     A*   with euclid
Test 212     34   7.584871    A*   with manhattan
Test 212     96   1.430310    IDA* with weighted manhattan
Test 212     -1   Timeout     IDA* with euclid
Test 212     -1   Timeout     IDA* with manhattan
```

可以发现针对 15-Puzzle 问题，由于搜索状态众多，空间复杂度较高，A* 表现总体优于 IDA*。而在 Evaluate function 的区别上，Weighted Manhattan 的表现力压 Manhattan & Euclid，在牺牲最优解的情况下，求解速度大大提升。

下图为 10s Limit, 500 Tests 的横向对比测试

![image-20230406113653375](/Users/qiu_nangong/Library/Application Support/typora-user-images/image-20230406113653375.png)

## 四、参考资料

[15-Puzzle on Wikipedia](https://en.wikipedia.org/wiki/15_puzzle)

[A* Search Algorithm on Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)

[IDA* Search Algorithm on Wikipedia](https://en.wikipedia.org/wiki/Iterative_deepening_A*)

[Idea of constructing Weighted Manhattan Matrix](https://stackoverflow.com/questions/94975/how-do-you-solve-the-15-puzzle-with-a-star-or-dijkstras-algorithm)

## 五、源代码

*main.py*

```python
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
```

*random_test.py*

```python
import generate
import time
import main


class test_class(object):

    def __init__(self, name, time_limit, test_method, evaluate):
        self.name = name
        self.time_limit = time_limit
        self.test_method = test_method
        self.time_count = 0
        self.pass_count = 0
        self.evaluate = evaluate

    def test(self, state):
        base = time.time()
        ans = self.test_method(state,
                               evaluate=self.evaluate,
                               time_limit=self.time_limit)
        used = time.time() - base
        if used < time_limit:
            self.time_count += used
            self.pass_count += 1
            return ans, used
        else:
            self.time_count += time_limit
            return -1, -1.0

    def count(self):
        return self.time_count, self.pass_count


if __name__ == '__main__':
    pass_count = 0
    time_count = 0
    n = int(input('Test number: '))
    time_limit = float(input('Time limit(s): '))

    methods = [
        test_class('A*   with weighted manhattan', time_limit, main.A_star,
                   main.evaluate),
        test_class('A*   with euclid', time_limit, main.A_star,
                   main.evaluate_euclid),
        test_class('A*   with manhattan', time_limit, main.A_star,
                   main.evaluate_manhattan),
        test_class('IDA* with weighted manhattan', time_limit, main.IDA_star,
                   main.evaluate),
        test_class('IDA* with euclid', time_limit, main.IDA_star,
                   main.evaluate_euclid),
        test_class('IDA* with manhattan', time_limit, main.IDA_star,
                   main.evaluate_manhattan),
    ]

    for test in range(n):
        state, expectation = generate.generate(step_limit=200)

        for method in methods:
            ans, used = method.test(state)
            if used == -1:
                str = ("Test %-4d    %-4d Timeout     " + method.name) % (test,
                                                                          ans)
            else:
                str = ("Test %-4d    %-4d %-10f  " + method.name) % (test, ans,
                                                                     used)
            print(str)

        print('')

    for method in methods:
        time_count, pass_count = method.count()
        str = ('Average Time = %-10f Pass Rate = %-10f  ' +
               method.name) % (time_count / n, pass_count / n)
        print(str)
```

*generate.py*

```python
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
```

