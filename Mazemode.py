# Copied from: http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random 
from pokemonclass import Pokemon
from movesSpritesClass import MovesSprites
from levelmoves import addMoves
from playerclass import Player
from mazebacktracking import BacktrackingPuzzleSolver, State, MazeSolver, MazeState
import csv

class MazeGameMode(Mode):
    player = Player(0,1)
    def appStarted(mode):
        mode.progressDict = dict()

        #mode.tree = Image.open('tree.png')
        #mode.path = Image.open('path.png')
        mode.mazeBoard = []
        mode.solution = []
        mode.createMap()
        
        mode.rows, mode.cols = 8, 12
        mode.cellWidth = mode.width/mode.cols
        mode.cellHeight = mode.height/mode.rows

        # Generate random wild pokemon on the map
        mode.wildPic = mode.app.loadImage('egg.png')
        mode.wildList = []
        mode.dropWildPokemon()

        mode.playerX, mode.playerY = mode.cellWidth//2, mode.cellHeight//2
        mode.right, mode.left, mode.up, mode.down = False, False, False, False

        mode.loadSprites()
        mode.username = 'hi'
        mode.newPlayer = True
        #mode.loadProgress()
    
    def dropWildPokemon(mode):
        availableCell = []
        for row in range(mode.rows):
            for col in range(mode.cols):
                if mode.mazeBoard[row][col] == 'lightgreen':
                    availableCell.append((row, col))

        for _ in range(4):
            dropIndex = random.randint(0, len(availableCell)-1)
            mode.wildList.append(availableCell[dropIndex])

    def meetOpponent(mode):
        # Check if the player is facing an opponent
        for (row,col) in mode.wildList:
            cx = mode.cellWidth//2 + col*mode.cellWidth
            cy = mode.cellHeight//2 + row*mode.cellHeight
            if (cx == mode.playerX) and (cy == mode.playerY):
                mode.app.battleMode = BattleMode()
                mode.app.setActiveMode(mode.app.battleMode)
                mode.wildList.remove((x,y))
                # mode.
                if len(mode.wildList) == 0:
                    mode.dropWildPokemon()

    def loadSprites(mode):
        # Codes modied from 
        # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#ioMethods

        # Load player's sprites for going in all four directions
        spriteUp = mode.app.loadImage('up.png')
        mode.spritesUp = [ ]
        for i in range(4):
            sprite = spriteUp.crop((64*i, 0, 64*(i+1), 64))
            mode.spritesUp.append(sprite)
        
        spriteDown = mode.app.loadImage('down.png')
        mode.spritesDown = [ ]
        for i in range(4):
            sprite = spriteDown.crop((64*i, 0, 64*(i+1), 64))
            mode.spritesDown.append(sprite)

        spriteLeft = mode.app.loadImage('left.png')
        mode.spritesLeft = [ ]
        for i in range(4):
            sprite = spriteLeft.crop((64*i, 0, 64*(i+1), 64))
            mode.spritesLeft.append(sprite)
        
        spriteRight = mode.app.loadImage('right.png')
        mode.spritesRight = [ ]
        for i in range(4):
            sprite = spriteRight.crop((64*i, 0, 64*(i+1), 64))
            mode.spritesRight.append(sprite)

        mode.spriteCounter = 0
        
    def playerPosOfCell(mode, playerX, playerY):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        gridWidth  = app.width - 2*app.margin
        gridHeight = app.height - 2*app.margin
        cellWidth  = gridWidth / app.cols
        cellHeight = gridHeight / app.rows

        row = int(playerY / mode.cellHeight)
        col = int(playerX / mode.cellWidth)

        return (row, col) 

    def createMap(mode):
        #colors = [mode.tree, mode.path]
        colors = ['lightgreen', 'forestgreen']
        solvable = False
        while solvable == False:
            mode.mazeBoard = [[random.choice(colors) for i in range(12)]
                               for i in range(8)]
            #mode.mazeBoard[0][0] = mode.path
            mode.mazeBoard[0][0] = 'lightgreen'
            (path, solution) = MazeSolver(mode.mazeBoard).solve(printReport=True)
            if solution != None:
                solvable = True
                mode.solution = path

    def timerFired(mode):
        mode.spriteCounter = ((1 + mode.spriteCounter) % len(mode.spritesUp))

    def movePlayer(mode, dx, dy):
        # Make sure that player doesn't go off the map horizontally
        if ((mode.playerX + dx) > mode.width) or ((mode.playerX + dx) < 0 ):
            pass
        else:
            mode.playerX += dx

        # Make sure that player doesn't go off the map vertically
        if ((mode.playerY + dy) < 0) or ((mode.playerY + dy) > mode.height):
            pass
        else:
            mode.playerY += dy

    def keyPressed(mode, event):
        if (event.key == "Left"):
            mode.movePlayer(-mode.cellWidth, 0)
            mode.left = True
            mode.up, mode.down, mode.right = False, False, False
        elif (event.key == "Right"):
            mode.movePlayer(+mode.cellWidth, 0)
            mode.right = True
            mode.up, mode.down, mode.left = False, False, False
        elif (event.key == 'Up'):
            mode.movePlayer(0, -mode.cellHeight)
            mode.up = True
            mode.down, mode.left, mode.right = False, False, False
        elif (event.key == 'Down'):
            mode.movePlayer(0, mode.cellHeight)
            mode.down = True
            mode.up, mode.left, mode.right = False, False, False
        
        elif (event.key == 's'):
            # Learnt and modified from
            # https://realpython.com/python-csv/#reading-csv-files-with-csv

            # This command saves user's progress under the username
            progressList = list()
            with open('PlayerProgress.csv', mode = 'r') as csvfile:
                csvReader = csv.reader(csvfile)
                next(csvReader, None)
                for row in csvReader:
                    if row[0] == mode.username:
                        mode.newPlayer = False
                        info = [row[0], mode.player.exp,
                                RegularGameMode.player.level,
                                RegularGameMode.player.charList]
                    else:
                        info = [row[0], row[1], row[2], row[3]]
                    progressList.append(info)
            
            with open('PlayerProgress.csv', mode = 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['username', 'exp', 'level', 'chars'])
                for person in progressList:
                    writer.writerow(person)
                if mode.newPlayer:
                    currentInfo = [mode.username, mode.player.exp,
                                   RegularGameMode.player.level,
                                   RegularGameMode.player.charList]
                    writer.writerow(currentInfo)

        mode.meetOpponent()

    def drawWildPokemon(mode, canvas):
        # Draw wild Pokemon
        for (row, col) in mode.wildList:
            x = mode.cellWidth//2 + col*mode.cellWidth
            y = mode.cellHeight//2 + row*mode.cellHeight
            canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.wildPic))


    def drawPlayer(mode, canvas):
        # Draw players with sprites based on the four directions
        cx, cy = mode.playerX, mode.playerY
        if ((mode.right == False) and (mode.left == False) and
            (mode.down == False) and (mode.up == False)):
            sprite = mode.spritesRight[mode.spriteCounter]
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.right == True:
            sprite = mode.spritesRight[mode.spriteCounter]
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.left == True:
            sprite = mode.spritesLeft[mode.spriteCounter]
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.up == True:
            sprite = mode.spritesUp[mode.spriteCounter]
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.down == True:
            sprite = mode.spritesDown[mode.spriteCounter]
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

    def drawMaze(mode, canvas):
        for row in range(mode.rows):
            for col in range(mode.cols):
                '''
                canvas.create_image(mode.cellWidth//2 + mode.cellWidth*col,
                                    mode.cellHeight//2 + mode.cellHeight*row,
                                    image=ImageTk.PhotoImage(mode.mazeBoard[row][col]))
                '''
                canvas.create_rectangle(col*mode.cellWidth, row*mode.cellHeight,
                                        (col+1)*mode.cellWidth,
                                        (row+1)*mode.cellHeight,
                                        fill = mode.mazeBoard[row][col])
                

    def redrawAll(mode, canvas):
        mode.drawMaze(canvas)
        mode.drawPlayer(canvas)
        mode.drawWildPokemon(canvas)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.regularGameMode = RegularGameMode()
        app.mazeGameMode = MazeGameMode()
        app.helpMode = HelpMode()
        app.battleMode = BattleMode()
        app.setActiveMode(app.mazeGameMode)
        app.timerDelay = 50

app = MyModalApp(width=600, height=400)