import csv
import sys
import time
import copy

print ("""
  _  __                                 _      _______ _     _       __
 | |/ /                                | |    |__   __| |   (_)     / _|
 | ' / _ __   __ _ _ __  ___  __ _  ___| | __    | |  | |__  _  ___| |_
 |  < | '_ \ / _` | '_ \/ __|/ _` |/ __| |/ /    | |  | '_ \| |/ _ \  _|
 | . \| | | | (_| | |_) \__ \ (_| | (__|   <     | |  | | | | |  __/ |
 |_|\_\_| |_|\__,_| .__/|___/\__,_|\___|_|\_\    |_|  |_| |_|_|\___|_|
                  | |
                  |_|
                  """)

start_time = float(time.time())
costLimit = 0
maxValue = 0
bestSack = None
rowNum = 0
height = 0
nodeIndex = 0

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

class Node:
	def __init__(self):
		self.sack = []
		self.height = 0
		self.totalCost = 0
		self.totalValue = 0
		self.finishedLeft = False
		self.finishedRight = False
		self.pot = 0

	def addToSack(self, inItem):
		self.sack.append(inItem)
		self.totalCost += int(inItem.getCost())
		self.totalValue += int(inItem.getValue())

	def getSack(self):
		return self.sack

	def getTotalCost(self):
		return self.totalCost

	def getTotalValue(self):
		return self.totalValue

	def setFinishedLeft(self, inState):
		self.finishedLeft = inState

	def isFinishedLeft(self):
		return self.finishedLeft

	def setFinishedRight(self):
		self.finishedRight = True

	def isFinishedRight(self):
		return self.finishedRight

	def getHeight(self):
		return self.height

	def setHeight(self, inHeight):
		self.height = inHeight

	def getPot(self):
		return self.pot

	def setPot(self, inPot):
		self.pot = inPot

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

    def setValue(self, inValue):
        self.value = inValue
        
    def getCost(self):
        return self.cost
    
    def resetSack(self):
        self.sack = []
        self.value = 0
        self.cost = 0

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

def stealPartial(knapsack,items):
    global costLimit
    localCost = costLimit
    for item in items:
        if (int(localCost) < 0):
        	return knapsack.getValue()

        elif (int(localCost)-int(item.getCost())>=0):
            knapsack.addToSack(item)
            localCost = int(localCost) - int(item.getCost())

        elif (int(localCost)>0):
        	knapsack.setValue(float(knapsack.getValue()) +float(float(localCost)*float(item.getRatio())))
        	return knapsack.getValue()

'''
#Recursive solution, not written well
def traverse(tree,items):
	global maxValue
	global bestSack
	global height
	global nodeIndex
	if (len(tree) == 0):
		return
	else:
		if (tree[nodeIndex].isFinishedLeft() and tree[nodeIndex].isFinishedRight()):
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			traverse (tree, items)
		elif (tree[nodeIndex].getHeight() == len(items)):
			#Evaluate, now at leaf
			if ((tree[nodeIndex].getTotalCost() <= int(costLimit))):
			#if ((tree[nodeIndex].getTotalCost() < 999)):
				print ("Possible knapsack:")
				for item in tree[nodeIndex].getSack():
					print (item.getName(), end=" ")
				print (' ')
				print ("Total cost:", tree[nodeIndex].getTotalCost())
				print ("Total value:", tree[nodeIndex].getTotalValue())
				print (' ')
				if (tree[nodeIndex].getTotalValue() > maxValue):
					maxValue = tree[nodeIndex].getTotalValue()
					bestSack = tree[nodeIndex]
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			traverse (tree, items)
		elif (tree[nodeIndex].isFinishedLeft() == False):
			height += 1
			#newNode = copy.deepcopy(tree[nodeIndex])
			newNode = Node()
			for item in tree[nodeIndex].getSack():
				newNode.addToSack(item)
			newNode.setHeight(height)
			tree[nodeIndex].setFinishedLeft(True)
			nodeIndex += 1
			tree.append(newNode)
			traverse (tree, items)
		elif (tree[nodeIndex].isFinishedLeft() == True and tree[nodeIndex].isFinishedRight() == False):
			height += 1
			#newNode = copy.deepcopy(tree[nodeIndex])
			newNode = Node()
			for item in tree[nodeIndex].getSack():
				newNode.addToSack(item)
			newNode.addToSack(items[height-1])
			newNode.setHeight(height)
			newNode.setFinishedLeft(False)
			tree[nodeIndex].setFinishedRight()
			nodeIndex += 1
			tree.append(newNode)
			traverse (tree, items)
'''
bestValue = 0
potential = 0
f = sys.stdin.readlines()
reader = csv.reader(f)
items = []
ks = Knapsack()
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
		potential += int(item.getValue())
	rowNum += 1
sortCost(items)
steal(ks, items)
if (int(ks.getValue())>int(bestValue)):
    bestValue = ks.getValue()
print ("Stolen the best in terms of cost: ")
newlist = sorted(ks.getSack(), key=lambda x: x.name)
for item in newlist:
    print (item.getName(), end=" ")
print ('')
print ("Cost:", ks.getCost())
print ("Value:", ks.getValue())
print ('')
ks.resetSack()
sortValue(items)
steal(ks, items)
if (int(ks.getValue())>int(bestValue)):
    bestValue = ks.getValue()
print ("Stolen the best in terms of value: ")
newlist = sorted(ks.getSack(), key=lambda x: x.name)
for item in newlist:
    print (item.getName(), end=" ")
