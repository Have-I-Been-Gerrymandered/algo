import csv


class District:
    def __init__(self, districtNum):
        self.num = districtNum
        self.dem = -1
        self.rep = -1

    def getNum(self):
        return self.num

    def setDem(self, demVotes):
        self.dem = demVotes

    def setRep(self, repVotes):
        self.rep = repVotes

    def getDem(self):
        return self.dem

    def getRep(self):
        return self.rep

    # def calcEffGap(self):
    #     return -1

    # def calcAdvEffGap(self):
    #     return -1



class State:
    def __init__(self, stateName, stateAppr):
        self.name = stateName
        self.appr = stateAppr
        self.districts = []

    def getName(self):
        return self.name

    def addDis(self, newDis):
        self.districts.append(newDis)

    def getDisIndex(self, disNum):
        for i in range(0, len(self.districts)):
            # if seen district before
            if self.districts[i].getNum() == disNum:
                return i
        # return -1 if not seen district before
        return -1

    def getDis(self, index):
        return self.districts[index]

    def addDistrict(self, newDisNum):
        newDis = District(newDisNum)
        self.districts.append(newDis)

    def getDisCount(self):
        return len(self.districts)






states = []
with open("2020HouseData.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for line in reader:
        if line[4] == "DEMOCRAT" or line[4] == "REPUBLICAN":    # ignore all 3rd party folks
            # print(line)
            found = False

            for i in range(0, len(states)):
                # if seen state before
                if line[0] == states[i].getName():

                    # if new district
                    disIndex = states[i].getDisIndex(line[2])
                    if disIndex == -1:
                        newDis = District(line[2])
                        # dem in new dis
                        if line[4] == "DEMOCRAT":
                            newDis.setDem(int(line[5]))
                        # rep in new dis
                        else:
                            newDis.setRep(int(line[5]))
                        # append to districts array
                        states[i].addDis(newDis)

                    # exisitng district
                    else:

                        # dem in old dis
                        if line[4] == "DEMOCRAT":
                            states[i].getDis(disIndex).setDem(int(line[5]))
                            # ! count total
                        # rep in old dis
                        else:
                            states[i].getDis(disIndex).setRep(int(line[5]))
                            # ! count total
                    # print("old - " + line[0])
                    found = True

            
            # create new state
            if found == False:
                # print("new - " + line[0])
                newState = State(line[0], line[1])
                states.append(newState)
                # ! create new district for new state

print(len(states))
count = 0
for i in range(0, len(states)):
    print(states[i].getName() + " - " + str(states[i].getDisCount()))
    count += states[i].getDisCount()
# print(count)
