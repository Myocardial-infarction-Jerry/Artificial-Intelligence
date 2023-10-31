# 中山大学 本科生实验报告

实验课程：人工智能

实验名称：

专业名称：计算机科学与技术

学生姓名：刘森元

学生学号：21307289

实验地点：广州校区东校园 实验中心 D501

报告时间：



***本人使用的环境如下：***

***Apple Inc. MacBook Pro 2021***

***M1 Pro (Apple Silicon)***

***使用的文献、软件、包大部分以超连接形式给出了原址。***



## 一、实验题目

用归结算法求解逻辑推理问题（如 AIpine Club 问题）

## 二、实验内容

### 1. 算法原理

**命题逻辑归结算法**

1. 将 α 取否定，加入到 KB 当中
2. 将更新的 KB 转换为 clausal form 得到 S
3. 反复调用单步归结
   1. 如果得到空子句，即 S|-()，说明 KB∧¬α 不可满足，算法终止，可得到 KB|=α
   2. 如果一直归结知道不产生新的子句，在这个过程中没有得到空子句，则 KB|=α 不成立

**最一般和一算法**

1. $k=0;\sigma_0=\{\};S_0=\{f,g\}$

2. 若 $S_k$ 中公式等价，返回 $\sigma_k$ 作为最一般和一的结果，否则找出 $S_k$ 中的不匹配项 $D_k=\{e_1,e_2\}$

3. 如果 $e_1=V$ 是变量，$e_2=t$ 是一个不包含变量 $V$ 的项，将 $V=t$ 添加到赋值集合 $\sigma_{k+1}=\sigma_k\cup\{V=t\}$，并将 $S_k$ 中的其他 $V$ 也赋值为 $t$，得到 $S_{k+1}$，$k=k+1$，转到第二步；

   否则合一失败

### 2. 伪代码

```
read subsentence set S
turn into clausal form
for i in S
	for j in S
		unifier -> rules
		i, j -> s
		S += s
		parents[s] = i, j
		
recall and output
```

### 3. 关键代码展示

*main.py*

```python
import re
import string


def neg(vec):  # 对项进行取反操作
    if vec[0][0] == '¬':
        return [vec[0][1:]] + vec[1:]
    else:
        return ['¬' + vec[0]] + vec[1:]


def unifier(veca, vecb):  # 最一般合一算法
    rules = []
    unia, unib = veca[1:], vecb[1:]
    tag = True
    while tag:
        tag = False  # 归结标识符
        for cur in range(len(unia)):
            for tema, temb in [[unia[cur], unib[cur]], [unib[cur], unia[cur]]]:
                if tema in string.ascii_lowercase[:] and tema not in temb and temb not in string.ascii_lowercase:  # 判断是否为一阶变量并不互相包含
                    rules.append((tema, temb))
                    unia = list(map(lambda x: re.sub(tema, temb, x), unia))
                    unib = list(map(lambda x: re.sub(tema, temb, x), unib))
                    tag = True

    if unia == unib:
        return rules  #归结成功，返回替换规则
    else:
        return ['fail']  # 归结失败


def resolute():  # 归结算法
    global S
    n = len(S)
    subi = -1
    while subi + 1 < len(S):  # 使用 while 以便利整个 S 集合
        subi += 1
        subj = -1
        while subj + 1 < len(S):
            subj += 1
            if subi == subj:
                continue
            suba, subb = S[subi][0], S[subj][0]
            for veci in range(len(suba)):
                for vecj in range(len(subb)):
                    veca, vecb = suba[veci], subb[vecj]
                    if neg(veca)[0] != vecb[0]:
                        continue
                    rules = unifier(veca, vecb)
                    if rules == ['fail']:
                        continue
                    # 生成新子句
                    sub = []
                    for vec in (suba + subb):
                        if vec == veca or vec == vecb:
                            continue
                        for rule in rules:
                            vec = list(
                                map(lambda x: re.sub(rule[0], rule[1], x),
                                    vec))
                        sub.append(vec)
                    sub = list(
                        map(lambda x: list(x), set(tuple(vec) for vec in sub)))
                    S.append([list(sub), (subi, veci, subj, vecj), rules])
                    if sub == []:
                        return
    return


def recall(s):  # 回溯并输出
    global counter, S  # 重标号计数器，子句集合
    [sub, parents, rules] = s
    if parents == (-1, -1, -1, -1):
        return S.index(s)
    posa, posb = recall(S[parents[0]]), recall(S[parents[2]])
    print('R[',
          posa + 1,
          string.ascii_lowercase[parents[1]],
          ', ',
          posb + 1,
          string.ascii_lowercase[parents[3]],
          ']',
          sep='',
          end='')
    if rules != []:
        print('(',
              ', '.join(map(lambda x: x[0] + ' = ' + x[1], rules)),
              ')',
              sep='',
              end='')
    print(' = ',
          '[ ',
          ', '.join(map(lambda x: x[0] + '(' + ', '.join(x[1:]) + ')', sub)),
          ' ]',
          sep='')
    counter += 1
    return counter


if __name__ == '__main__':
    n = int(input())

    # 转换为 Clausal Forming
    global S  # 子句集合
    S = []
    for i in range(n):
        str = input()
        S.append(
            list(
                map(lambda x: re.findall('¬?\w+', x),
                    re.findall('¬?\w+\(.*?\)', str))))
    S = list(map(lambda x: [x, (-1, -1, -1, -1), []], S))

    # Resolution
    resolute()

    # Relabeling & Output
    global counter  # 重标号计数器
    counter = n - 1
    recall(S[-1])
```

### 4. 创新点 & 优化

1. 在原算法的基础上，在最一般合一算法处进行了迭代操作，使得能够一次归结出多条替换规则，节省了时间
2. 使用正则表达式，利用 `re.finall` 将子句转化为 clausal form，精准而优雅
3. 多处使用 `map(lambda x: ..., )` 的形式，简化流程并压缩代码
4. 兼容 numpy 操作

## 三、实验结果及分析

### 1. 实验结果展示示例

![image-20230327222424975](/Users/qiu_nangong/Library/Application Support/typora-user-images/image-20230327222424975.png)

![image-20230327223134494](/Users/qiu_nangong/Library/Application Support/typora-user-images/image-20230327223134494.png)

![image-20230327223203829](/Users/qiu_nangong/Library/Application Support/typora-user-images/image-20230327223203829.png)

## 四、参考资料

[Python 菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html)

[numpy 菜鸟教程](https://www.runoob.com/numpy/numpy-tutorial.html)
