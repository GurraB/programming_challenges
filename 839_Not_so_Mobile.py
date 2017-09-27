import sys
mobileInput = sys.stdin.read().split('\n')
currentLine = 2
balanced = True

def fulcrum():
    global currentLine
    global balanced
    data = mobileInput[currentLine].split(' ')
    currentLine += 1
    left = int(data[0])
    right = int(data[2])
    if int(data[0]) == 0:   #has nodes
        left = fulcrum()
    if int(data[2]) == 0:   #has nodes
        right = fulcrum()
    if (left * int(data[1])) != (right * int(data[3])):
        balanced = False
    return left + right

for i in range(int(mobileInput[0])):
    balanced = True
    fulcrum()
    if balanced:
        print("YES")
    else:
        print("NO")
    if i != (int(mobileInput[0]) - 1):
        print("")
    currentLine += 1