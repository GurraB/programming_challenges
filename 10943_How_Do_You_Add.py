import sys
addInput = sys.stdin.read().split('\n')
currentline = 0

def printArr(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(arr[i][j], end="\t")
        print()

def rec(a, b, savedValues):
    if a == 0:
        savedValues[a][b] = 1
        return 1
    #print(str(a) + ' ' + str(b))
    if not savedValues[a][b] == 0:
        return savedValues[a][b]
    if b <= 2:
        savedValues[a][b] = a + 1
        return a + 1
    count = 0
    temp = a
    while a >= 0:
        count += rec(a, b - 1, savedValues)
        a -= 1
    savedValues[temp][b] = count
    return count

while not addInput[currentline] == "0 0":
    digits = addInput[currentline].split(' ')
    currentline += 1
    numberToCountTo = int(digits[0])
    numberOfDigitsToUse = int(digits[1])

    savedValues = [[0 * i for i in range(numberOfDigitsToUse + 1)] for j in range(numberToCountTo + 1)]
    count = rec(numberToCountTo, numberOfDigitsToUse, savedValues)
    count = count % 1000000
    #print()
    printArr(savedValues)
    print(count)