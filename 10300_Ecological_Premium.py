import sys

farmerInput = sys.stdin.read().split('\n')
testCases = int(farmerInput[0])
currentLine = 1
for i in range(testCases):
    f = int(farmerInput[currentLine])
    currentLine += 1
    farmerScoreSum = 0
    for j in range(f):
        tempFarmer = farmerInput[currentLine].split(' ')
        farmerScoreSum += int(tempFarmer[0]) * int(tempFarmer[2])
        currentLine += 1
    print(farmerScoreSum)