import sys
wineinput = sys.stdin.read().split('\n')
currentline = 0
citizens = 0
while wineinput[currentline] != 0:
    citizens = wineinput[currentline]
    currentline += 1

    market = list(map(int, wineinput[currentline].split(' ')))
    rootnode = len(market) / 2

def tree(node):
    demand = market[node]
    branchingdemand = tree(node + 1)