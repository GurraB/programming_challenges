import operator

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print ('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

class Edge:
    weight = 9999
    v1 = None
    v2 = None

    def __init__(self, v1, v2, weight):
        self.weight = weight
        self.v1 = v1
        self.v2 = v2

    def getPrettyText(self):
        text = ""
        text += self.v1.name
        text += " <-- "
        text += str(self.weight)
        text += " --> "
        text += self.v2.name
        return text

class Vertex:
    name = ""
    edges = list()

    def __init__(self, name):
        self.name = name
        self.edges = list()

    def addEdge(self, edge):
        self.edges.append(edge)

    def getEdges(self):
        return self.edges

class Graph:
    vertices = {}

    def __init__(self):
        self.vertices = {}

    def addVertex(self, vName):
        self.vertices[vName] = Vertex(vName)

    def addEdge(self, edge):
        e = Edge(self.vertices[edge[0]], self.vertices[edge[1]], int(edge[2]))
        self.vertices[e.v1.name].edges.append(e)
        self.vertices[e.v2.name].edges.append(e)

    def addEdgeObj(self, edge):
        self.vertices[edge.v1.name].edges.append(edge)
        self.vertices[edge.v2.name].edges.append(edge)

    def getVertices(self):
        return self.vertices.keys()

    def getEdges(self):
        edges = list()
        for v in self.vertices.keys():
            edges.extend(self.vertices[v].getEdges())
        return edges

class Node:
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
    node = Node(data, rank)
    node.parent = node
    uf.nodeMap[data] = node

def union(data1, data2, uf):
    node1 = uf.nodeMap[data1]
    node2 = uf.nodeMap[data2]
    parent1 = findset(node1)
    parent2 = findset(node2)

    if(parent1.data == parent2.data):
        return

    if(parent1.rank >= parent2.rank):
        if(parent1.rank == parent2.rank):
            parent1.rank += 1
            parent2.parent = parent1

        parent2.parent = parent1
    else:
        parent1.parent = parent2

def findset(node):
    node_parent = node.parent
    if(node == node_parent):
        return node_parent
    node_parent = findset(node_parent.parent)
    node.parent = node_parent   #bushy tree ^^
    return node_parent


import sys
import time
from collections import deque
import _thread as thread
mazeinput = sys.stdin.read().split('\n')
currentline = 0
testcases = int(mazeinput[currentline])
currentline += 1

def formatVertex(name1, weight, name2):
    if name1 == 'S':
        return (name1, weight, name2)
    if name2 == 'S':
        return (name2, weight, name1)

    if int(name1[1:]) > int(name2[1:]):
        return (name1, weight, name2)
    else:
        return (name2, weight, name1)

def findS(maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 'S':
                return (y, x)

def findA(maze):
    aliens = list()
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if 'A' in maze[y][x]:
                aliens.append((y, x))
    return aliens

def inbounds(pos, lenX, lenY):
    return True if pos[0] > 0 and pos[0] < lenY and pos[1] > 0 and pos[1] < lenX else False

def createVerticesFromNode(maze, xlen, ylen, node):
    mazeweights = list()
    q = deque()
    for y in range(ylen):
        rowweights = [9999] * xlen
        mazeweights.append(rowweights)
    mazeweights[node[0]][node[1]] = 0
    operations = 0
    q.append(node)
    while len(q) > 0:
        operations += 1
        u = q.pop()
        #EAST
        if inbounds((u[0] + 1, u[1]), xlen, ylen):
            if mazeweights[u[0]][u[1]] + 1 < mazeweights[u[0] + 1][u[1]] and not maze[u[0] + 1][u[1]] == '#':
                mazeweights[u[0] + 1][u[1]] = mazeweights[u[0]][u[1]] + 1
                q.append((u[0] + 1, u[1]))
        #WEST
        if inbounds((u[0] - 1, u[1]), xlen, ylen):
            if mazeweights[u[0]][u[1]] + 1 < mazeweights[u[0] - 1][u[1]] and not maze[u[0] - 1][u[1]] == '#':
                mazeweights[u[0] - 1][u[1]] = mazeweights[u[0]][u[1]] + 1
                q.append((u[0] - 1, u[1]))
        #NORTH
        if inbounds((u[0], u[1] - 1), xlen, ylen):
            if mazeweights[u[0]][u[1]] + 1 < mazeweights[u[0]][u[1] - 1] and not maze[u[0]][u[1] - 1] == '#':
                mazeweights[u[0]][u[1] - 1] = mazeweights[u[0]][u[1]] + 1
                q.append((u[0], u[1] - 1))
        #SOUTH
        if inbounds((u[0], u[1] + 1), xlen, ylen):
            if mazeweights[u[0]][u[1]] + 1 < mazeweights[u[0]][u[1] + 1] and not maze[u[0]][u[1] + 1] == '#':
                mazeweights[u[0]][u[1] + 1] = mazeweights[u[0]][u[1]] + 1
                q.append((u[0], u[1] + 1))
    print(operations)
    vertices = list()
    nodes = list()
    nodes.append(findS(maze))
    nodes.extend(findA(maze))
    for n in nodes:
        if not mazeweights[n[0]][n[1]] == 0:
            vertices.append((n, mazeweights[n[0]][n[1]]))

    return vertices

@timing
def createMST(g):
    uf = UnionFind()
    edges = g.getEdges()
    mst = list()
    sorted_edges = sorted(edges, key=operator.attrgetter('weight'))
    for v in g.getVertices():
        makeSet(v, 0, uf)
    for e in sorted_edges:
        if not findset(uf.nodeMap[e.v1.name]) == findset(uf.nodeMap[e.v2.name]):
            union(e.v1.name, e.v2.name, uf)
            mst.append(e)
    return mst

@timing
def createGraph(maze):
    s = findS(maze)
    g = Graph()
    g.addVertex('S')
    allVertices = list()
    for v in createVerticesFromNode(maze, xlen, ylen, s):
        allVertices.append(formatVertex(maze[s[0]][s[1]], v[1], maze[v[0][0]][v[0][1]]))
    for alien in findA(maze):
        g.addVertex(maze[alien[0]][alien[1]])
        for v in createVerticesFromNode(maze, xlen, ylen, alien):
            #thread.start_new_thread(createVerticesFromNode(maze, xlen, ylen, alien))
            allVertices.append(formatVertex(maze[alien[0]][alien[1]], v[1], maze[v[0][0]][v[0][1]]))
    #thread.join()
    allVertices = list(set(allVertices))
    sorted_vertices = sorted(allVertices, key=lambda tup: tup[1])
    for v in sorted_vertices:
        g.addEdge((v[0], v[2], v[1]))
    return g

for i in range(testcases):
    maze = list()
    [xlen, ylen] = mazeinput[currentline].split(' ')
    xlen = int(xlen)
    ylen = int(ylen)
    currentline += 1
    counter = 0
    for y in range(int(ylen)):
        row = list(mazeinput[currentline])
        for k in range(len(row)):
            if 'A' in row[k]:
                row[k] = 'A' + str(counter)
                counter += 1
        maze.append(row)
        currentline += 1
    if findS(maze) == None:
        print("0")
        continue
    g = createGraph(maze)
    mst = createMST(g)
    weightsum = 0
    for e in mst:
        weightsum += e.weight
    print(weightsum)