import sys

bobbyInput = sys.stdin.read().split('\n')
currentLine = 0
setCount = 0
while not int(bobbyInput[currentLine]) == 0:
    currentLine += 1
    setCount += 1
    stacks = list(map(int, bobbyInput[currentLine].split(' ')))
    currentLine += 1
    wantedHeight = sum(stacks, 0) / len(stacks)
    moves = 0
    for stack in stacks:
        moves += abs(stack - wantedHeight)
    print("Set #" + str(setCount))
    print("The minimum number of moves is " + str(int(moves/2)) + ".\n")