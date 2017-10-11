import sys
wineinput = sys.stdin.read().split('\n')
currentline = 0
citizens = 0

def split(housedemand):
    units = 0
    left = housedemand[:int(len(housedemands) / 2)]
    right = housedemand[int(len(housedemands) / 2):]

    for i in range(len(left) - 1):
        units += abs(left[i])
        left[i + 1] += left[i]

    for i in range(len(right) - 1):
        units += abs(right[len(right) - 1 - i])
        right[len(right) - 1 - i - 1] += right[len(right) - 1 - i]

    units += abs(right[0])
    print(units)


while int(wineinput[currentline]) != 0:
    citizens = wineinput[currentline]
    currentline += 1
    housedemands = list(map(int, wineinput[currentline].split(' ')))
    currentline += 1
    split(housedemands)