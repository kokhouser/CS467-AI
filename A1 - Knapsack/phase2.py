import csv
import sys
import time
import pprint

#Defining global variables
start_time = float(time.time())
costLimit = 0
maxValue = 0
rowNum = 0
leaves = 0


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
        self.ratio = int(self.value)/int(self.cost)
        
    def getRatio(self):
        return self.ratio
        
class Tree:
    def __init__(self):
        self.sack = []
        self.left = None
        self.right = None
        self.totalCost = 0
        self.totalValue = 0
        self.bound = 0
    
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
        
    def getBound (self):
        return self.bound
    
    def setBound (self, inBound):
        self.bound = inBound
        
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

        
#Defining optimal knapsack
maxTree = Tree()
bestValue = 0
    
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
def printLeaves(inTree,pot):
    global maxValue
    global maxTree
    global bestValue
    global leaves

    leaves += 1
    #Makes sure we don't go down an unwanted rabbit hole.
    if (inTree.getTotalCost() > int(costLimit)):
        return
    
    #Makes sure we don't go down an unwanted rabbit hole.
    if (int(pot) < bestValue):
        return
    
    if (inTree.getLeft() == None) and (inTree.getRight() == None):
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
        newPotential = pot - int(inTree.getRight().getSack()[len(inTree.getRight().getSack())-1].getValue())
        printLeaves(inTree.getLeft(),newPotential)
        printLeaves(inTree.getRight(),pot)
        
f = sys.stdin.readlines()
reader = csv.reader(f)
knapsack = Tree()
ks = Knapsack()
items = []
items_back = []
potential = 0
#CSV reading stuff
for row in reader:
    if rowNum == 0:
        costLimit = row[0]
    else:
        item = Item()
        item_back = Item()
        item.setName(row[0])
        item.setCost(row[1])
        item.setValue(row[2])
        potential += int(item.getValue())
        item_back.setName(row[0])
        item_back.setCost(row[1])
        item_back.setValue(row[2])
        items_back.append(item_back)
        items.append(item)
        addToLeaf(knapsack, item)
    rowNum += 1

sortCost(items_back)
steal(ks, items_back)
if (int(ks.getValue())>int(bestValue)):
    bestValue = ks.getValue()
ks.resetSack()
sortValue(items_back)
steal(ks, items_back)
if (int(ks.getValue())>int(bestValue)):
    bestValue = ks.getValue()
ks.resetSack()
sortRatio(items_back)
steal(ks, items_back)
if (int(ks.getValue())>int(bestValue)):
    bestValue = ks.getValue()
ks.resetSack()
#Printing the valid knapsacks
printLeaves(knapsack,potential)
#Printing the optimal knapsack
print ("Optimal Knapsack:", end=' ')
for item in (maxTree.getSack()):
    print (item.getName(), end=", ")
print (' ')
print ("Cost:",maxTree.getTotalCost())
print ("Value:",maxTree.getTotalValue())
print (' ')
print ("Best greedy:",bestValue)
print (' ')
print ("Nodes evaluated:", leaves)
print (' ')
print("--- seconds ---", time.time() - start_time)
