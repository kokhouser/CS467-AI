import sys
import random
import copy

class Gamestate:
    
    def __init__(self, oldState = None):
        self.state = []
        if (oldState is None):
            self.state = ["_", "_", "_", "_", "_", "_","_", "_", "_"]
            self.chancesX = [100, 100, 100, 100, 100, 100, 100, 100, 100]
            self.chancesO = [100, 100, 100, 100, 100, 100, 100, 100, 100]
        else:
            for symbol  in oldState.state:
                self.state.append(symbol)
            self.chancesX = []
            self.chancesO = []
            for chance in oldState.chancesX:
                self.chancesX.append(chance)
            for chance in oldState.chancesO:
                self.chancesO.append(chance)
    
    def isEqual(self, inList):
        if (inList == self.state):
            return True
        else:
            return False
    
    def suggestMove(self, currentSymbol):
        chance = random.randint(0,890)
        counter = 0
        if currentSymbol == "X":
            for x, chanceX in enumerate(self.chancesX):
                counter += self.chancesX[x]
                if counter >= chance:
                    return x
        else:
            for x, chanceO in enumerate(self.chancesO):
                counter += self.chancesO[x]
                if counter >= chance:
                    return x
        
    def isGameOver(self):
        if (self.state[0] != "_" and self.state[0] == self.state[1] and self.state[0] == self.state [2]):
            return self.state[0]
        elif (self.state[0] != "_" and self.state[0] == self.state[3] and self.state[0] == self.state [6]):
            return self.state[0]
        elif (self.state[0] != "_" and self.state[0] == self.state[4] and self.state[0] == self.state [8]):
            return self.state[0]
        elif (self.state[1] != "_" and self.state[1] == self.state[4] and self.state[1] == self.state [7]):
            return self.state[1]
        elif (self.state[2] != "_" and self.state[2] == self.state[5] and self.state[2] == self.state [8]):
            return self.state[2]
        elif (self.state[2] != "_" and self.state[2] == self.state[4] and self.state[2] == self.state [6]):
            return self.state[2]
        elif (self.state[3] != "_" and self.state[3] == self.state[4] and self.state[3] == self.state [5]):
            return self.state[3]
        elif (self.state[6] != "_" and self.state[6] == self.state[7] and self.state[6] == self.state [8]):
            return self.state[6]
        else:
            full = True
            for symbol in self.state:
                if symbol == "_":
                    full = False
            if full:
                return -2
            else:
                return -1

class Statelog:
    
    def __init__(self):
        self.states=[]
    
    def makeMove(self, prevState, movePos, symbol):
        newList = copy.deepcopy(prevState.state)
        newList[movePos] = symbol
        isNew = True
        currentState = 0
        for state in self.states:
            if (state.isEqual(newList)):
                isNew = False
                currentState = state
        if (isNew):
            newState = Gamestate()
            newState.state = newList
            count = 9
            for thing in newState.state:
                if thing != "_":
                    count -= 1
            for x,chance in enumerate(newState.chancesX):
                if newState.state[x] == "_":
                    newState.chancesX[x] = 900//count
                else:
                    newState.chancesX[x] = 0
            for x,chance in enumerate(newState.chancesO):
                if newState.state[x] == "_":
                    newState.chancesO[x] = 900//count
                else:
                    newState.chancesO[x] = 0
            self.states.append(newState)
            return newState
        else:
            return currentState
        

state = Gamestate()
states = Statelog()
states.states.append(state)
winX = 0
winO = 0
draws = 0
for i in range (0,100):
    currentSymbol = "X"
    currentState = states.states[0]
    movesX = {}
    movesY = {}
    while True:
        nextMove = currentState.suggestMove(currentSymbol)
        if currentSymbol == "X":
            movesX[currentState] = nextMove
        else:
            movesY[currentState] = nextMove
        currentState = states.makeMove(currentState,nextMove,currentSymbol)
        if (currentState.isGameOver() != -1):
            break
        elif currentSymbol == "X":
            currentSymbol = "O"
        else:
            currentSymbol = "X"
    '''
    for x,symbol in enumerate(currentState.state):
        if (x%3 == 0):
            print ()
        print (symbol, end="")
    print ()
    '''
    if (currentState.isGameOver() == "X"):
        print ("X won!")
        winX += 1
                    
    elif (currentState.isGameOver() == "O"):
        print ("O won!")
        winO += 1
        
    elif (currentState.isGameOver() == -2):
        print ("Draw!")
        draws += 1

print ("X has won",winX,"times.")
print ("O has won",winO,"times.")
print ("Draws occured",draws,"times.")