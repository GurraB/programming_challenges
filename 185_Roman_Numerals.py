import sys
import re

romanInput = sys.stdin.read().split('\n')
currentline = 0

romanDict = {
    'M': 1000,
    'D': 500,
    'C': 100,
    'L': 50,
    'X': 10,
    'V': 5,
    'I': 1
}

def translateRomanToDecimal(romanNumber):
    decimalNumber = 0
    while len(romanNumber) > 0:
        if len(romanNumber) > 1:
            if romanDict[romanNumber[1]] > romanDict[romanNumber[0]]:
                decimalNumber += romanDict[romanNumber[1]] - romanDict[romanNumber[0]]
                romanNumber = romanNumber[2::]
                continue
        decimalNumber += romanDict[romanNumber[0]]
        romanNumber = romanNumber[1::]
    return decimalNumber

def interpretation(line):
    print()

while not romanInput[currentline] == '#':
    line = re.split(r'[+=]', romanInput[currentline])
    currentline += 1
    isCorrect = True if translateRomanToDecimal(line[0]) + translateRomanToDecimal(line[1]) == translateRomanToDecimal(line[2]) else False
    print("Correct" if isCorrect else "Incorrect", end=' ')

