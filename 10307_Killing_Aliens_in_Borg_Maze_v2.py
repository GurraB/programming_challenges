import operator
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
    dist = 9999
    mstWeight = 9999

    def __init__(self, name):
        self.name = name
        self.edges = list()

    def addEdge(self, edge):
        self.edges.append(edge)
        self.edges = list(set(self.edges))

    def getEdges(self):
        return self.edges

    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return False

    def __gt__(self, other):
        return self.dist > other.dist

    def __lt__(self, other):
        return self.dist < other.dist


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

    def findVertex(self, key):
        if key in self.vertices.keys():
            return self.vertices[key]
        return None


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
    node1 = uf.nodeMap[data1]
    node2 = uf.nodeMap[data2]
    parent1 = findset(node1)
    parent2 = findset(node2)

    if (parent1.rank >= parent2.rank):
        if (parent1.rank == parent2.rank):
            parent1.rank += 1
            parent2.parent = parent1

        parent2.parent = parent1
    else:
        parent1.parent = parent2


def findset(node):
    node_parent = node.parent
    if (node == node_parent):
        return node_parent
    node_parent = findset(node_parent.parent)
    node.parent = node_parent  # bushy tree ^^
    return node_parent


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


def findA(maze):
    aliens = list()
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if 'A' in maze[y][x] or 'S' in maze[y][x]:
                aliens.append((y, x))
    return aliens


def findS(maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 'S':
                return str(y) + ', ' + str(x)


def sort_edges(edges):
    return sorted(edges, key=operator.attrgetter('weight'))


def cuttin(sorted_edges, uf, sizeofnodes):
    mst = list()
    i = 0
    sizeofMst = 0
    while sizeofMst < (sizeofnodes - 1):
        e = sorted_edges[i]
        i += 1
        if not findset(uf.nodeMap[e.v1.name]) == findset(uf.nodeMap[e.v2.name]):
            union(e.v1.name, e.v2.name, uf)
            mst.append(e)
            sizeofMst += 1
    return mst


def createMST(g, sizeofnodes):
    uf = UnionFind()
    edges = g.getEdges()
    sorted_edges = sort_edges(edges)
    for v in g.getVertices():
        makeSet(v, 0, uf)
    mst = cuttin(sorted_edges, uf, sizeofnodes)
    return mst


def primMst(g, source):
    INF = 9999
    cost = {x: INF for x in g.getVertices()}
    cost[source] = 0
    PQ = []
    heapq.heappush(PQ, (cost[source], source))
    while (PQ):
        u = heapq.heappop(PQ)  # u is a tuple [u_dist, u_id]
        u_id = u[1]
        #print(u_id)
        if not g.findVertex(u_id) is None:
            for e in g.findVertex(u_id).getEdges():
                v_id = e.v2.name
                w = e.weight
                if w + cost[u_id] <= cost[v_id]:
                    cost[v_id] = w
                    heapq.heappush(PQ, (cost[v_id], v_id))
    return cost

# @timing
def createCompleteGraph(maze):
    g = Graph()
    for n in range(len(maze)):
        for m in range(len(maze[n])):
            if not maze[n][m] == '#':
                g.addVertex((str(n) + ', ' + str(m)))
    for n in range(len(maze)):
        for m in range(len(maze[n])):
            thisedge = g.findVertex((str(n) + ', ' + str(m)))
            if not thisedge == None:
                eastneighbor = g.findVertex((str(n) + ', ' + str(m - 1)))
                westneighbor = g.findVertex((str(n) + ', ' + str(m + 1)))
                southneighbor = g.findVertex((str(n + 1) + ', ' + str(m)))
                northneighbor = g.findVertex((str(n - 1) + ', ' + str(m)))
                if not eastneighbor == None:
                    g.addEdge((thisedge.name, eastneighbor.name, 1))
                if not westneighbor == None:
                    g.addEdge((thisedge.name, westneighbor.name, 1))
                if not southneighbor == None:
                    g.addEdge((thisedge.name, southneighbor.name, 1))
                if not northneighbor == None:
                    g.addEdge((thisedge.name, northneighbor.name, 1))
    return g


def dijkstra(g, source):
    INF = 9999
    dist = {x: INF for x in g.getVertices()}
    dist[source] = 0
    PQ = []
    heapq.heappush(PQ, [dist[source], source])
    while (PQ):
        u = heapq.heappop(PQ)  # u is a tuple [u_dist, u_id]
        u_dist = u[0]
        u_id = u[1]
        if u_dist == dist[u_id]:
            for e in g.findVertex(u_id).getEdges():
                v_id = e.v2.name
                w = e.weight
                if dist[v_id] == 9999:
                    dist[v_id] = dist[u_id] + w
                    heapq.heappush(PQ, [dist[v_id], v_id])
    return dist


def runDijkstraOnGraph(nodes, g, newGraph):
    while len(nodes) > 1:
        temp = nodes[0]
        nodes = nodes[1:]
        distances = dijkstra(g, str(temp[0]) + ', ' + str(temp[1]))
        for m in nodes:
            distanceToM = distances[str(m[0]) + ', ' + str(m[1])]
            newGraph.addEdge(((str(temp[0]) + ', ' + str(temp[1])), (str(m[0]) + ', ' + str(m[1])), distanceToM))
            newGraph.addEdge(((str(m[0]) + ', ' + str(m[1])), (str(temp[0]) + ', ' + str(temp[1])), distanceToM))
    return newGraph


def finddistances(g, maze):
    newGraph = Graph()
    nodes = findA(maze)

    for n in nodes:
        newGraph.addVertex((str(n[0]) + ', ' + str(n[1])))

    newGraph = runDijkstraOnGraph(nodes, g, newGraph)

    mst = createMST(newGraph, len(nodes))
    sumweight = 0
    for e in mst:
       sumweight += e.weight

    #mst = primMst(newGraph, findS(maze))
    #sumweight = 0
    #for key in mst.keys():
    #    print(str(key) + ": " + str(mst[key]))
    #    sumweight += mst[key]
    print(sumweight)


@timing
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
        g = createCompleteGraph(maze)
        finddistances(g, maze)


runprogram(testcases, currentline, mazeinput)
