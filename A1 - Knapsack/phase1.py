import csv
import sys
import pprint

costLimit = 0
class Item:
    def __init__(self):
        self.name = None
        self.cost = None
        self.value = None
        
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
        
class Tree:
    def __init__(self):
        self.sack = []
        self.left = None
        self.right = None
        self.totalCost = 0
    
    def addToSack (self, inItem):
        self.sack.append(inItem)
        self.totalCost += int(inItem.getCost())
        
    def setSack (self, inSack):
        self.sack = inSack
    
    def setLeft (self, inTree):
        self.left = inTree
        self.totalCost += inTree.getTotalCost()
    
    def setRight (self, inTree):
        self.right = inTree
        
    def getSack (self):
        return self.sack

    def getLeft (self):
        return self.left
    
    def getRight (self):
        return self.right
        
    def getTotalCost (self):
        return self.totalCost
    
def addToLeaf(inTree, inItem):
    if (inTree.getLeft() == None) and (inTree.getRight() == None):
        sameTree = Tree()
        newTree = Tree()
        for item in inTree.getSack():
            newTree.addToSack(item)
            sameTree.addToSack(item)
        newTree.addToSack(inItem)
        inTree.setLeft(newTree)
        inTree.setRight(sameTree)
    else:
        addToLeaf (inTree.getLeft(), inItem)
        addToLeaf (inTree.getRight(), inItem)
        
def printLeaves(inTree):
    if (inTree.getLeft() == None) and (inTree.getRight() == None):
        if (inTree.getTotalCost() <= int(costLimit)):
            print (inTree.getTotalCost())
            for item in (inTree.getSack()):
                print (item.getName(),end="")
            print (' ')
    else:
        printLeaves(inTree.getLeft())
        printLeaves(inTree.getRight())
        
f = sys.stdin.readlines()
reader = csv.reader(f)
rowNum = 0
knapsack = Tree()
items = []
for row in reader:
    if rowNum == 0:
        costLimit = row[0]
    else:
        item = Item()
        item.setName(row[0])
        item.setCost(row[1])
        item.setValue(row[2])
        #sameTree = Tree()
        #sameTree.setSack = items;
        items.append(item)
        #addTree = Tree()
        #addTree.setSack = items;
        addToLeaf(knapsack, item)
        #print ("%s, %s, %s" % (item.getName(), item.getCost(), item.getValue()))
    rowNum += 1
printLeaves(knapsack)
