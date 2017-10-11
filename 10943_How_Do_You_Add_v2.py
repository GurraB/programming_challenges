import sys
addInput = sys.stdin.read().split('\n')
currentline = 0

def printArr(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(arr[i][j], end="\t")
        print()

while not addInput[currentline] == "0 0":
    digits = addInput[currentline].split(' ')
    currentline += 1
    numberToCountTo = int(digits[0])
    numberOfDigitsToUse = int(digits[1])

    savedValues = [[i for i in range(numberOfDigitsToUse + 1)] for j in range(numberToCountTo)]
    for i in range(1, len(savedValues), 1):
        for j in range(1, len(savedValues[i]), 1):
            savedValues[i][j] = savedValues[i - 1][j] + savedValues[i][j - 1]
    #printArr(savedValues)
    val = savedValues[numberToCountTo - 1][numberOfDigitsToUse] % 1000000
    print(val)