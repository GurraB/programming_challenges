def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print ('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

import sys
import time

debugInput = "10 14\n1 2 2 1 1 1 1 1 1 1 1 1 1 2\n1 1 2 2 1 1 1 1 1 1 1 1 1 1\n1 1 1 2 2 1 1 1 1 1 1 1 1 1\n1 1 1 1 2 2 1 1 1 1 1 1 1 1\n1 1 1 1 1 2 2 1 1 1 1 1 1 1\n1 1 1 1 1 1 2 2 1 1 1 1 1 1\n1 1 1 1 1 1 1 2 2 1 1 1 1 1\n1 1 1 1 1 1 1 1 2 2 1 1 1 1\n1 1 1 1 1 1 1 1 1 2 2 1 1 1\n1 1 1 1 1 1 1 1 1 1 2 2 1 1"

tspInput = sys.stdin.read().split('\n')
#tspInput = debugInput.split('\n')
currentline = 0

def traverseUp(y, x, matrix):
    if y == 0:
        return (len(matrix) - 1, x + 1)
    return (y - 1, x + 1)

def traverseDown(y, x, matrix):
    if y == (len(matrix) - 1):
        return (0, x + 1)
    return (y + 1, x + 1)

def traverseRight(y, x, matrix):
    return (y, x + 1)

#@timing
def rec(pos, matrix, savedValues, savedPaths):
    [y, x] = pos
    if x >= len(matrix[0]):
        return 0
    if not (savedValues[y][x]) == 99999:
        return savedValues[y][x]

    upPos = traverseUp(y, x, matrix)
    rightPos = traverseRight(y, x, matrix)
    downPos = traverseDown(y, x, matrix)

    upRes = rec(upPos, matrix, savedValues, savedPaths)
    rightRes = rec(rightPos, matrix, savedValues, savedPaths)
    downRes = rec(downPos, matrix, savedValues, savedPaths)

    returnVal = min([(upRes, upPos), (rightRes, rightPos), (downRes, downPos)], key=lambda item: (item[0], item[1][0]))
    savedValues[y][x] = returnVal[0] + matrix[y][x]
    savedPath = list()
    savedPath.extend(savedPaths[returnVal[1][0]][returnVal[1][1]])
    savedPath.append(y + 1)
    savedPaths[y][x] = savedPath

    return returnVal[0] + matrix[y][x]

#@timing
def runprogram():
    global currentline
    while currentline < len(tspInput):
        matrixSize = tspInput[currentline].split(' ')
        y = int(matrixSize[0])
        x = int(matrixSize[1])
        currentline += 1
        matrix = [[0 for i in range(x)] for j in range(y)]
        savedValues = [[99999 for i in range(x + 1)] for j in range(y)]
        savedPaths = [[list() for i in range(x + 1)] for j in range(y)]
        for i in range(y):
            row = tspInput[currentline].split(' ')
            for j in range(x):
                matrix[i][j] = int(row[j])
            currentline += 1
        for i in range(y):
            rec((i, 0), matrix, savedValues, savedPaths)

        smallestStartPositions = list()
        smallest = 9999999
        for i in range(y):
            if savedValues[i][0] < smallest:
                smallestStartPositions = list()
                smallestStartPositions.append(i)
                smallest = savedValues[i][0]
            elif savedValues[i][0] == smallest:
                smallestStartPositions.append(i)

        smallestPath = 999999
        selectedStart = -1
        for i in range(len(smallestStartPositions)):
            pathsum = sum(savedPaths[i][0])
            if pathsum < smallestPath:
                smallestPath = pathsum
                selectedStart = i

        for p in savedPaths[selectedStart][0][::-1]:
            print(p, end=' ')
        print('\n' + str(savedValues[i][0]))

runprogram()