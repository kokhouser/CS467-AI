import csv
import sys
import pprint

#Defining global variables
costLimit = 0
maxValue = 0
rowNum = 0
leaves = 0


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
        self.totalValue = 0
    
    def addToSack (self, inItem):
        self.sack.append(inItem)
        self.totalCost += int(inItem.getCost())
        self.totalValue += int (inItem.getValue())
        
    def setSack (self, inSack):
        self.sack = inSack
    
    def setLeft (self, inTree):
        self.left = inTree
    
    def setRight (self, inTree):
        self.right = inTree
        #self.totalCost += inTree.getTotalCost()
        #self.totalValue += inTree.getTotalValue()
        
    def getSack (self):
        return self.sack

    def getLeft (self):
        return self.left
    
    def getRight (self):
        return self.right
        
    def getTotalCost (self):
        return self.totalCost
        
    def getTotalValue (self):
        return self.totalValue

        
#Defining optimal knapsack
maxTree = Tree()
    
def addToLeaf(inTree, inItem):
    global maxValue
    global maxTree
    global rowNum
    if (inTree.getLeft() == None) and (inTree.getRight() == None):
        #Initializing new subtrees
        sameTree = Tree()
        newTree = Tree()
        #Adding existing items to new subtrees
        for item in inTree.getSack():
            newTree.addToSack(item)
            sameTree.addToSack(item)
        #Adding new item to newTree
        newTree.addToSack(inItem)
        #Setting respective pointers to their respective subtrees
        inTree.setLeft(sameTree)
        inTree.setRight(newTree)
    else:
        addToLeaf (inTree.getLeft(), inItem)
        addToLeaf (inTree.getRight(), inItem)
        
#Simple traversal and print function, only prints those valid within cost limit.
def printLeaves(inTree):
    global maxValue
    global maxTree
    global leaves
    
    #Makes sure we don't go down an unwanted rabbit hole.
    if (inTree.getTotalCost() > int(costLimit)):
        return
    
    if (inTree.getLeft() == None) and (inTree.getRight() == None):
        leaves += 1
        #Change indentation!
        if (inTree.getTotalCost() <= int(costLimit)):
            print ("Cost:",inTree.getTotalCost())
            print ("Value:",inTree.getTotalValue())
            print ("Items:", end=" ")
            for item in (inTree.getSack()):
                print (item.getName(),end=", ")
            print (' ')
            print (' ')
            if (inTree.getTotalValue() > int(maxValue)):
                maxTree = inTree
                maxValue = inTree.getTotalValue()
    #elif (inTree.getTotalCost() > int(costLimit)):
    #    return
    else:
        printLeaves(inTree.getLeft())
        printLeaves(inTree.getRight())
        
f = sys.stdin.readlines()
reader = csv.reader(f)
knapsack = Tree()
items = []
#CSV reading stuff
for row in reader:
    if rowNum == 0:
        costLimit = row[0]
    else:
        item = Item()
        item.setName(row[0])
        item.setCost(row[1])
        item.setValue(row[2])
        items.append(item)
        addToLeaf(knapsack, item)
    rowNum += 1
#Printing the valid knapsacks
printLeaves(knapsack)
#Printing the optimal knapsack
print ("Optimal Knapsack:", end=' ')
for item in (maxTree.getSack()):
    print (item.getName(), end=", ")
print (' ')
print ("Cost:",maxTree.getTotalCost())
print ("Value:",maxTree.getTotalValue())
print (' ')
print ("Leaves evaluated:", leaves)
