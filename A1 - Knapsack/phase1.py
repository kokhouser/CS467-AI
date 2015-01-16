import csv

class Item:
    def __init__(self):
        self.name = None
        self.cost = None
        self.value = None
        
    def setName (inName):
        self.name = inName
    
    def setCost (inCost):
        self.cost = inCost
        
    def setValue (inValue):
        self.value = inValue
        
    def getName():
        return self.name
        
    def getCost():
        return self.cost
        
    def getValue():
        return self.value
        
f = sys.stdin.readlines()
reader = csv.reader(f)
rowNum = 0
costLimit = 0
items = []
for row in reader:
    if rowNum == 0:
        costLimit = row[0]
    else:
        item = Item()
        item.setName(row[0])
        item.setCost(row[1])
        item.setValue(row[2])
        print ("%s, %s, %s" % (item.getName, item.getCost, item.getValue))
    rowNum += 1