import itertools
import operator
import time
import copy
from random import randint

scores = {'e': 1, 'a':1, 'i':1,'o':1,'n':1,'r':1,'t':1,'l':1,'s':1,'u':1,'d':2,'g':2,'b':3,'c':3,'m':3,'p':3,'f':4,'h':4,'v':4,'w':4,'y':4,'k':5,'j':8,'x':8,'q':10,'z':10}

class Word:
    def __init__(self):
        self.word = ""
        self.score = 0
    
    def setWord(self,inWord):
        self.word = inWord
    
    def getWord (self):
        return self.word
    
    def setScore(self,inScore):
        self.score = inScore
    
    def getScore(self):
        return self.score

class Attempt:
	def __init__(self):
		self.words = []
		self.used =  []
		self.unused = []
		self.totalScore = 0
		self.weight = 0

	def getWords(self):
		return self.words

	def addToWords(self, inWord):
	    unusedCopy = copy.deepcopy(self.unused)
	    for char in inWord.getWord():
	        if char in unusedCopy:
	            unusedCopy.remove(char)
	        else:
	            return
	    self.words.append(inWord)
	    for char in inWord.getWord():
	        self.unused.remove(char)
	        self.used.append(char)
			
	def setWeight(self,inWeight):
	    self.weight = inWeight
	    
	def getWeight(self):
	    return self.weight

	def getUsed(self):
		return self.used
	
	def setUsed(self, inList):
	    self.used = inList

	def getUnused(self):
		return self.unused

	def setUnused(self,inList):
		self.unused = inList

	def setTotalScore(self, inScore):
		self.totalScore = inScore

	def getTotalScore(self):
		return self.totalScore

	def generateWords(self):
		while (len(self.unused)>1):
			length = len(self.unused)
			randLength = randint(2,length if (length<11) else 10)
			newWord = ""
			newWordClass = Word()
			unusedWords = []
			for char in self.unused:
				unusedWords.append(char)
			while randLength > 0:
				usedIndex = randint(0,len(unusedWords)-1) #if len(unusedWords) > 0 else 0
				newWord += unusedWords[usedIndex]
				del(unusedWords[usedIndex])
				randLength -= 1
			newWordClass.setWord(newWord.lower())
			self.addToWords(newWordClass)
		if len(self.unused)>0:
		    newWordClass = Word()
		    newWord = ""
		    for char in self.unused:
		        newWord += char
		    newWordClass.setWord(newWord)
		    self.addToWords(newWordClass)
		#print (self.words)

	def calculateScore(self):
	    self.totalScore = 0
	    for each in self.words:
	        #print (each.getWord())
	        if each.getWord() in legal:
	            wordScore = 0
	            for char in each.getWord():
	                self.totalScore+=scores[char]
	                wordScore+=scores[char]
	            each.setScore(wordScore)
	'''
		for each in self.words:
		    if each.getWord() in legal:
				#if len(each) > 3:
				#	print ("Long: ", each)
                wordScore = 0
                for char in each.getWord():
					self.totalScore+=scores[char]
					wordScore+=scores[char]
				each.setScore(wordScore)
	'''
def createAttempt(parent1, parent2, unused):
    mid1 = len(parent1.getWords())/2
    mid2 = len(parent2.getWords())/2
    newAttempt = Attempt()
    newAttempt.setUnused(unused)
    current = 0
    '''
    for each in parent1.getWords():
        if current > mid1:
            break
        if each.getWord() in legal:
            newAttempt.addToWords(each)
            current += 1
    current = 0
    for each in parent2.getWords():
        if current > mid2:
            break
        if each.getWord() in legal:
            newAttempt.addToWords(each)
            current += 1
    '''
    check = False
    for x in range (0,max(len(parent1.getWords()),len(parent2.getWords()))):
        if x == len(parent1.getWords()):
            check = True
        if x == len(parent2.getWords()):
            check = True
        if check == False and x%2 == 0:
            if parent1.getWords()[x].getWord() in legal:
                newAttempt.addToWords(parent1.getWords()[x])
        elif check == False and x%2 == 1:
            if parent2.getWords()[x].getWord() in legal:
                newAttempt.addToWords(parent2.getWords()[x])
        elif check == True and len(parent1.getWords()) > x:
            if parent1.getWords()[x].getWord() in legal:
                newAttempt.addToWords(parent1.getWords()[x])
        elif check == True and len(parent2.getWords()) > x:
            if parent2.getWords()[x].getWord() in legal:
                newAttempt.addToWords(parent2.getWords()[x])
    return newAttempt
            
def cataclysm(leaderboard):
    for x in range (1, len(leaderboard)-1):
        currentAttempt = leaderboard[x]
        for word in currentAttempt.getWords():
            chance = randint(0,9)
            if chance <= 3:
                unusedCopy = copy.deepcopy(currentAttempt.getUnused())
                usedCopy = copy.deepcopy(currentAttempt.getUsed())
                for char in word.getWord():
                    unusedCopy.append(char)
                    if char in usedCopy:
                        usedCopy.remove(char)
                currentAttempt.setUnused(unusedCopy)
                currentAttempt.setUsed(usedCopy)
                currentAttempt.getWords().remove(word)
        currentAttempt.generateWords()
        currentAttempt.calculateScore()