print ('')
print ("Cost:", ks.getCost())
print ("Value:", ks.getValue())
print ('')
ks.resetSack()
sortRatio(items)
steal(ks, items)
if (int(ks.getValue())>int(bestValue)):
    bestValue = ks.getValue()
print ("Stolen the best in terms of ratio: ")
newlist = sorted(ks.getSack(), key=lambda x: x.name)
for item in newlist:
    print (item.getName(), end=" ")
print ('')
print ("Cost:", ks.getCost())
print ("Value:", ks.getValue())
print ('')
ks.resetSack()
partialValue=stealPartial(ks, items)
print ("Partial Knapsack: ")
print ("Value:", partialValue)
print ('')
print("--- seconds ---", time.time() - start_time, "\n")
ks.resetSack()
empty = Node()
empty.setPot(potential)
tree = [empty]
#traverse(tree, items)
nodesVisited = 1
#print (potential)
while (True):
	if (len(tree) == 0):
		break
	else:
		
		#Optimization 1
		if (tree[nodeIndex].getTotalCost() > int(costLimit)):
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			continue
		#Optimization 2
		elif (tree[nodeIndex].getPot() < bestValue):
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			continue
		
		elif (tree[nodeIndex].isFinishedLeft() and tree[nodeIndex].isFinishedRight()):
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			continue
		elif (tree[nodeIndex].getHeight() == len(items)):
			#Evaluate, now at leaf
			if ((tree[nodeIndex].getTotalCost() <= int(costLimit))):
				if (tree[nodeIndex].getTotalValue() > maxValue):
					maxValue = tree[nodeIndex].getTotalValue()
					bestSack = tree[nodeIndex]
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			continue
		elif (tree[nodeIndex].isFinishedLeft() == False):
			nodesVisited += 1
			height += 1
			#newNode = copy.deepcopy(tree[nodeIndex])
			newNode = Node()
			newNode.setPot(tree[nodeIndex].getPot() - int(items[height-1].getValue()))
			for item in tree[nodeIndex].getSack():
				newNode.addToSack(item)
			newNode.setHeight(height)
			tree[nodeIndex].setFinishedLeft(True)
			nodeIndex += 1
			tree.append(newNode)
			continue
		elif (tree[nodeIndex].isFinishedLeft() == True and tree[nodeIndex].isFinishedRight() == False):
			nodesVisited += 1
			height += 1
			#newNode = copy.deepcopy(tree[nodeIndex])
			newNode = Node()
			newNode.setPot(tree[nodeIndex].getPot())
			for item in tree[nodeIndex].getSack():
				newNode.addToSack(item)
			newNode.addToSack(items[height-1])
			newNode.setHeight(height)
			newNode.setFinishedLeft(False)
			tree[nodeIndex].setFinishedRight()
			nodeIndex += 1
			tree.append(newNode)
			continue
newlist = sorted(bestSack.getSack(), key=lambda x: x.name)
print ("Optimized knapsack:")
for item in newlist:
	print (item.getName(), end=" ")
print (' ')
print ("Total cost:", bestSack.getTotalCost())
print ("Total value:", bestSack.getTotalValue())
print (' ')
print ('Nodes visited:', nodesVisited)
print("--- seconds ---", time.time() - start_time)
bestSack = None
nodeIndex = 0
maxValue = 0
height = 0
empty = Node()
empty.setPot(potential)
tree = [empty]
#traverse(tree, items)
nodesVisited = 1
#print (potential)
while (True):
	if (len(tree) == 0):
		break
	else:
		if (tree[nodeIndex].isFinishedLeft() and tree[nodeIndex].isFinishedRight()):
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			continue
		elif (tree[nodeIndex].getHeight() == len(items)):
			#Evaluate, now at leaf
			if ((tree[nodeIndex].getTotalCost() <= int(costLimit))):
				if (tree[nodeIndex].getTotalValue() > maxValue):
					maxValue = tree[nodeIndex].getTotalValue()
					bestSack = tree[nodeIndex]
			del tree[nodeIndex]
			nodeIndex -= 1
			height -= 1
			continue
		elif (tree[nodeIndex].isFinishedLeft() == False):
			nodesVisited += 1
			height += 1
			#newNode = copy.deepcopy(tree[nodeIndex])
			newNode = Node()
			newNode.setPot(tree[nodeIndex].getPot() - int(items[height-1].getValue()))
			for item in tree[nodeIndex].getSack():
				newNode.addToSack(item)
			newNode.setHeight(height)
			tree[nodeIndex].setFinishedLeft(True)
			nodeIndex += 1
			tree.append(newNode)
			continue
		elif (tree[nodeIndex].isFinishedLeft() == True and tree[nodeIndex].isFinishedRight() == False):
			nodesVisited += 1
			height += 1
			#newNode = copy.deepcopy(tree[nodeIndex])
			newNode = Node()
			newNode.setPot(tree[nodeIndex].getPot())
			for item in tree[nodeIndex].getSack():
				newNode.addToSack(item)
			newNode.addToSack(items[height-1])
			newNode.setHeight(height)
			newNode.setFinishedLeft(False)
			tree[nodeIndex].setFinishedRight()
			nodeIndex += 1
			tree.append(newNode)
			continue
newlist = sorted(bestSack.getSack(), key=lambda x: x.name)
print (" ")
print ("Brute-Forced knapsack:")
for item in newlist:
	print (item.getName(), end=" ")
print (' ')
print ("Total cost:", bestSack.getTotalCost())
print ("Total value:", bestSack.getTotalValue())
print (' ')
print ('Nodes visited:', nodesVisited)
print("--- seconds ---", time.time() - start_time)