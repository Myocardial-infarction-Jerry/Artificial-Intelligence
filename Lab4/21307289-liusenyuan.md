# 中山大学 本科生实验报告

实验课程：人工智能

实验名称：用 Alpha-beta 剪枝算法设计一个中国象棋博弈程序

专业名称：计算机科学与技术

学生姓名：刘森元

学生学号：21307289

实验地点：广州校区东校园 实验中心 D501

报告时间：2023-04-24



***本人使用的环境如下：***

***Apple Inc. MacBook Pro 2021***

***M1 Pro (Apple Silicon)***

***使用的文献、软件、包大部分以超连接形式给出了原址。***



## 一、实验题目

> 编写一个中国象棋博弈程序，要求用 [alpha-beta](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) 剪枝算法，可以实现人机对弈。棋局评估方法可以参考已有文献，要求具有下棋界面，界面编程也可以参考网上程序，但正式实验报告要引用参考过的文献和程序。

## 二、实验内容

### 1. 算法原理

alpha-beta剪枝是一种在博弈树搜索中减少计算量的常用算法。它利用了极大值和极小值之间的关系，将某些子树的搜索过程剪枝，从而可以减少搜索的深度和节点数。

alpha-beta剪枝的基本原理是：在极大值和极小值中，如果发现一个节点的值不会影响到其父亲节点的选择，那么就可以直接剪掉该节点的搜索。具体的实现方式是，维护两个变量alpha和beta，它们分别代表当前极大节点已知的最小值和极小节点已知的最大值。如果一个搜索到的节点的值小于等于alpha或者大于等于beta，那么可以直接剪枝不再继续搜索。

alpha-beta剪枝算法的具体实现一般采用递归的方式，首先从根节点开始搜索，假设当前节点是极大节点，那么就搜索其所有子节点中的最大值并更新alpha值。如果发现一个节点的值小于等于alpha，那么就可以剪枝不再搜索其子树。如果当前节点是极小节点，那么就搜索其所有子节点中的最小值并更新beta值。如果发现一个节点的值大于等于beta，那么就可以剪枝不再搜索其子树。

在实际应用中，alpha-beta剪枝算法可以显著地减少搜索深度和节点数，从而大大提高搜索效率。它被广泛应用于博弈和人工智能领域中。

### 2. 伪代码

```pseudocode
function alpha_beta(node, alpha, beta, maximizingPlayer):
    if node is a terminal node:
        return the value of node
     if maximizingPlayer:
        v = -infinity
        for each child of node:
            v = max(v, alpha_beta(child, alpha, beta, false))
            alpha = max(alpha, v)
            if beta <= alpha:
                break   // beta剪枝
        return v
    else:
        v = +infinity
        for each child of node:
            v = min(v, alpha_beta(child, alpha, beta, true))
            beta = min(beta, v)
            if beta <= alpha:
                break   // alpha剪枝
        return v
```
其中， `node` 是当前搜索的节点， `maximizingPlayer` 是一个布尔值，表示当前节点是极大节点还是极小节点。

 `alpha` 和 `beta` 分别代表当前极大节点已知的最小值和极小节点已知的最大值。在搜索过程中，对于每个极大节点，都会搜索其所有子节点中的最大值，并更新 `alpha` 值。如果发现某个子节点的值小于等于 `alpha` ，那么就会直接剪枝并停止搜索该子节点的子树。对于每个极小节点，都会搜索其所有子节点中的最小值，并更新 `beta` 值。如果发现某个子节点的值大于等于 `beta` ，那么就会直接剪枝并停止搜索该子节点的子树。

### 3. 关键代码展示

```python
def alpha_beta(state, depth, alpha=-INF, beta=INF):
    # 如果游戏已经结束，返回一个很小的负数和空的操作
    if state.terminated():
        return -1E8, None
    # 如果搜索达到了设定的深度，返回当前局面的估值和空的操作
    if depth == SEARCH_DEPTH:
        return evaluate(state) * (-1)**(depth + 1), None
    # 初始化val、chosenAction的值
    val, chosenAction = -INF, None
    # 获取所有可以执行的操作，并打乱顺序
    actionList = state.actionList()
    random.shuffle(actionList) 
    # 遍历所有操作
    for action in actionList:
        pieceIndex, targetPos = action
        # 如果该棋子不是当前玩家的，跳过
        if state.piecesList[pieceIndex].player != camp[(-1)**(depth + 1)]:
            continue
        # 复制当前局面，模拟该操作
        nextState = copy.deepcopy(state)
        nextState.move(action)
        # 利用递归，获取下一个局面的估值和操作
        _val, _action = alpha_beta(nextState, depth + 1, -beta, -alpha) 
        # 如果_val更优，更新val和chosenAction
        if -_val > val:
            val, chosenAction = -_val, action
        # beta剪枝
        if val >= beta:
            return val, chosenAction
        # 更新alpha
        alpha = max(alpha, val)
    # 输出当前的alpha和beta值
    print('alpha=%15.2f beta=%15.2f' % (alpha, beta))
    # 返回最佳估值和操作
    return val, chosenAction
```

### 4. 创新点 & 优化

1. 代码中采用了随机打乱所有可执行操作的顺序，以避免搜索出现周期性重复的情况
2. 代码中对于当前玩家无法操作的棋子进行了过滤，减少了搜索的时间和复杂度   

## 三、实验结果及分析

### 1. 实验结果展示示例

![image-20230425204620725](/Users/qiu_nangong/Library/Application Support/typora-user-images/image-20230425204620725.png)

### 2. 评测指标展示及分析

在与一般水平的人对弈上, 算法胜率如下:

| 搜索深度 | 决策平均时间 | 胜率 |
| -------- | ------------ | ---- |
| 3        | 1.3s         | 17%  |
| 4        | 7.5s         | 43%  |
| 5        | 48.8s        | 56%  |

可见随着搜索深度加深, 算法棋力同步上升, 但耗时大幅增加

## 四、参考资料

[Alpha-beta pruning on Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

[TkInter on Python.org](https://wiki.python.org/moin/TkInter)
