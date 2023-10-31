import time
import os
import counter


class net(object):

    def __init__(self, file='', directivity=0, logger=1, time_counter=0):
        # directivity=0 representing directed-map, =1 representing undirected-map
        # logger=0 representing log mode off, =1 representing log mode on
        # time_counter=0 representing running time counter off, =1 representing counter on

        DIR_NAME = os.path.dirname(__file__)
        self.map_info = open(file, mode='r')
        self.m, self.n = map(int, self.map_info.readline().split())
        self.directivity = directivity
        self.edges = {}
        self.dist = {}
        self.nodes = set()
        self.logger = logger
        self.time_counter = time_counter
        self.avg_time = 0
        self.avg_count = 0
        LOG_LIMITS = 5
        # log files limit

        tmp = open(DIR_NAME + '/net_logfiles/IGNORED_FILES.txt', mode='r')
        IGNORED_FILES = tmp.read().split()

        FILES = os.listdir(DIR_NAME + '/net_logfiles')
        for ig in IGNORED_FILES:
            if ig in FILES:
                FILES.remove(ig)
        # keep files that should be presistently saved, stored in '/net_logfiles/IGNORED_FILES'

        for i in range(len(FILES) - LOG_LIMITS + self.logger):
            os.remove(DIR_NAME + '/net_logfiles/' + min(FILES))
            FILES.remove(min(FILES))
        # remove excessive files

        if self.logger:
            self.log_file = open(time.strftime(
                DIR_NAME + "/net_logfiles/%Y%m%d-%H-%M-%S.log",
                time.localtime()),
                                 mode='w+')

    def __del__(self):
        self.map_info.close()

        if self.logger:
            self.log_file.close()

        if self.time_counter:
            print('Average running time:',
                  round(self.avg_time / self.avg_count * 1000, 3), 'ms')

    def readNet(self):
        for i in range(self.n):
            start, end, distance = self.map_info.readline().split()
            self.nodes |= set([start, end])
            distance = int(distance)
            for j in range(self.directivity + 1):
                if start not in self.edges: self.edges[start] = []
                self.edges[start].append([end, distance])
                start, end = end, start

    def quest(self, start, end, method):
        # [method] throw out an opportunity to modify shortest path algorithm

        if start not in self.nodes or end not in self.nodes:
            return "ERROR: invalid input, please check nodes\' name"

        count = counter.counter()
        if start not in self.dist:
            count.refresh()
            method(start, self)
            if self.time_counter:
                self.avg_time += count.print()
                self.avg_count += 1
        path = self.dist[start]
        # generate shortest path with [start] as start node

        distance = self.dist[start][end][0]
        pathOut = ''
        cur = end
        while cur != start:
            pathOut = ' -> ' + cur + pathOut
            cur = path[cur][1]
        pathOut = start + pathOut

        if self.logger:
            self.log_file.write(start + ' ' + end + '\n')
            self.log_file.write("The shortest path is: " + pathOut + '\n')
            self.log_file.write("The distance is: " + str(distance) + '\n')

        return "The shortest path is: " + pathOut + '\n' + "The distance is: " + str(
            distance)


def Dijkstra(start, net):
    # Djikstra to get the shortest path

    queue = [start]
    path = {start: [0, ""]}
    while len(queue):
        cur = min(queue, key=lambda val: path[val][0])
        for tar, dis in net.edges[cur]:
            if tar not in path:
                path[tar] = [int(1E9), ""]
            if path[tar][0] > path[cur][0] + dis:
                path[tar] = [path[cur][0] + dis, cur]
                queue.append(tar)
        queue.remove(cur)
    net.dist[start] = path
    return


def SPFA(start, net):
    # SPFA to get the shortest path

    queue = [start]
    path = {start: [0, ""]}
    while len(queue):
        cur = queue[0]
        for tar, dis in net.edges[cur]:
            if tar not in path:
                path[tar] = [int(1E9), ""]
            if path[tar][0] > path[cur][0] + dis:
                path[tar] = [path[cur][0] + dis, cur]
                if tar not in queue:
                    queue.append(tar)
        queue.pop(0)

    net.dist[start] = path
    return
