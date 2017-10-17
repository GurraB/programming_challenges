import sys
import math

mountainInput = sys.stdin.read().split('\n')
currentline = 0

testcases = int(mountainInput[currentline])
currentline += 1

def lenOfVector(p1, p2, coveredY):
    xlen = p1[0] - p2[0]
    ylen = p1[1] - p2[1]
    visiblePart = p2[1] - coveredY
    if visiblePart < 0:
        return 0
    factor = visiblePart / ylen
    vectorlen = math.sqrt(math.pow(xlen, 2) + math.pow(ylen, 2))
    return vectorlen * -factor

for i in range(testcases):
    coordinatePairs = int(mountainInput[currentline])
    currentline += 1
    coordinates = []
    for cor in range(coordinatePairs):
        [x, y] = map(int, mountainInput[currentline].split())
        coordinates.append((x, y))
        currentline += 1
    sorted_coordinates = sorted(coordinates, key=lambda item: item[0])
    sorted_coordinates = sorted_coordinates[::-1]

    coveredY = 0
    sunny = 0
    for j in range(0, len(sorted_coordinates), 1):
        if j + 1 >= len(sorted_coordinates):
            break
        p1 = sorted_coordinates[j]
        p2 = sorted_coordinates[j + 1]
        if p2[1] < p1[1]:
            continue
        sunny += lenOfVector(p1, p2, coveredY)
        coveredY = p2[1]
    if i == testcases - 1:
        print("%.2f" % sunny, end='')
    else:
        print("%.2f" % sunny)