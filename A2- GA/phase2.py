import csv
import sys
import time
from random import randint


#Globals
costLimit = 0


class Item:
    def __init__(self):
        self.name = None
        self.cost = 0
        self.value = 0
        
    def setName (self, inName):
        self.name = inName
    
    def setCost (self, inCost):
        self.cost = inCost
        
    def setValue (self, inValue):
        self.value = inValue
        
    def getName(self):
        return self.name
        
    def getCost(self):
        return self.cost
        
    def getValue(self):
        return self.value

class Knapsack:
    def __init__(self):
        self.sack = []
        self.value = 0
        self.cost = 0
        #self.fitness = 0
        
    def addToSack(self, inItem):
        self.value += int(inItem.getValue())
        self.cost += int(inItem.getCost())
    
    def getSack(self):
        return self.sack
    
    def getValue(self):
        return self.value

    def setValue(self, inValue):
        self.value = inValue
        
    def getCost(self):
        return self.cost
    
    def resetSack(self):
        self.sack = []
        self.value = 0
        self.cost = 0

    def setSack(self,inSack):
        self.sack = inSack
    
    '''
    def setFitness(self, inFitness):
        self.fitness = inFitness
        
    def getFitness(self):
        return self.fitness
    '''
        
def calcFitness(inSack,inItems):
    count = 0
    for item in inItems:
        if (inSack.getSack()[count] == 1):
            inSack.addToSack(item)
            if (inSack.getCost()>int(costLimit)):
                inSack.setValue(0)
                break
        count += 1
        
def randomGenesis(inSack, numItems):
    for x in range (0, numItems):
        inSack.getSack().append(randint(0,1))
        
def sortValue(items):
    if len(items)>1:
        mid = len(items)//2
        lefthalf = items[:mid]
        righthalf = items[mid:]
        sortValue(lefthalf)
        sortValue(righthalf)
        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if (lefthalf[i].getValue())>(righthalf[j].getValue()):
                items[k]=lefthalf[i]
                i=i+1
            else:
                items[k]=righthalf[j]
                j=j+1
            k=k+1

        while i<len(lefthalf):
            items[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j<len(righthalf):
            items[k]=righthalf[j]
            j=j+1
            k=k+1

def createOffspring(sack1, sack2):
    mid = len(sack1.getSack())//2
    lefthalf = sack1.getSack()[:mid]
    righthalf = sack2.getSack()[mid:]
    newSack = lefthalf+righthalf
    childSack = Knapsack()
    childSack.setSack(newSack)
    return childSack
        
f = sys.stdin.readlines()
reader = csv.reader(f)
items = []
rowNum = 0
for row in reader:
	if rowNum == 0:
		costLimit = row[0]
	else:
		item = Item()
		item.setName(row[0])
		item.setCost(row[1])
		item.setValue(row[2])
		items.append(item)
	rowNum += 1
leaderboard = []
leadCount = 0
while (leadCount < 10):
    sack = Knapsack()
    randomGenesis(sack,len(items))
    calcFitness(sack,items)
    if (sack.getValue()>0):
        leaderboard.append(sack)
        leadCount += 1
print ("100 Sacks Are:")
sortValue(leaderboard)
for sack in leaderboard:
    for sackItem in sack.getSack():
        print (sackItem, end="")
    print (", Cost = ",sack.getCost(), ", Value = ",sack.getValue())
print ()
print ("New Offspring:")
childSack = createOffspring(leaderboard[0],leaderboard[1]);
calcFitness(childSack,items);
for sackItem in childSack.getSack():
    print (sackItem, end="")
print (", Cost = ",childSack.getCost(), ", Value = ",childSack.getValue())
print ()
if (childSack.getValue()>leaderboard[-1].getValue()):
    print("Ritual passed! Child is fit to be accepted into the population.")
    print ()
    leaderboard.append(childSack)
    sortValue(leaderboard)
    del leaderboard[-1]
    print ("New Population:")
    for sack in leaderboard:
        for sackItem in sack.getSack():
            print (sackItem, end="")
        print (", Cost = ",sack.getCost(), ", Value = ",sack.getValue())
    print ()
else:
    print("Ritual failed! Child is unfit to be accepted into society. Commencing incineration of disgraceful offspring.")
    print()
