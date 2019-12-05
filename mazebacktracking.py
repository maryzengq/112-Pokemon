# This is the backtracking class that helps me generate randomized maze maps
# that are solvable

# Copied from: http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random
import csv

# Copied from:
# http://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#genericBacktrackingSolver
import copy, time

class BacktrackingPuzzleSolver(object):
    def solve(self, checkConstraints=True, printReport=False):
        self.moves = [ ]
        self.states = set()
        # If checkConstraints is False, then do not check the backtracking
        # constraints as we go (so instead do an exhaustive search)
        self.checkConstraints = checkConstraints
        # Be sure to set self.startArgs and self.startState in __init__
        self.startTime = time.time()
        self.solutionState = self.solveFromState(self.startState)
        self.endTime = time.time()
        if (printReport): self.printReport()
        return (self.moves, self.solutionState)

    def printReport(self):
        print()
        print('***********************************')
        argsStr = str(self.startArgs).replace(',)',')') # remove singleton comma
        print(f'Report for {self.__class__.__name__}{argsStr}')
        print('checkConstraints:', self.checkConstraints)
        print('Moves:', self.moves)
        print('Solution state: ', end='')
        if ('\n' in str(self.solutionState)): print()
        print(self.solutionState)
        print('------------')
        print('Total states:', len(self.states))
        print('Total moves: ', len(self.moves))
        millis = int((self.endTime - self.startTime)*1000)
        print('Total time:  ', millis, 'ms')
        print('***********************************')

    def solveFromState(self, state):
        if state in self.states:
            # we have already seen this state, so skip it
            return None
        self.states.add(state)
        if self.isSolutionState(state):
            # we found a solution, so return it!
            return state
        else:
            for move in self.getLegalMoves(state):
                # 1. Apply the move
                childState = self.doMove(state, move)
                # 2. Verify the move satisfies the backtracking constraints
                #    (only proceed if so)
                if ((self.stateSatisfiesConstraints(childState)) or
                    (not self.checkConstraints)):
                    # 3. Add the move to our solution path (self.moves)
                    self.moves.append(move)
                    # 4. Try to recursively solve from this new state
                    result = self.solveFromState(childState)
                    # 5. If we solved it, then return the solution!
                    if result != None:
                        #print('result:', result)
                        return result
                    # 6. Else we did not solve it, so backtrack and
                    #    remove the move from the solution path (self.moves)
                    self.moves.pop()
            return None

    # You have to implement these:

    def __init__(self):
        # Be sure to set self.startArgs and self.startState here
        pass

    def stateSatisfiesConstraints(self, state):
        # return True if the state satisfies the solution constraints so far
        raise NotImplementedError

    def isSolutionState(self, state):
        # return True if the state is a solution
        raise NotImplementedError

    def getLegalMoves(self, state):
        # return a list of the legal moves from this state (but not
        # taking the solution constraints into account)
        raise NotImplementedError

    def doMove(self, state, move):
        # return a new state that results from applying the given
        # move to the given state
        raise NotImplementedError

class State(object):
    def __eq__(self, other): return (other != None) and self.__dict__ == other.__dict__
    def __hash__(self): return hash(str(self.__dict__)) # hack but works even with lists
    def __repr__(self): return str(self.__dict__)


class MazeState(State):
    def __init__(self, solutionPath):
        self.solutionPath = solutionPath


class MazeSolver(BacktrackingPuzzleSolver):
    def __init__(self, board):
        self.board = board
        self.startArgs = (board, )
        self.startState = MazeState([(0,0)])

    def isSolutionState(self, state):
        if len(state.solutionPath) < ((len(self.board)-1)*2):
            return False
        if state.solutionPath[-1] != (len(self.board)-1, len(self.board[0])-1):
            return False
        return True
        
    def getLegalMoves(self, state):
        dirs = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
        moves = []
        for drow, dcol in dirs:
            (row, col) = state.solutionPath[-1]
            nrow = row + drow
            ncol = col + dcol
            moves.append((nrow, ncol))
        return moves
    
    def doMove(self, state, move):
        newSolutionPath = state.solutionPath + [move]
        return MazeState(newSolutionPath)

    def stateSatisfiesConstraints(self, state):
        row, col = state.solutionPath[-1]
        if ((row < 0) or (row >= len(self.board)) or
            (col < 0) or (col >= len(self.board[0])) or
            ((row, col) in state.solutionPath[:-1])):
            return False
        else:
            if self.board[row][col] == 'lightgreen':
                return True

