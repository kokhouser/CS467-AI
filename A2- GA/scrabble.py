import itertools
import operator
import time
import copy
from random import randint

scores = {'e': 1, 'a':1, 'i':1,'o':1,'n':1,'r':1,'t':1,'l':1,'s':1,'u':1,'d':2,'g':2,'b':3,'c':3,'m':3,'p':3,'f':4,'h':4,'v':4,'w':4,'y':4,'k':5,'j':8,'x':8,'q':10,'z':10}

class Attempt:
	def __init__(self):
		self.words = []
		self.used =  []
		self.unused = []
		self.totalScore = 0

	def getWords(self):
		return self.words

	def addToWords(self, inWord):
		self.words.append(inWord)
		for char in inWord:
			self.unused.remove(char)
			self.used.append(char)

	def getUsed(self):
		return self.used

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
			unusedWords = []
			for char in self.unused:
				unusedWords.append(char)
			while randLength > 0:
				usedIndex = randint(0,len(unusedWords)-1) #if len(unusedWords) > 0 else 0
				newWord += unusedWords[usedIndex]
				del(unusedWords[usedIndex])
				randLength -= 1
			self.addToWords(newWord.lower())
		if len(self.unused)>0:
			self.addToWords(self.unused)
		#print (self.words)

	def calculateScore(self):
		for each in self.words:
			if each in legal:
				#if len(each) > 3:
				#	print ("Long: ", each)
				for char in each:
					self.totalScore+=scores[char]

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
leaderboard.sort(key=lambda x: x.getTotalScore(), reverse=True)
for each in leaderboard:
	if each.getTotalScore() > 15:
		print ("Words:" , each.getWords())
	print ("Score:", each.getTotalScore())


'''
start_time = float(time.time())
print ()
for size in range (2,8):
	for each in itertools.permutations(guess,size):
	    temp = ""
	    score = 0
	    for item in each:
		    if item in scores:
			    score += scores[item]
		    temp += item
	    if temp.lower() in legal:
		    #print (temp, end = "")
		    #print (", Scrabble score=",score)
		    words[temp]=score
print ("Lists of words, ordered by Scrabble score:")
sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse = True)
for item in sorted_words:
    print (item)
print ()
print("--- seconds ---", time.time() - start_time)
'''

