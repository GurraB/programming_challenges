import sys

artInput = sys.stdin.read().split('\n')
currentline = 0

class Line:

    p1 = (0, 0)
    p2 = (0, 0)

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def tt(p1, p2, p3):
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    return (v1[0] * v2[1]) - (v1[1] * v2[0])

def intersects(p1, p2, p3, p4):
    return ((tt(p1, p2, p3) * tt(p1, p2, p4) < 0) and (tt(p3, p4, p1) * tt(p3, p4, p2) < 0))

while True:
    corners = int(artInput[currentline])
    currentline += 1
    if corners == 0:
        break

    points = []
    for i in range(corners):
        [x, y] = map(int, artInput[currentline].split())
        currentline += 1
        points.append((x, y))

    lines = []

    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        lines.append(Line(p1, p2))

    isValidPoly = True
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                continue
            l1 = lines[i]
            l2 = lines[j]
            if intersects(l1.p1, l1.p2, l2.p1, l2.p2):
                isValidPoly = False
                break
    hasCritical = False

    firstTurn = True
    turnPositive = False
    turnNone = False

    if isValidPoly:
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            p3 = points[(i + 2) % len(points)]
            if tt(p1, p2, p3) == 0:
                turnNone = True
            elif tt(p1, p2, p3) < 0:
                if turnPositive and not firstTurn:
                    hasCritical = True
                    break
                firstTurn = False
                turnPositive = False
                turnNone = False
            elif tt(p1, p2, p3) > 0:
                if not turnPositive and not firstTurn:
                    hasCritical = True
                    break
                firstTurn = False
                turnPositive = True
                turnNone = False
        print("Yes" if hasCritical else "No")
    else:
        print("No")
