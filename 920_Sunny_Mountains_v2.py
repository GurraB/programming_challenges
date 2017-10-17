import sys
import math

mountainInput = sys.stdin.read().split('\n')
currentline = 0

testcases = int(mountainInput[currentline])
currentline += 1

class Line:
    k = 0
    m = 0

    def __init__(self, k, m):
        self.k = k
        self.m = m

    def getX(self, y):
        return ((y - self.m) / self.k)

    def getY(self, x):
        return (self.k * x + self.m)

def generateLineFromPoints(p1, p2):
    k = -(p2[1] - p1[1]) / (p2[0] - p1[0])
    m = p1[1] - (k * p1[0])
    return Line(k, m)

def getLenBetweenPoints(p1, p2):
    ylen = p2[1] - p1[1]
    xlen = p2[0] - p1[0]
    totlen = math.sqrt(math.pow(ylen, 2) + math.pow(xlen, 2))
    return totlen

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

    for j in range(len(sorted_coordinates) - 1):
        p1 = sorted_coordinates[j]
        p2 = sorted_coordinates[j + 1]
        if p2[1] <= coveredY:
            continue
        line = generateLineFromPoints(p1, p2)
        if line.k > 0:
            newp1 = (line.getX(coveredY), coveredY)
            sunny += getLenBetweenPoints(newp1, p2)
            coveredY = p2[1]
        else:
            print()

    if i == testcases - 1:
        print("%.2f" % sunny, end='\n')
    else:
        print("%.2f" % sunny)
