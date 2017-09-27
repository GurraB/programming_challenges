import sys
friendinput = sys.stdin.read().split('\n')
testcases = int(friendinput[0])
currentLine = 1

class person:
    checked = False
    personnumber = 0
    def __init__(self, personnumber):
        self.personnumber = personnumber

    def getfriends(self):
        totallyfriends = list()
        if self.checked:
            return list()
        self.checked = True
        totallyfriends.extend(friends[self.personnumber])
        for friend in friends[self.personnumber]:
            totallyfriends.extend(persons[friend - 1].getfriends())
        return list(set(totallyfriends))

for i in range(testcases):
    persons = list()
    friends = {}
    cityinformation = friendinput[currentLine].split(' ')
    currentLine += 1

    inhabitants = int(cityinformation[0])
    for j in range(inhabitants):
        friends[j + 1] = list()
        persons.append(person(j + 1))

    pairsofFriends = int(cityinformation[1])
    for j in range(pairsofFriends):
        friendPair = friendinput[currentLine].split(' ')
        currentLine += 1
        friends[int(friendPair[0])].append(int(friendPair[1]))
        friends[int(friendPair[1])].append(int(friendPair[0]))
    biggestgroup = 0
    for aperson in persons:
        amountoffriends = len(aperson.getfriends())
        if biggestgroup < amountoffriends:
            biggestgroup = amountoffriends
    print(biggestgroup if biggestgroup !=0 else 1)