import sys
import random
import copy

class Gamestate:
    
    def __init__(self, oldState = None):
        self.state = ["_", "_", "_", "_", "_", "_","_", "_", "_"]
        if (oldState is None):
            self.chancesX = [1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9]
            self.chancesY = [1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9,1/9]
        else:
            self.chancesX = []
            self.chancesY = []
            for chance in oldState.chancesX:
                self.chancesX.append(chance)
            for chance in oldState.chancesY:
                self.chancesY.append(chance)
    
    def isEqual(self, inList):
        if (inList == self.state):
            return True
        else:
            return False
        
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
            return -1

class Statelog:
    
    def __init__(self):
        self.states=[]
    
    def makeMove(self, prevState, movePos, symbol):
        newList = copy.deepcopy(prevState.state)
        newList[movePos] = symbol
        isNew = True
        for state in self.states:
            if (state.isEqual(newList)):
                isNew = False
        if (isNew):
            newState = Gamestate(prevState)
            newState.state[movePos] = symbol
            count = 9
            for thing in newState.state:
                if thing != "_":
                    count -= 1
            for x,chance in enumerate(newState.chancesX):
                if newState.state[x] == "_":
                    newState.chancesX[x] = 1/count
                else:
                    newState.chancesX[x] = 0
            for x,chance in enumerate(newState.chancesY):
                newState.chancesY[x] = 1/count
            self.states.append(newState)
        

state = Gamestate()
states = Statelog()
states.states.append(state)
states.makeMove(state,1,"X")
print (states.states[1].chancesX)
    
