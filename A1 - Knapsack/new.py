import csv
import sys
import time
import copy

class Item:
    def __init__(self):
        self.name = None
        self.cost = 0
        self.ratio = 0
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

    def calcRatio(self):
        self.ratio = float(self.value)/float(self.cost)
        
    def getRatio(self):
        return self.ratio
        
class Sack:
    def __init__(self):
        self.knapsack = []
        self.totalCost = 0
        self.value = 0
    
    def setTotalCost(self, inCost):
        self.totalCost = inCost
    
    def setValue(self, inValue):
        self.value = inValue
    
    def addToKnapsack(self, inItem):
        self.knapsack.append(inItem)
        self.totalCost += int(inItem.getCost())
        self.value += int(inItem.getValue())
    
    def getTotalCost(self):
        return self.totalCost
    
    def getValue(self):
        return self.value
    
    def getKnapsack(self):
        return self.knapsack
        
rowNum = 0
costLimit = 0
f = sys.stdin.readlines()
reader = csv.reader(f)
empty = Sack()
leaves = [empty]
for row in reader:
    if rowNum == 0:
        costLimit = row[0]
    else:
        item = Item()
        item_back = Item()
        item.setName(row[0])
        item.setCost(row[1])
        item.setValue(row[2])
        clones = []
        for leaf in leaves:
            clones.append(copy.deepcopy(leaf))
        for leaf in leaves:
            if (leaf.getTotalCost() > int(costLimit)):
                del leaf
            else:
                leaf.addToKnapsack(item)
        for clone in clones:
            leaves.append(clone)
        #potential += int(item.getValue())
        '''
        item_back.setName(row[0])
        item_back.setCost(row[1])
        item_back.setValue(row[2])
        items_back.append(item_back)
        '''
        #addToLeaf(knapsack, item)
        #leafNodes = addToLeaf(leafNodes, item)
    rowNum += 1
#print (leaves[2].getKnapsack()[4].getName())
for leaf in leaves:
    print("Knapsack:")
    for item in leaf.getKnapsack():
        print (item.getName(), end=",")
    print ()
    print ("Value:")
    print (leaf.getValue())
    print (' ')
