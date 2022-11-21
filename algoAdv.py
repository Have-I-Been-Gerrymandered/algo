import csv
from operator import attrgetter


class District:
    def __init__(self, stateName, districtNum):
        self.state = stateName
        self.num = districtNum
        self.dem = 0
        self.rep = 0
        self.effGap = 0

    def getState(self):
        return self.state

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

    def getTotal(self):
        return self.dem + self.rep

    def getWinner(self):
        if self.rep > self.dem:
            return 'REPUBLICAN'
        else:
            return 'DEMOCRAT'



    def demWasted(self):
        if self.getWinner() == 'DEMOCRAT':
            return self.dem - int((self.dem+self.rep)/2) - 1
        else:
            return self.dem

    def repWasted(self):
        if self.getWinner() == 'REPUBLICAN':
            return self.rep - int((self.rep+self.dem)/2) - 1
        else:
            return self.rep

    def calcEffGap(self):
        self.effGap = round(100*abs(self.demWasted()-self.repWasted()) / float(self.getTotal()) , 4)

    def getEffGap(self):
        return self.effGap


    def advDemWasted(self):
        if self.getWinner() == 'DEMOCRAT':
            return self.dem - int((self.dem+self.rep)/2) - 1
        else:
            return self.dem

    def advRepWasted(self):
        if self.getWinner() == 'REPUBLICAN':
            return self.rep - int((self.rep+self.dem)/2) - 1
        else:
            return self.rep


    def advEffGap(self):
        return -1



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
        newDis = District(self.name, newDisNum)
        self.districts.append(newDis)

    def getDisCount(self):
        return len(self.districts)



def findPercentile(sortedList, districtCount, stateName, disNum):
    for i in range(0, districtCount):
        if sortedList[i].getState() == stateName and sortedList[i].getNum() == disNum:
            return round( i*100/float(districtCount) , 4)
    return -1




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
                        newDis = District(states[i].getName(), line[2])
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
                # create new district for new state
                newDis = District(newState.getName(), line[2])
                # dem in new dis
                if line[4] == "DEMOCRAT":
                    newDis.setDem(int(line[5]))
                # rep in new dis
                else:
                    newDis.setRep(int(line[5]))
                # append to districts array
                states[len(states)-1].addDis(newDis)


# print(len(states))
disCount = 0
for i in range(0, len(states)):
    # print(states[i].getName() + " ----------------------------- " + str(states[i].getDisCount()))
    disCount += states[i].getDisCount()
# print(count)

# calc eff gap and make presorted district list
sortedDistricts = []
for i in range (0, len(states)):
    for j in range(0, states[i].getDisCount()):
        states[i].getDis(j).calcEffGap()
        sortedDistricts.append(states[i].getDis(j))
# sort list of districts
sortedDistricts.sort(key=attrgetter('effGap'))





with open('results.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['State','District','Winner','Dem Votes','Rep Votes','Total Votes','Total Wasted','Dem Wasted', 'Rep Wasted', 'Eff Gap', 'Percentile', 'Adv Dem Wasted', 'Adv Rep Wasted', 'Adv Eff Gap', 'Adv Percentile'])

    for i in range(0, len(states)):
        for j in range(0, states[i].getDisCount()):
            newLine = [None] * 15
            newLine[0] = states[i].getName()
            newLine[1] = states[i].getDis(j).getNum()
            newLine[2] = states[i].getDis(j).getWinner()
            newLine[3] = states[i].getDis(j).getDem()
            newLine[4] = states[i].getDis(j).getRep()
            newLine[5] = states[i].getDis(j).getTotal()
            newLine[6] = states[i].getDis(j).demWasted() + states[i].getDis(j).repWasted()
            newLine[7] = states[i].getDis(j).demWasted()
            newLine[8] = states[i].getDis(j).repWasted()
            newLine[9] = states[i].getDis(j).getEffGap()
            newLine[10] = findPercentile(sortedDistricts, disCount, states[i].getName(), states[i].getDis(j).getNum())
            newLine[11] = -1
            newLine[12] = -1
            newLine[13] = -1
            newLine[14] = -1
            writer.writerow(newLine)

for i in range(0, disCount):
    print(sortedDistricts[i].getState() + ' ' + sortedDistricts[i].getNum() + ' ----- ' +  str(sortedDistricts[i].getEffGap()))