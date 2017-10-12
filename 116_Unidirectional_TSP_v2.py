import sys

tspInput = sys.stdin.read().split('\n')
currentline = 0
maxX = 0
maxY = 0

def traverseUp(y, x):
    if y == 0:
        return (maxY - 1, x + 1)
    return (y - 1, x + 1)

def traverseDown(y, x):
    if y == (maxY - 1):
        return (0, x + 1)
    return (y + 1, x + 1)

def rec(pos, matrix, savedValues, savedPaths):
    [y, x] = pos
    if x >= maxX:
        return 0
    if not (savedValues[y][x]) == 99999:
        return savedValues[y][x]

    upPos = traverseUp(y, x)
    rightPos = (y, x + 1)
    downPos = traverseDown(y, x)

    upRes = rec(upPos, matrix, savedValues, savedPaths)
    rightRes = rec(rightPos, matrix, savedValues, savedPaths)
    downRes = rec(downPos, matrix, savedValues, savedPaths)

    returnVal = min([(upRes, upPos), (rightRes, rightPos), (downRes, downPos)], key=lambda item: (item[0], item[1][0]))
    savedValues[y][x] = returnVal[0] + matrix[y][x]
    savedPath = list()
    savedPath.extend(savedPaths[returnVal[1][0]][returnVal[1][1]])
    savedPath.append(y + 1)
    savedPaths[y][x] = savedPath

    return savedValues[y][x]

def runprogram():
    global currentline, maxX, maxY
    while currentline < len(tspInput) - 1:
        matrixSize = tspInput[currentline].split(' ')
        y = int(matrixSize[0])
        x = int(matrixSize[1])
        maxY = y
        maxX = x
        currentline += 1
        matrix = [[0 for i in range(x)] for j in range(y)]
        savedValues = [[99999 for i in range(x + 1)] for j in range(y)]
        savedPaths = [[list() for i in range(x + 1)] for j in range(y)]
        totalInput = list()
        while len(totalInput) < (x * y):
            row = tspInput[currentline].split(' ')
            print(len(row))
            for c in row:
                try:
                    totalInput.append(int(c))
                except:
                    continue
            currentline += 1
        for i in range(len(totalInput)):
            matrix[int(i/x)][i%x] = totalInput[i]

        #for r in matrix:
        #    print(len(r))

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

        for smallest in smallestStartPositions:
            savedPaths[smallest][0] = savedPaths[smallest][0][::-1]

        selectedStart = -1
        shouldbreak = False
        for j in range(x):
            currentsmallest = 11
            if shouldbreak:
                break
            for i in smallestStartPositions:
                if savedPaths[i][0][j] == currentsmallest:
                    shouldbreak = False
                    continue
                if savedPaths[i][0][j] < currentsmallest:
                    currentsmallest = savedPaths[i][0][j]
                    selectedStart = i
                    shouldbreak = True

        for i in range(len(savedPaths[selectedStart][0])):
            if not i == len(savedPaths[selectedStart][0]) - 1:
                print(savedPaths[selectedStart][0][i], end=' ')
            else:
                print(savedPaths[selectedStart][0][i], end='\n')
        print(savedValues[selectedStart][0])

runprogram()