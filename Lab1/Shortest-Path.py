import os
import net

if __name__ == '__main__':
    DIR_NAME = os.path.dirname(__file__)
    Romania = net.net(DIR_NAME + '/Romania.txt',
                      directivity=1,
                      logger=1,
                      time_counter=1)
    Romania.readNet()

    print('Input \'stop\' to quit. ')
    while True:
        s = input()
        if s == 'stop':
            break

        if len(s.split()) != 2:
            print("ERROR: invalid input, requiring 2 arguments excepting",
                  len(s.split()))
            continue

        start, end = map(lambda val: val.capitalize(), s.split())
        for tar in Romania.nodes:
            if start == tar[0]: start = tar
            if end == tar[0]: end = tar

        # print(Romania.quest(start, end, method=net.Dijkstra))
        print(Romania.quest(start, end, method=net.SPFA))
