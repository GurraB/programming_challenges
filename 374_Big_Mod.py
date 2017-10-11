import sys
modInput = sys.stdin.read().split('\n')
currentLine = 0

def successive_squaring(b, p, m):
    if p == 0: return 1
    z = successive_squaring(b, int(p/2), m)
    if p & 0b1 == 0:
        return (z*z) % m
    else:
        return (b * (z*z)) % m

while( currentLine < len(modInput)):
    b = int(modInput[currentLine])
    currentLine += 1
    p = int(modInput[currentLine])
    currentLine += 1
    m = int(modInput[currentLine])
    currentLine += 2

    modular = successive_squaring(b, p, m)
    print(modular)