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