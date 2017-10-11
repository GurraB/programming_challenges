import sys
lines = sys.stdin.read().split('\n')

for line in lines:
    args = line.split(' ')
    if len(args) > 1:
        counter = 0
        for i in range(len(args[1])):
            if counter < len(args[0]):
                if args[1][i] == args[0][counter]:
                    counter += 1
        if len(args[0]) == counter:
            print('Yes')
        else:
            print('No')