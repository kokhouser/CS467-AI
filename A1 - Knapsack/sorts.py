import csv
import sys
import pprint

costLimit = 0
maxValue = 0
leaves = 0

class Item:
    def __init__(self):
        self.name = None
        self.cost = 0
        self.value = 0
        self.ratio = 0
        
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
        return int(self.value)
    
    def calcRatio(self):
        self.ratio = int(self.value)/int(self.cost)
        
    def getRatio(self):
        return self.ratio
        
class Knapsack:
    def __init__(self):
        self.sack = []
        self.value = 0
        self.cost = 0
    
    def addToSack(self, inItem):
        self.sack.append(inItem)
        self.value+=int(inItem.getValue())
        self.cost+=int(inItem.getCost())
    
    def getSack(self):
        return self.sack
    
    def getValue(self):
        return self.value
        
    def getCost(self):
        return self.cost
    
    def resetSack(self):
        self.sack = []
        self.value = 0
        self.cost = 0

def alphabetize(items):
    if len(items)>1:
        mid = len(items)//2
        lefthalf = items[:mid]
        righthalf = items[mid:]
        alphabetize(lefthalf)
        alphabetize(righthalf)
        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if (ord(lefthalf[i].getName()[0])<(ord(righthalf[j].getName()[0]))):
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

def sortCost(items):
    if len(items)>1:
        mid = len(items)//2
        lefthalf = items[:mid]
        righthalf = items[mid:]
        sortCost(lefthalf)
        sortCost(righthalf)
        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if (lefthalf[i].getCost())<(righthalf[j].getCost()):
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
        
def sortRatio(items):
    if len(items)>1:
        mid = len(items)//2
        lefthalf = items[:mid]
        righthalf = items[mid:]
        sortRatio(lefthalf)
        sortRatio(righthalf)
        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if (lefthalf[i].getRatio())>(righthalf[j].getRatio()):
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
            
def steal(knapsack,items):
    global costLimit
    localCost = costLimit
    for item in items:
        if (int(localCost)-int(item.getCost())>=0):
            knapsack.addToSack(item)
            localCost = int(localCost) - int(item.getCost())
        if (int(localCost) <= 0):
            break

rowNum = 0
f = sys.stdin.readlines()
reader = csv.reader(f)
items = []
knapsack = Knapsack()
#CSV reading stuff
for row in reader:
    if rowNum == 0:
        costLimit = row[0]
    else:
        item = Item()
        item.setName(row[0])
        item.setCost(row[1])
        item.setValue(row[2])
        item.calcRatio()
        items.append(item)
    rowNum += 1
sortCost(items)
'''
for item in items:
    print (item.getName(), end = ",")
print ('')
'''
print ("Stolen the best in terms of cost: ")
steal(knapsack,items)
newlist = sorted(knapsack.getSack(), key=lambda x: x.name)
for item in newlist:
    print (item.getName(), end=" ")
print ('')
print ("Cost:", knapsack.getCost())
print ("Value:", knapsack.getValue())
print ('')
knapsack.resetSack()
sortValue(items)
steal(knapsack,items)
print ("Stolen the best in terms of value: ")
newlist = sorted(knapsack.getSack(), key=lambda x: x.name)
for item in newlist:
    print (item.getName(), end=" ")
print ('')
print ("Cost:", knapsack.getCost())
print ("Value:", knapsack.getValue())
print ('')
knapsack.resetSack()
sortRatio(items)
steal(knapsack,items)
print ("Stolen the best in terms of ratio: ")
newlist = sorted(knapsack.getSack(), key=lambda x: x.name)
for item in newlist:
    print (item.getName(), end=" ")
print ('')
print ("Cost:", knapsack.getCost())
print ("Value:", knapsack.getValue())
print ('')

