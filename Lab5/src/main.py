from lib import *
from SA import *
from GA import *
import time

if __name__ == '__main__':
    data = open(DIR + '/../data/a280.tsp', mode='r')
    line = data.readline().split()
    coords = []
    while line != ['EOF']:
        num, x, y = map(float, line)
        coords.append((x, y))
        line = data.readline().split()

    finalSol, finalDis, usedTime = SA(coords)
    print('Time:          ', usedTime, 's')
    print('Total distance:', finalDis)
    drawPath(coords, finalSol, 'Final Solution with ' + str(finalDis))
