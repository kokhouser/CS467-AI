import itertools
import operator
import time

f = open("words.txt","r")
str1 = f.read().lower()
f.close

legal = {}
temp = str1.split(" ")
for each in temp:
    legal[each]=""

scores = {'e': 1, 'a':1, 'i':1,'o':1,'n':1,'r':1,'t':1,'l':1,'s':1,'u':1,'d':2,'g':2,'b':3,'c':3,'m':3,'p':3,'f':4,'h':4,'v':4,'w':4,'y':4,'k':5,'j':8,'x':8,'q':10,'z':10}
words = {}

guess = input("Enter some letters: ")
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