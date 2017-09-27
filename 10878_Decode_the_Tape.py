import sys

tape = sys.stdin.read().split('\n')
message = ""
for line in tape:
    if not (line == '' or line == "___________"):
        lineinfo = ''
        for i in range(9):
            if line[i + 1] == 'o':
                lineinfo += '1'
            elif line[i + 1] == '.':
                continue
            else:
                lineinfo += '0'
        message += chr(int(lineinfo, 2))
print(message, end="")