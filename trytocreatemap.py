# Copied from: http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random 
from pokemonclass import Pokemon
from movesSpritesClass import MovesSprites
from levelmoves import addMoves
from playerclass import Player
from mazebacktracking import BacktrackingPuzzleSolver,State,MazeSolver,MazeState
import csv

testPlayer = Player(100,1)
username = 'Mary'


hi = dict()

invenDict = dict()

with open('test.csv', mode = 'r') as csvfile:
    csvReader = csv.reader(csvfile)
    next(csvReader, None)
    for row in csvReader:
        invenRaw = row[5]
        invenStr = invenRaw.split(", ")
        invenStr[0], invenStr[-1] = invenStr[0][1:], invenStr[-1][:-1]
        invenDict['Master Ball'] = int(invenStr[0])
        invenDict['Poké Ball'] = int(invenStr[1])
        invenDict['Full Restore'] = int(invenStr[2])
        invenDict['Ultra Ball'] = int(invenStr[3])
        invenDict['Poison'] = int(invenStr[4])
        invenDict['Paralyze'] = int(invenStr[5])

        hi['inventory'] = invenDict
print(hi)





with open('PlayerProgress.csv', mode = 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['username','exp','level','chars','inventory'])
    inventoryAmount = [testPlayer.inventory['Master Ball'],
                       testPlayer.inventory['Poké Ball'],
                       testPlayer.inventory['Full Restore'],
                       testPlayer.inventory['Ultra Ball'],
                       testPlayer.inventory['Poison'],
                       testPlayer.inventory['Paralyze']]
    currentInfo = [username, testPlayer.exp,
                    testPlayer.level,
                    testPlayer.money,
                    testPlayer.charList,
                    inventoryAmount]
    writer.writerow(currentInfo)