f = open("words.txt","r")
str1 = f.read().lower()
f.close

legal = {}
temp = str1.split(" ")
for each in temp:
    legal[each]=""

words = {}

guess = input("Enter some letters: ")
leaderboard = []
while len(leaderboard)<100:
	guess2 = []
	for char in guess:
		guess2.append(char.lower())
	newAttempt = Attempt()
	newAttempt.setUnused(guess2)
	newAttempt.generateWords()
	if ([] in newAttempt.getWords()):
		newAttempt.getWords().remove([])
	newAttempt.calculateScore()
	if (newAttempt.getTotalScore()>0):
		leaderboard.append(newAttempt)
while True:
    leaderboard.sort(key=lambda x: x.getTotalScore(), reverse=True)
    weight = 100
    accumulator = 0
    selected1 = Attempt()
    selected2 = Attempt()
    isSelected1 = False
    isSelected2 = False
    randSelected1 = randint(1,5050)
    randSelected2 = randint(1,5050)
    for each in leaderboard:
    	#if each.getTotalScore() > 10:
    	#	print ("High!")
    	#print ("Score:", each.getTotalScore())
    	accumulator += weight
    	each.setWeight(weight)
    	weight -= 1
    	if isSelected1 != True and randSelected1 <= accumulator:
    	    selected1 = each
    	    isSelected1 = True
    	if isSelected2 != True and randSelected2 <= accumulator:
    	    selected2 = each
    	    isSelected2 = True
    	    '''
    print ("First Parent:")
    for each in selected1.getWords():
        print (each.getWord(), end =", ")
    print ()
    print ("Second Parent:")
    for each in selected2.getWords():
        print (each.getWord(), end =", ")
    print ()
    '''
    guess2 = []
    for char in guess:
        guess2.append(char)
    newAttempt = createAttempt(selected1, selected2, guess2)
    newAttempt.generateWords()
    newAttempt.calculateScore()
    '''
    print ("New Child:")
    for each in newAttempt.getWords():
        print (each.getWord(), end=", ")
    print ()
    '''
    print ("Score", newAttempt.getTotalScore())
    if (newAttempt.getTotalScore() > leaderboard[-1].getTotalScore()):
        #print ("Child accepted!")
        leaderboard.append(newAttempt)
        leaderboard.sort(key=lambda x: x.getTotalScore(), reverse=True)
        del leaderboard[-1]
    #else:
        #print ("Child not accepted!")
    equal = True
    firstScore = leaderboard[0].getTotalScore()
    for each in leaderboard:
        if each.getTotalScore() != firstScore:
            equal = False
            break
    if equal == True:
        break
for each in leaderboard:
    for word in each.getWords():
        print (word.getWord(), end=" ")
    print ("Score", each.getTotalScore())
print ()
cataCount = 0
while (cataCount < 3):
    print ("Cataclysmic mutation!")
    cataclysm(leaderboard)
    print ()
    while True:
        leaderboard.sort(key=lambda x: x.getTotalScore(), reverse=True)
        weight = 100
        accumulator = 0
        selected1 = Attempt()
        selected2 = Attempt()
        isSelected1 = False
        isSelected2 = False
        randSelected1 = randint(1,5050)
        randSelected2 = randint(1,5050)
        for each in leaderboard:
        	#if each.getTotalScore() > 10:
        	#	print ("High!")
        	#print ("Score:", each.getTotalScore())
        	accumulator += weight
        	each.setWeight(weight)
        	weight -= 1
        	if isSelected1 != True and randSelected1 <= accumulator:
        	    selected1 = each
        	    isSelected1 = True
        	if isSelected2 != True and randSelected2 <= accumulator:
        	    selected2 = each
        	    isSelected2 = True
        guess2 = []
        for char in guess:
            guess2.append(char)
        newAttempt = createAttempt(selected1, selected2, guess2)
        newAttempt.generateWords()
        newAttempt.calculateScore()
        print ("Score", newAttempt.getTotalScore())
        if (newAttempt.getTotalScore() > leaderboard[-1].getTotalScore()):
            #print ("Child accepted!")
            leaderboard.append(newAttempt)
            leaderboard.sort(key=lambda x: x.getTotalScore(), reverse=True)
            del leaderboard[-1]
        #else:
            #print ("Child not accepted!")
        firstScore = leaderboard[0].getTotalScore()
        equal1 = 0
        for each in leaderboard:
            if each.getTotalScore() != firstScore:
                equal1 += 1
        if equal1 <= 2:
            break
    cataCount += 1
print ("Final Population:")
for each in leaderboard:
    for word in each.getWords():
        print (word.getWord(), end=" ")
    print ("Score", each.getTotalScore())