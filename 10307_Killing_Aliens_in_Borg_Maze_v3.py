import sys
import time
import heapq


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2 - time1) * 1000.0))
        return ret

    return wrap
class UfNode:
    def __init__(self, data, rank):
        self.data = data
        self.parent = 0
        self.rank = rank

    def getNodeMap(self):
        return self.nodeMap


class UnionFind:
    nodeMap = {}

    def __init__(self):
        self.nodeMap = {}


def makeSet(data, rank, uf):
    node = UfNode(data, rank)
    node.parent = node
    uf.nodeMap[data] = node


def union(data1, data2, uf):
    parent1 = findset(uf.nodeMap[data1], uf)
    parent2 = findset(uf.nodeMap[data2], uf)

    if (parent1.rank >= parent2.rank):
        if (parent1.rank == parent2.rank):
            parent1.rank += 1
            parent2.parent = parent1

        parent2.parent = parent1
    else:
        parent1.parent = parent2


def findset(node, uf):
    node_parent = node.parent
    if (node == node_parent):
        return node_parent
    node_parent = findset(node_parent.parent, uf)
    node.parent = node_parent  # bushy tree ^^
    return node_parent


mazeinput = sys.stdin.read().split('\n')
currentline = 0
testcases = int(mazeinput[currentline])
currentline += 1

directions = {'LEFT': (0, -1), 'RIGHT': (0, 1), 'UP':(-1, 0), 'DOWN':(1, 0)}

def findA(maze):
    aliens = list()
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if 'A' in maze[y][x] or 'S' in maze[y][x]:
                aliens.append((y, x))
    return aliens


def createMST(truples, nodes):
    uf = UnionFind()
    sorted_truples = sorted(truples, key=lambda item: item[1])
    for node in nodes:
        makeSet(node, 0, uf)
    mst = list()
    i = 0
    while len(mst) < (len(nodes) - 1):
        truple = sorted_truples[i]
        i += 1
        if not findset(uf.nodeMap[truple[0]], uf) == findset(uf.nodeMap[truple[2]], uf):
            union(truple[0], truple[2], uf)
            mst.append(truple)
    return mst


#@timing
def createCompleteGraph(maze):
    booleanMaze = list()
    for n in range(len(maze)):
        booleanRow = list()
        for m in range(len(maze[n])):
            if maze[n][m] == '#':
                booleanRow.append(True)
            else:
                booleanRow.append(False)
        booleanMaze.append(booleanRow)
    return booleanMaze

def dijkstra(booleanMaze, source):
    booleanMazeCpy = [row[:] for row in booleanMaze]
    dist = {}
    dist[source] = 0
    PQ = []
    heapq.heappush(PQ, [dist[source], source])
    while (PQ):
        u = heapq.heappop(PQ)  # u is a tuple [u_dist, u_id]
        u_dist = u[0]
        u_id = u[1]
        #if u_dist == dist[u_id]:
        for dir in directions.values():
            newpos = (u_id[0] + dir[0], u_id[1] + dir[1])
            if not booleanMazeCpy[newpos[0]][newpos[1]]:
                dist[newpos] = u_dist + 1
                booleanMazeCpy[newpos[0]][newpos[1]] = True
                heapq.heappush(PQ, [dist[newpos], newpos])
    return dist


def runDijkstraOnGraph(nodes, booleanMaze):
    truples = list()
    while len(nodes) > 1:
        temp = nodes[0]
        nodes = nodes[1:]
        distances = dijkstra(booleanMaze, temp)
        for m in nodes:
            distanceToM = distances[m]
            truple = (temp, distanceToM, m)
            truples.append(truple)
    return truples


def finddistances(booleanMaze, maze):
    nodes = findA(maze)

    truples = runDijkstraOnGraph(nodes, booleanMaze)

    mst = createMST(truples, nodes)
    sumweight = 0
    for truple in mst:
       sumweight += truple[1]
    print(sumweight)


#@timing
def runprogram(testcases, currentline, mazeinput):
    for i in range(testcases):
        maze = list()
        [xlen, ylen] = mazeinput[currentline].split(' ')
        ylen = int(ylen)
        currentline += 1
        for y in range(int(ylen)):
            row = list(mazeinput[currentline])
            maze.append(row)
            currentline += 1
        booleanMaze = createCompleteGraph(maze)
        finddistances(booleanMaze, maze)


runprogram(testcases, currentline, mazeinput)
