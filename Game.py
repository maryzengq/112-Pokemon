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

# All the color codes are from https://uicolorpicker.com/
        

class SplashScreenMode(Mode):
    def appStarted(mode):
        mode.startpic = mode.app.loadImage('splash.jpg')
        mode.colorWhenMoveRegular = '#26ae60'
        mode.colorWhenMoveMaze = '#26ae60'

    def mousePressed(mode, event):
        if (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (175 < event.y < 205)):
            mode.app.setActiveMode(mode.app.regularGameMode)
        elif (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (235 < event.y < 265)):
            mode.app.setActiveMode(mode.app.mazeStart)

    def mouseMoved(mode, event):
        if (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (175 < event.y < 205)):
            mode.colorWhenMoveRegular = "#218F76"
        elif (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (235 < event.y < 265)):
            mode.colorWhenMoveMaze = "#218F76"
        else:
            mode.colorWhenMoveRegular = '#26ae60'
            mode.colorWhenMoveMaze = '#26ae60'


    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,
                            image=ImageTk.PhotoImage(mode.startpic))
        
        # Draw game name
        canvas.create_text(mode.width/2, 120, text = 'The Pokémon Game',
                           fill = '#EAF0F1', font = 'Georgia 40 bold')
        
        # Draw regular mode
        canvas.create_rectangle(mode.width/2-100, 175, mode.width/2+100, 205,
                                fill = mode.colorWhenMoveRegular, outline = '#10A881')
        canvas.create_text(mode.width/2, 190,
                           text='Regular Mode', fill = '#EAF0F1',
                           font='Georgia 20')
        
        # Draw maze mode
        canvas.create_rectangle(mode.width/2-100, 235, mode.width/2+100, 265,
                                fill = mode.colorWhenMoveMaze, outline = '#10A881')
        canvas.create_text(mode.width/2, 250,
                           text='Maze Mode', fill = '#EAF0F1',
                           font='Georgia 20')

        # Draw reminder for progress
        canvas.create_rectangle(mode.width/2 - 180, mode.height - 80,
                                mode.width/2 + 180, mode.height - 30,
                                fill = '#DAE0E2')
        canvas.create_text(mode.width/2, mode.height-65,
                           text =("Dont forget "
                                  "to press 's' to save your progress"),
                           font = 'Georgia 16')
        canvas.create_text(mode.width/2, mode.height-45,
                           text =("Use the same username "
                                  "to load your progress."),
                           font = 'Georgia 16')

class RegularGameMode(Mode):
    player = Player(0, 1)
    def appStarted(mode):
        mode.progressDict = dict()
        mode.startpic = mode.app.loadImage('gamemap.png')
        mode.scalePic = mode.app.scaleImage(mode.startpic, 3)
        mode.mapWidth, mode.mapHeight = mode.scalePic.size
        mode.store = mode.app.loadImage('store.png')
        mode.bag = mode.app.loadImage('bag.png')
        mode.storeItem = mode.app.loadImage('storeitems.png')
        mode.inventory = mode.app.loadImage('inventory.png')

        mode.scrollX, mode.scrollY = 0, 0
        mode.scrollMargin = 120
        mode.playerX, mode.playerY = mode.width/2, mode.height/2
        mode.r = 10

        mode.backButton = '#DAE0E2'
    
        mode.mapLeftEnd = mode.width//2 - mode.mapWidth//2
        mode.mapRightEnd = mode.width//2 + mode.mapWidth//2
        mode.mapTopEnd = mode.height//2 - mode.mapHeight//2
        mode.mapDownEnd = mode.height//2 + mode.mapHeight//2

        # Store player position relatively to the map
        mode.mapPlayerX = mode.mapLeftEnd + mode.mapWidth/2
        mode.mapPlayerY = mode.mapTopEnd + mode.mapHeight/2
        
        # Generate random wild pokemon on the map
        mode.wildPic = mode.app.loadImage('egg.png')
        mode.wildList = []
        mode.dropWildPokemon()

        mode.right, mode.left, mode.up, mode.down = False, False, False, False
        mode.loadSprites()

        mode.username = 'hi'
        mode.newPlayer = True

        mode.storeFunction = False
        mode.broke = False
        mode.notEnoughMoney = False
        mode.checkInventory = False

        mode.loadProgress()

          
    def loadProgress(mode):
        # Learnt and modified from
        # https://realpython.com/python-csv/#reading-csv-files-with-csv
        charSet = set()
        invenDict = dict()

        with open('PlayerProgress.csv', mode = 'r') as csvfile:
            csvReader = csv.reader(csvfile)
            next(csvReader, None)
            for row in csvReader:
                charRaw = row[4]
                charStr = charRaw.split(", ")
                charStr[0], charStr[-1] = charStr[0][1:], charStr[-1][:-1]
                for char in charStr:
                    char = char.strip(" '")
                    charSet.add(char)

                invenRaw = row[5]
                invenStr = invenRaw.split(", ")
                invenStr[0], invenStr[-1] = invenStr[0][1:], invenStr[-1][:-1]
                invenDict['Master Ball'] = int(invenStr[0])
                invenDict['Poké Ball'] = int(invenStr[1])
                invenDict['Full Restore'] = int(invenStr[2])
                invenDict['Ultra Ball'] = int(invenStr[3])
                invenDict['Poison'] = int(invenStr[4])
                invenDict['Great Ball'] = int(invenStr[5])

                mode.progressDict[row[0]] = {'exp': int(row[1]),
                                             'level': int(row[2]),
                                             'money': int(row[3]),
                                             'characters': charSet,
                                             'inventory': invenDict}

        print(mode.progressDict)

        mode.username = mode.getUserInput('What is your username').title()

        for key in mode.progressDict.keys():
            if mode.username == key:
                RegularGameMode.player = Player(mode.progressDict[key]['exp'],
                                         mode.progressDict[key]['level'],
                                         mode.progressDict[key]['money'],
                                         charSet, invenDict)
                    
        return mode.progressDict

    def dropWildPokemon(mode):
        # Drop random, wild pokemon
        for i in range(10):
            wildX = random.randint(mode.mapLeftEnd+100 + mode.scrollMargin,
                                   mode.mapRightEnd - mode.scrollMargin)
            wildY = random.randint(mode.mapTopEnd + mode.scrollMargin,
                                   mode.mapDownEnd - mode.scrollMargin)
            mode.wildList.append((wildX, wildY))
        
  
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
    
    def makePlayerVisible(mode):
        # Codes modied from 
        # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
        
        # scroll to make player visible as needed
        if (mode.playerX < mode.scrollX + mode.scrollMargin):
            mode.scrollX = mode.playerX - mode.scrollMargin
        if (mode.playerX > mode.scrollX + mode.width - mode.scrollMargin):
            mode.scrollX = mode.playerX - mode.width + mode.scrollMargin

        if (mode.playerY < mode.scrollY + mode.scrollMargin):
            mode.scrollY = mode.playerY - mode.scrollMargin
        if (mode.playerY > + mode.scrollY + mode.height - mode.scrollMargin):
            mode.scrollY = mode.playerY - mode.height + mode.scrollMargin 

    def movePlayer(mode, dx, dy):
        mapRightEnd = mode.width//2 + mode.mapWidth//2
        mapLeftEnd = mode.width//2 - mode.mapWidth//2
        mapTopEnd = mode.height//2 - mode.mapHeight//2
        mapDownEnd = mode.height//2 + mode.mapHeight//2

        # Make sure that player doesn't go off the map horizontally
        if mode.playerX + dx > mapRightEnd - mode.scrollMargin:
            pass
        elif mode.playerX + dx < mapLeftEnd + mode.scrollMargin:
            pass
        else:
            mode.playerX += dx

        # Make sure that player doesn't go off the map vertically
        if mode.playerY + dy < mapTopEnd + mode.scrollMargin:
            pass
        elif mode.playerY + dy > mapDownEnd - mode.scrollMargin:
            pass
        else:
            mode.playerY += dy
        
        mode.makePlayerVisible()

    
    def meetOpponent(mode, cx, cy):
        # Check if the player is facing an opponent
        for (x,y) in mode.wildList:
            if (((x - 20) <= cx <= (x + 20)) and
                ((y - 20) <= cy <= (y + 20))):
                mode.app.battleMode = BattleMode()
                mode.app.setActiveMode(mode.app.battleMode)
                mode.wildList.remove((x,y))
                # mode.
                if len(mode.wildList) == 0:
                    mode.dropWildPokemon()

    def timerFired(mode):
        mode.spriteCounter = ((1 + mode.spriteCounter) % len(mode.spritesUp))

    def keyPressed(mode, event):
        if (event.key == "Left"):
            mode.movePlayer(-10, 0)
            mode.mapPlayerX -= 10
            mode.left = True
            mode.up, mode.down, mode.right = False, False, False
        elif (event.key == "Right"):
            mode.movePlayer(+10, 0)
            mode.mapPlayerX += 10
            mode.right = True
            mode.up, mode.down, mode.left = False, False, False
        elif (event.key == 'Up'):
            mode.movePlayer(0, - 10)
            mode.mapPlayerY -= 10
            mode.up = True
            mode.down, mode.left, mode.right = False, False, False
        elif (event.key == 'Down'):
            mode.movePlayer(0, +10)
            mode.mapPlayerY += 10
            mode.down = True
            mode.up, mode.left, mode.right = False, False, False
        elif (event.key == 'Space'):
            if mode.broke:
                mode.storeFunction = False
            if mode.notEnoughMoney:
                mode.notEnoughMoney = False
        
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
                        inventoryAmount = [RegularGameMode.player.inventory['Master Ball'],
                                    RegularGameMode.player.inventory['Poké Ball'],
                                    RegularGameMode.player.inventory['Full Restore'],
                                    RegularGameMode.player.inventory['Ultra Ball'],
                                    RegularGameMode.player.inventory['Poison'],
                                    RegularGameMode.player.inventory['Great Ball']]
                        info = [row[0], mode.player.exp,
                                RegularGameMode.player.level,
                                RegularGameMode.player.money,
                                RegularGameMode.player.charList,
                                inventoryAmount]
                    else:
                        info = [row[0], row[1], row[2], row[3], row[4], row[5]]
                    progressList.append(info)

            with open('PlayerProgress.csv', mode = 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['username','exp','level','chars','inventory'])
                for person in progressList:
                    writer.writerow(person)
                if mode.newPlayer:
                    inventoryAmount = [RegularGameMode.player.inventory['Master Ball'],
                                    RegularGameMode.player.inventory['Poké Ball'],
                                    RegularGameMode.player.inventory['Full Restore'],
                                    RegularGameMode.player.inventory['Ultra Ball'],
                                    RegularGameMode.player.inventory['Poison'],
                                    RegularGameMode.player.inventory['Great Ball']]
                    currentInfo = [mode.username, RegularGameMode.player.exp,
                                    RegularGameMode.player.level,
                                    RegularGameMode.player.money,
                                    RegularGameMode.player.charList,
                                    inventoryAmount]
                    writer.writerow(currentInfo)
            
        mode.meetOpponent(mode.mapPlayerX, mode.mapPlayerY)

    def checkBalance(mode):
        if RegularGameMode.player.money <= 0:
            mode.broke = True

    def mousePressed(mode, event):
        mode.checkBalance()
        if (10 < event.x < 70) and (350 < event.y < 380):
            if mode.storeFunction:
                mode.storeFunction = False
            elif mode.checkInventory:
                mode.checkInventory = False
            else:
                mode.app.setActiveMode(mode.app.splashScreenMode)
        elif (16 < event.x < 64) and (199 < event.y < 241):
            mode.storeFunction = True
        elif (16 < event.x < 64) and (99 < event.y < 158):
            mode.checkInventory = True
        
        # Enable all the clicks when store is drawn
        if mode.storeFunction:
            if (10 < event.x < 190) and (70 < event.y < 180):
                if RegularGameMode.player.money - 100 > 0:
                    RegularGameMode.player.inventory['Master Ball'] = RegularGameMode.player.inventory.get('Master Ball', 0) + 1
                    RegularGameMode.player.money -= 100
                else: mode.notEnoughMoney = True

            elif (210 < event.x < 390) and (70 < event.y < 180):
                if RegularGameMode.player.money - 200 > 0:
                    RegularGameMode.player.inventory['Full Restore'] = RegularGameMode.player.inventory.get('Full Restore', 0) + 1
                    RegularGameMode.player.money -= 200
                else: mode.notEnoughMoney = True

            elif (410 < event.x < 590) and (70 < event.y < 180):
                if RegularGameMode.player.money - 250 > 0:
                    RegularGameMode.player.inventory['Poison'] = RegularGameMode.player.inventory.get('Poison', 0) + 1
                    RegularGameMode.player.money -= 250
                else:mode.notEnoughMoney = True
            
            elif (10 < event.x < 190) and (220 < event.y < 325):
                if RegularGameMode.player.money - 50 > 0:
                    RegularGameMode.player.inventory['Poké Ball'] = RegularGameMode.player.inventory.get('Poké Ball', 0) + 1
                    RegularGameMode.player.money -= 50
                else: mode.notEnoughMoney = True
            
            elif (210 < event.x < 390) and (220 < event.y < 325):
                if RegularGameMode.player.money - 70 > 0:
                    RegularGameMode.player.inventory['Ultra Ball'] = RegularGameMode.player.inventory.get('Ultra Ball', 0) + 1
                    RegularGameMode.player.money -= 70
                else: mode.notEnoughMoney = True
            
            elif (410 < event.x < 590) and (220 < event.y < 325):
                if RegularGameMode.player.money - 250 > 0:
                    RegularGameMode.player.inventory['Great Ball'] = RegularGameMode.player.inventory.get('Great Ball', 0) + 1
                    RegularGameMode.player.money -= 250
                else: mode.notEnoughMoney = True

    def drawInventory(mode, canvas):
        if mode.checkInventory:
            canvas.create_image(300,200, image=ImageTk.PhotoImage(mode.inventory))
            #draw number of items owned
            canvas.create_text(32, 120,
                text=RegularGameMode.player.inventory['Master Ball'],
                font='Courier 20 bold')
            canvas.create_text(232, 120,
                text=RegularGameMode.player.inventory['Full Restore'],
                font='Courier 20 bold')
            canvas.create_text(432, 120,
                text=RegularGameMode.player.inventory['Poison'],
                font='Courier 20 bold')
            canvas.create_text(32, 275,
                text=RegularGameMode.player.inventory['Poké Ball'],
                font='Courier 20 bold')
            canvas.create_text(232, 275,
                text=RegularGameMode.player.inventory['Ultra Ball'],
                font='Courier 20 bold')
            canvas.create_text(432, 275,
                text=RegularGameMode.player.inventory['Great Ball'],
                font='Courier 20 bold')
            canvas.create_text(316, 365,
                               text=RegularGameMode.player.money,
                               font='Courier 18 bold')


    def drawStoreItems(mode, canvas):
        if mode.storeFunction:
            canvas.create_image(300, 200, image=ImageTk.PhotoImage(mode.storeItem))
            canvas.create_text(313, 372,
                               text=RegularGameMode.player.money,
                               font='Courier 18')

            mode.drawItemsOwned(canvas)
            mode.drawBroke(canvas)
            mode.drawNotEnoughMoney(canvas)

    def drawItemsOwned(mode, canvas):        
        #draw number of items owned
        canvas.create_text(143, 187,
            text=RegularGameMode.player.inventory['Master Ball'],
            font='Courier 14')
        canvas.create_text(343, 187,
            text=RegularGameMode.player.inventory['Full Restore'],
            font='Courier 14')
        canvas.create_text(543, 187,
            text=RegularGameMode.player.inventory['Poison'],
            font='Courier 14')
        canvas.create_text(143, 337,
            text=RegularGameMode.player.inventory['Poké Ball'],
            font='Courier 14')
        canvas.create_text(343, 337,
            text=RegularGameMode.player.inventory['Ultra Ball'],
            font='Courier 14')
        canvas.create_text(543, 337,
            text=RegularGameMode.player.inventory['Great Ball'],
            font='Courier 14')

    def drawBroke(mode, canvas):
        if mode.broke:
            canvas.create_rectangle(0,100,600,300, fill = 'white')
            canvas.create_text(300,150, text="YOU ARE BROKE!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,200, text="CAN'T BUY ANYTHING!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,250, text="Press 'Space' to go back",
                               font = 'Courier 22')
    
    def drawNotEnoughMoney(mode, canvas):
        if mode.notEnoughMoney:
            canvas.create_rectangle(0,100,600,300, fill = 'white')
            canvas.create_text(300,150, text="YOU DON'T HAVE ENOUGH MONEY!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,200, text="CAN'T BUY IT!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,250, text="Press 'Space' to go back",
                               font = 'Courier 22')
                

    def drawPlayer(mode, canvas):
        # Draw players with sprites based on the four directions
        if ((mode.right == False) and (mode.left == False) and
            (mode.down == False) and (mode.up == False)):
            sprite = mode.spritesRight[mode.spriteCounter]
            cx, cy = mode.playerX, mode.playerY
            cx -= mode.scrollX
            cy -= mode.scrollY
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.right == True:
            sprite = mode.spritesRight[mode.spriteCounter]
            cx, cy = mode.playerX, mode.playerY
            cx -= mode.scrollX
            cy -= mode.scrollY
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.left == True:
            sprite = mode.spritesLeft[mode.spriteCounter]
            cx, cy = mode.playerX, mode.playerY
            cx -= mode.scrollX
            cy -= mode.scrollY
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.up == True:
            sprite = mode.spritesUp[mode.spriteCounter]
            cx, cy = mode.playerX, mode.playerY
            cx -= mode.scrollX
            cy -= mode.scrollY
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
        elif mode.down == True:
            sprite = mode.spritesDown[mode.spriteCounter]
            cx, cy = mode.playerX, mode.playerY
            cx -= mode.scrollX
            cy -= mode.scrollY
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

    def redrawAll(mode, canvas):
        # Draw the map
        canvas.create_image(mode.width/2 - mode.scrollX,
                            mode.height/2 - mode.scrollY,
                            image=ImageTk.PhotoImage(mode.scalePic))
        # Draw the player
        mode.drawPlayer(canvas)

        # Draw the compPkm, shifted by the scrollX offset
        for (x, y) in mode.wildList:
            x -= mode.scrollX  
            y -= mode.scrollY
            canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.wildPic))
        
        # Draw functionality column 
        canvas.create_rectangle(0, 0, 80, 400, fill = '#7CEC9F',
                                outline = '#10A881', width = 2)
        canvas.create_text(40, 40, text = 'Menu', fill = '#218F76',
                           font = 'Georgia 20 bold')
        
        # Draw 'Bag' button
        canvas.create_text(40, 90, text = 'My Bag', fill = '#019031',
                           font = 'Georgia 16')
        canvas.create_image(40, 130, image=ImageTk.PhotoImage(mode.bag))

        # Draw 'store'
        canvas.create_text(40, 185, text = 'Store', fill = '#019031',
                           font = 'Georgia 16')
        canvas.create_image(40, 220, image=ImageTk.PhotoImage(mode.store))
        
        # Draw storeitems
        mode.drawStoreItems(canvas)

        # Draw inventory
        mode.drawInventory(canvas)

        # Draw 'Back' button
        canvas.create_rectangle(10, 350, 70, 380, fill = mode.backButton)
        canvas.create_text(40, 365, text = 'Back', fill = '#333945',
                           font = 'Georgia 22')


class BattleMode(Mode):
    def appStarted(mode):
        # Load all the inventory items
        mode.loadImages()

        # Initiate the player and computer pokémon
        mode.player = RegularGameMode.player
        mode.playerPKM = Pokemon('Squirtle', mode.player.level, mode)
        mode.compPKM = Pokemon('Squirtle', mode.player.level, mode)

        mode.playerTurn = False
        mode.battleOver = False

        # Initialize all the necesary booleans
        mode.playerMove = MovesSprites('Nuzzle', mode)
        mode.playerDoneMoving = False
        mode.playerDone = False
        mode.drawPlayerMove = False
        mode.displayPlayerDamage = False
        mode.actuallyRunPlayerMove = False
        mode.damageOnPlayer = 0

        mode.compMove = MovesSprites('Nuzzle', mode)
        mode.compDoneMoving = False
        mode.compDone = False
        mode.drawCompMove = False
        mode.displayCompDamage = False
        mode.actuallyRunCompMove = False
        mode.damageOnComp = 0

        mode.drawWinner = False
        mode.winnter = 'no one'
        mode.decideWinnter = True

        mode.displayCheatMove = False
        mode.cheatMove = ('hi', 0)
        mode.pause = False
        mode.drawCompPKM = True

        mode.useInven = False
        mode.notEnoughItems = False
        mode.itemUsed = 'start'
        mode.itemIcon = mode.bag

        mode.purchase = False
        mode.broke = False
        mode.notEnoughMoney = False

        mode.drawPlayerPKM = False
        mode.successfulCapture = False

        mode.drawPlayerItem = False
        mode.playerItemX, mode.playerItemY = 225, 340

        mode.initiatePokemon()
    
    def loadImages(mode):
        mode.pic = mode.app.loadImage('bi.png')
        mode.scalePic = mode.app.scaleImage(mode.pic, 4/3)
        mode.bag = mode.app.loadImage('bag.png')
        mode.storeIcon = mode.app.loadImage('store.png')
        mode.inventory = mode.app.loadImage('battleInven.png')
        mode.store = mode.app.loadImage('battleStore.png')

        mode.masterBall = mode.app.loadImage('masterball.png')
        mode.fullRestore = mode.app.loadImage('fullrestore.png')
        mode.greatBall = mode.app.loadImage('greatball.png')
        mode.poison = mode.app.loadImage('poison.png')
        mode.pokeBall = mode.app.loadImage('pokeball.png')
        mode.ultraBall = mode.app.loadImage('ultraball.png')

    def moveEffective(mode, computer, player):
        # Got Pokemon info from https://pokemondb.net/pokedex/squirtle

        # Return a dictionary of moves and their effectiveness (0.5, 1, 2)
        movesDict = {
        'Nuzzle': {'name': 'Nuzzle', 'power': 20, 'type': 'Electric', 
                'effective': ["Water", "Flying"], 
                'not effective': ["Electric", "Grass", "Dragon"]},
        'Quick Attack': {'name': 'Quick Attack', 'power': 40, 'type': 'Normal', 
                        'effective': ["N/A"], 
                        'not effective': ["Rock", "Steel"]},
        'Thunder Shock': {'name': 'Thunder Shock', 'power': 40, 'type': 'Electric',
                        'effective': ['Water', 'Flying'],
                        'not effective': ['Electric', 'Grass',
                        'Dragon']}, 
        'Spark': {'name': 'Spark', 'power': 65, 'type': 'Electric',
                'effective': ['Water', 'Flying'],
                'not effective': ['Electric', 'Grass',
                'Dragon']},
        'Slam': {'name': 'Slam', 'power': 80, 'type': 'Normal',
                'effective': ["N/A"], 
                'not effective': ["Rock", "Steel"]},
        'Ember': {'name': 'Ember', 'power': 40, 'type': 'Fire',
                'effective': ['Grass', 'Ice', 'Bug', 'Steel'],
                'not effective': ['Fire', 'Water', 'Rock',
                'Dragon']}, 
        'Scratch': {'name': 'Scratch', 'power': 40,'type': 'Normal',
                    'effective': ['N/A'],
                    'not effective': ['Rock', 'Steel']}, 
        'Air Slash': {'name': 'Air Slash', 'power': 75, 'type': 'Flying',
                    'effective': ["Grass", "Fighting", "Bug"],
                    'not effective': ["Electric", "Rock","Steel"]},
        'Slash': {'name': 'Slash', 'power': 70, 'type': 'Normal',
                'effective': ["N/A"], 
                'not effective': ["Rock", "Steel"]},
        'Flare Blitz': {'name': 'Flare Blitz', 'power': 120, 'type': 'Fire',
                        'effective': ['Grass', 'Ice', 'Bug', 'Steel'],
                        'not effective': ['Fire', 'Water', 'Rock',
                        'Dragon']},
        'Tackle': {'name': 'Tackle', 'power': 40, 'type': 'Normal', 
                'effective': ['N/A'], 
                'not effective': ['Rock', 'Steel']}, 
        'Water Gun': {'name': 'Water Gun', 'power': 40, 'type': 'Water', 
                    'effective': ["Fire", "Ground", "Rock"], 
                    'not effective': ["Water", "Grass", "Dragon"]},    
        'Bite': {'name': 'Bite', 'power': 60, 'type': 'Dark',
                'effective': ['Psychic', 'Ghost'],
                'not effective': ['Fighting', 'Dark', 'Fairy']}, 
        'Aqua Tail': {'name': 'Aqua Tail', 'power': 90, 'type': 'Water', 
                    'effective': ["Fire", "Ground", "Rock"], 
                    'not effective': ["Water", "Grass", "Dragon"]}, 
        'Skull Bash': {'name': 'Skull Bash', 'power': 130, 'type': 'Normal', 
                    'effective': ['N/A'], 
                    'not effective': ['Rock', 'Steel']},
        'Confusion': {'name': 'Confusion', 'power': 50, 'type': 'Psychic',
                    'effective': ['Fighting', 'Poison'],
                    'not effective': ['Psychic', 'Steel']},
        'Ancient Power': {'name': 'Ancient Power', 'power': 60, 'type': 'Rock',
                        'effective': ['Fire','Ice','Flying','Bug'],
                        'not effective': ['Fighting', 'Ground',
                        'Steel']}, 
        'Psycho Cut': {'name': 'Psycho Cut', 'power': 70, 'type': 'Psychic',
                    'effective': ['Fighting', 'Poison'],
                    'not effective': ['Psychic', 'Steel']},
        'Psystrike': {'name': 'Psystrike', 'power': 100, 'type': 'Psychic',
                    'effective': ['Fighting', 'Poison'],
                    'not effective': ['Psychic', 'Steel']},
        'Future Sight': {'name': 'Future Sight', 'power': 120, 'type': 'Psychic',
                        'effective': ['Fighting', 'Poison'],
                        'not effective': ['Psychic', 'Steel']},
        'Lick': {'name': 'Lick', 'power': 30, 'type': 'Ghost',
                'effective': ['Psychic', 'Ghost'],
                'not effective': ['Dark']}, 
        'Shadow Punch': {'name': 'Shadow Punch', 'power': 60, 'type': 'Ghost',
                        'effective': ['Psychic', 'Ghost'],
                        'not effective': ['Dark']},
        'Sucker Punch': {'name': 'Sucker Punch', 'power': 70, 'type': 'Dark',
                        'effective': ['Psychic', 'Ghost'],
                        'not effective': ['Fighting', 'Dark',
                        'Fairy']}, 
        'Dream Eater': {'name': 'Dream Eater', 'power': 100, 'type': 'Psychic',
                        'effective': ['Fighting', 'Poison'],
                        'not effective': ['Psychic', 'Steel']},
        'Covet': {'name': 'Covet', 'power': 60, 'type': 'Normal', 
                'effective': ['N/A'], 
                'not effective': ['Rock', 'Steel']},
        'Sand Attack': {'name': 'Sand Attack', 'power': 55, 'type': 'Ground',
                        'effective': ['Fire', 'Electric', 'Poison',
                        'Rock', 'Steel'],
                        'not effective': ['Grass', 'Bug']}, 
        'Take Down': {'name': 'Take Down', 'power': 90, 'type': 'Normal', 
                    'effective': ['N/A'], 
                    'not effective': ['Rock', 'Steel']},
        'Last Resort': {'name': 'Last Resort', 'power': 140, 'type': 'Normal', 
                        'effective': ['N/A'], 
                        'not effective': ['Rock','Steel']},
        'Thunderbolt': {'name': 'Thunderbolt', 'power': 90, 'type': 'Electric',
                        'effective': ['Water', 'Flying'],
                        'not effective': ['Electric','Grass',
                        'Dragon']}, 
        'Flash Cannon': {'name': 'Flash Cannon', 'power': 80, 'type': 'Steel',
                        'effective': ['Ice', 'Rock', 'Fairy'],
                        'not effective': ['Fire', 'Water',
                        'Electric','Steel']}, 
        'Vine Whip': {'name': 'Vine Whip', 'power': 45, 'type': 'Grass',
                    'effective': ['Water', 'Ground', 'Rock'],
                    'not effective': ['Fire', 'Grass', 'Poison',
                    'Flying', 'Bug', 'Dragon', 'Steel']}, 
        'Razor Leaf': {'name': 'Razor Leaf', 'power': 55, 'type': 'Grass',
                    'effective': ['Water', 'Ground', 'Rock'],
                    'not effective': ['Fire', 'Grass', 'Poison',
                    'Flying', 'Bug', 'Dragon', 'Steel']},
        'Solar Beam': {'name': 'Solar Beam', 'power': 120, 'type': 'Grass',
                    'effective': ['Water', 'Ground', 'Rock'],
                    'not effective': ['Fire', 'Grass', 'Poison',
                    'Flying', 'Bug', 'Dragon', 'Steel']}, 
        'Fire Spin': {'name': 'Fire Spin', 'power': 35, 'type': 'Fire',
                    'effective': ['Grass', 'Ice', 'Bug', 'Steel'],
                    'not effective': ['Fire', 'Water', 'Rock',
                    'Dragon']},
        'Flamethrower': {'name': 'Flamethrower', 'power': 90, 'type': 'Fire',
                        'effective': ['Grass', 'Ice', 'Bug',
                        'Steel'],'not effective': ['Fire', 'Water',
                        'Rock','Dragon']}, 
        'Wrap': {'name': 'Wrap', 'power': 15, 'type': 'Normal', 
                'effective': ['N/A'], 
                'not effective': ['Rock', 'Steel']},
        'Knock Off': {'name': 'Knock Off', 'power': 65, 'type': 'Dark',
                    'effective': ['Psychic', 'Ghost'],
                    'not effective': ['Fighting', 'Dark','Fairy']}, 
        'Pursuit': {'name': 'Pursuit', 'power': 40, 'type': 'Dark',
                    'effective': ['Psychic', 'Ghost'],
                    'not effective': ['Fighting', 'Dark','Fairy']}, 
        'Psycho Boost': {'name': 'Psycho Boost', 'power': 140, 'type':'Psychic',
                        'effective': ['Fighting', 'Poison'],
                        'not effective': ['Psychic', 'Steel']},
        'Rock Throw': {'name': 'Rock Throw', 'power': 50, 'type': 'Rock',
                    'effective': ['Fire', 'Ice', 'Flying', 'Bug'],
                    'not effective': ['Fighting', 'Ground',
                    'Steel']}, 
        'Mega Punch': {'name': 'Mega Punch', 'power': 80, 'type': 'Normal', 
                    'effective': ['N/A'], 
                    'not effective': ['Rock', 'Steel']},
        'Rock Slide': {'name': 'Rock Slide', 'power': 75, 'type': 'Rock',
                    'effective': ['Fire', 'Ice', 'Flying', 'Bug'],
                    'not effective': ['Fighting', 'Ground',
                    'Steel']},
        'Earthquake': {'name': 'Earthquake', 'power': 100, 'type': 'Ground',
                    'effective': ['Fire', 'Electric', 'Poison',
                    'Rock', 'Steel'], 'not effective':
                    ['Grass', 'Bug']},  
        'Aqua Jet': {'name': 'Aqua Jet', 'power': 40, 'type': 'Water',
                    'effective': ['Fire', 'Ground', 'Rock'],
                    'not effective': ['Water', 'Grass', 'Dragon']}, 
        'Headbutt': {'name': 'Headbutt', 'power': 70, 'type': 'Normal',
                    'effective': ['N/A'],
                    'not effective': ['Rock', 'Steel']},
        'Ice Shard': {'name': 'Ice Shard', 'power': 40, 'type': 'Ice',
                    'effective': ['Grass', 'Ground', 'Flying',
                    'Dragon'], 'not effective': ['Fire', 'Water',
                    'Ice', 'Steel']},
        'Waterfall': {'name': 'Waterfall', 'power': 80, 'type': 'Water', 
                    'effective': ["Fire", "Ground", "Rock"], 
                    'not effective': ["Water", "Grass", "Dragon"]},  
        'Double Edge': {'name': 'Double Edge', 'power': 120, 'type': 'Normal',
                        'effective': ['N/A'],
                        'not effective': ['Rock', 'Steel']},
        'Absorb': {'name': 'Absorb', 'power': 20, 'type': 'Grass',
                'effective': ['Water', 'Ground', 'Rock'],
                'not effective': ['Fire', 'Grass', 'Poison',
                'Flying', 'Bug', 'Dragon', 'Steel']}, 
        'Fairy Wind': {'name': 'Fairy Wind', 'power': 40, 'type': 'Fairy',
                    'effective': ['Fighting', 'Dragon', 'Dark'],
                    'not effective': ['Fire', 'Poison', 'Steel']}, 
        'Struggle Bug': {'name': 'Struggle Bug', 'power': 50, 'type': 'Bug',
                        'effective': ['Grass', 'Psychic', 'Dark'],
                        'not effective': ['Fire', 'Fighting',
                        'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy']}, 
        'Draining Kiss': {'name': 'Draining Kiss', 'power': 50, 'type': 'Fairy',
                        'effective': ['Fighting','Dragon','Dark'],
                        'not effective':['Fire','Poison','Steel']},
        'Bug Buzz': {'name': 'Bug Buzz', 'power': 90, 'type': 'Bug',
                    'effective': ['Grass', 'Psychic', 'Dark'],
                    'not effective': ['Fire', 'Fighting',
                    'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy']}}

        
        effectiveOrNot = {}

        for move in computer.moves:
            moveType = movesDict[move]['type']

            effective = 1
            for type_ in player.type_:
                if type_ in movesDict[move]['effective']:
                    effective *= 2
                elif type_ in movesDict[move]['not effective']:
                    effective *= 0.5
                else:
                    effective *= 1

            effectiveOrNot[effective] = effectiveOrNot.get(effective, [])+[move]

        return effectiveOrNot

    def stronggestMove(mode, playerPKM, compPKM):
        # Got Pokemon info from https://pokemondb.net/pokedex/squirtle
        
        # Creating a list of tuples (power, move) that contains 
        # all the available moves and their corresponding power
        # Return the strongest move with the highest power

        movesPower = {
                    'Nuzzle': 20,
                    'Quick Attack': 40,
                    'Thunder Shock': 40,
                    'Spark': 65,
                    'Slam': 80,
                    'Ember': 40,
                    'Scratch': 40,
                    'Air Slash': 75,
                    'Slash': 70,
                    'Flare Blitz': 120,
                    'Tackle': 40,
                    'Water Gun': 40,
                    'Bite': 60,
                    'Aqua Tail': 90,
                    'Skull Bash': 130,
                    'Confusion': 50,
                    'Ancient Power': 60,
                    'Psycho Cut': 70,
                    'Psystrike': 100,
                    'Future Sight': 120,
                    'Lick': 30,
                    'Shadow Punch': 60,
                    'Sucker Punch': 70,
                    'Dream Eater': 100,
                    'Covet': 60,
                    'Sand Attack': 55,
                    'Flash Cannon': 80,
                    'Take Down': 90,
                    'Last Resort': 140,
                    'Thunderbolt': 90,
                    'Vine Whip': 45,
                    'Razor Leaf': 55,
                    'Solar Beam': 120,
                    'Fire Spin': 35,
                    'Flamethrower': 90,
                    'Wrap': 15,
                    'Knock Off': 65,
                    'Pursuit': 40,
                    'Psycho Boost': 140,
                    'Rock Throw': 50,
                    'Mega Punch': 80,
                    'Rock Slide': 75,
                    'Earthquake': 100,
                    'Aqua Jet': 40,
                    'Headbutt': 70,
                    'Ice Shard': 40,
                    'Waterfall': 80,
                    'Double Edge': 120,
                    'Pound': 40,
                    'Absorb': 20,
                    'Fairy Wind': 40,
                    'Struggle Bug': 50,
                    'Draining Kiss': 50,
                    'Bug Buzz': 90}
        bestmove = []
        for effectiveLevel, moves in mode.moveEffective(mode.playerPKM, mode.compPKM).items():
            for move in moves:
                bestmove.append((movesPower[move] * effectiveLevel, move))
        bestmove = sorted(bestmove)
        strongest = bestmove[-1]
        return strongest

    def initiatePokemon(mode):

        # Ask for player's pokemon given all the available characters
        askPlayerPKM = (f'Your character choices are '
                     f'{mode.player.charList}. Which character would'
                     f'you like?')
        playerPKM = mode.getUserInput(askPlayerPKM).title()

        # Check whether the name entered is available
        while playerPKM not in mode.player.charList:
            askAgainMsg = (f'You did not enter a valid character'
                           f'Your character choices are'
                           f'{mode.player.charList}. Which '
                           f'character would you like?')
            playerPKM = mode.getUserInput(askAgainMsg).title()
        
        # Initialize player's pokemon
        mode.playerPKM = Pokemon(playerPKM, mode.player.level, mode)

        # Opponent pokemons based on player's level
        opponentL1 = ['Magnemite', 'Pikachu', 'Charmander', 'Cutiefly',
                          'Squirtle', 'Bulbasaur']
        opponentL2 = ['Deoxys','Eevee', 'Gengar', 'Charizard']
        opponentL3 = ['Golem', 'Dewgong', 'Mewtwo']

        # Opponent randomly chooses a pokemon character based on player's level
        if mode.player.level == 1:
            levelChoice = random.choices(population=[opponentL1, opponentL2,
                                       opponentL3], weights=[0.6,0.3,0.1])
            for choices in levelChoice:
                comp_character = random.choice(choices)
        elif mode.player.level == 2:
            levelChoice = random.choices(population=[opponentL1, opponentL2,
                                       opponentL3], weights=[0.2,0.6,0.2])
            for choices in levelChoice:
                comp_character = random.choice(choices)
        elif mode.player.level == 3:
            levelChoice = random.choices(population=[opponentL1, opponentL2,
                                       opponentL3], weights=[0.1,0.3,0.6])
            for choices in levelChoice:
                comp_character = random.choice(choices)
    
        # Initialize computer's pokemon
        mode.compPKM = Pokemon('Pikachu', mode.player.level, mode)
        #mode.compPKM = Pokemon(comp_character, mode.player.level, mode)

        
        # Determine whether player or computer start based on their speed
        if mode.playerPKM.speed >= mode.compPKM.speed:
            mode.playerTurn = True
            mode.compDone = True
            mode.playerMakeMove()
        else:
            mode.playerTurn= False
            mode.compMakeMove()
        
    def cheat(mode):
        # Ask if the player is willing to sacrifice 10% of its HP to know the
        # best move against computer
        mode.pause = True
        askSacrific = ("Would you like to sacrifice 10% "
                       "of your HP in exchange for the best "
                       "move against your opponent? yes/no ")
        sacrifice = mode.getUserInput(askSacrific)
        if sacrifice == 'yes':
            mode.playerPKM.hp = 0.9 * mode.playerPKM.hp
            mode.cheatMove = mode.stronggestMove(mode.playerPKM, mode.compPKM)
            mode.displayCheatMove = True
        else:
            mode.pause = False
        
    def playerMakeMove(mode): 
        if mode.playerPKM.hp > 0:
            mode.itemUsed = 'start'
            # Check whether player wants to use moves or the items they bought
            moveOrInven = ('Do you want to attack with available moves or '
                           'use items in your inventory? '
                           'Respond with "moves" or "items"')
            decision = mode.getUserInput(moveOrInven).title()
            
            while decision not in ['Moves', 'Items']:
                moveOrInvenAgain=('You entered invalid response. '
                                  'Please only respond with "moves" or "items"')
                decision = mode.getUserInput(moveOrInvenAgain).title()
            
            if decision == 'Moves':
                askMoveMsg = (f'The moves avaliable are {mode.playerPKM.moves}.'
                              f' Which move would you like?')
                move = mode.getUserInput(askMoveMsg).title()
                        
                # Check whether the move entered is available
                while move not in mode.playerPKM.moves:
                    askMoveAgain = ('You did not input a possible move. '
                                'Please try again. Which move would you like? '
                                f'{mode.playerPKM.moves}')
                    move = mode.getUserInput(askMoveAgain).title()

                mode.playerMove = MovesSprites(move, mode)
                mode.playerMove.startX, mode.playerMove.startY = 225, 340
                mode.drawPlayerMove = True

                # Calculate damage 
                mode.damageOnComp = mode.playerPKM.damage(move, mode.player.level,
                                                    mode.compPKM.type_)
            
            elif decision == 'Items':
                mode.useInven = True
            
            #mode.playerDone = True

    def runItemFeature(mode):
        if mode.itemUsed == 'Master Ball':
            mode.capture()
        elif mode.itemUsed == 'Great Ball':
            chance = random.choice(['yes','no'])
            if chance == 'yes': mode.capture()
        elif mode.itemUsed == 'Ultra Ball':
            chance = random.choices(population=['yes','no'], weights=[0.7, 0.3])
            if chance == 'yes': mode.capture()
        elif mode.itemUsed == 'Poké Ball':
            chance = random.choices(population=['yes','no'], weights=[0.3, 0.7])
            if chance == 'yes': mode.capture()
        elif mode.itemUsed == 'Poison':
            if mode.compPKM.level > 1:
                mode.compPKM.level -= 1
                mode.compPKM.changeMoves()
        elif mode.itemUsed == 'Full Restore':
            mode.playerPKM.hp = Pokemon(mode.playerPKM.name, mode.playerPKM.level, mode).hp
   
            
    
    def capture(mode):
        mode.drawCompPKM = False
        mode.player.updateCharList(f'{mode.compPKM.name}')
        mode.successfulCapture = True
        mode.battleOver = True

    def checkPlayerHit(mode):
        # Check if the position of the move drawn has reached 
        # computer's pokemon yet
        if ((440 < mode.playerMove.startX < 460) and
            (170 < mode.playerMove.startY < 190)):
            mode.runItemFeature()
            mode.playerDoneMoving = True
            mode.playerDone = True
            mode.compDoneMoving = False

    def compMakeMove(mode):
        if mode.compPKM.hp > 0:
            # Find the move that does the most damage 
            # using the dictionary generated in mode.moveEffective
            highest = 0
            effectivity = []
            for key in mode.moveEffective(mode.compPKM, mode.playerPKM).keys():
                effectivity.append(key)
                if key > highest:
                    highest = key
            print(mode.compPKM.moves)

            # Computer chooses a move based on player's level
            # When calculating damage, the computer always uses 
            # player's level to ensure they are evenly matches
            if mode.player.level == 3:
                move = random.choice(mode.moveEffective(mode.compPKM,
                                            mode.playerPKM)[effectivity[0]])
                mode.damageOnPlayer = mode.compPKM.damage(move,
                                      mode.player.level, mode.playerPKM.type_)
            elif mode.player.level == 2:
                if len(effectivity) >= 2:
                    move = random.choice(mode.moveEffective(mode.compPKM,
                                         mode.playerPKM)[effectivity[-2]])
                    mode.damageOnPlayer = mode.compPKM.damage(move,
                                        mode.player.level,mode.playerPKM.type_)
                else:
                    print('<2')
                    move = random.choice(mode.moveEffective(mode.compPKM,
                                         mode.playerPKM)[effectivity[0]])
                    mode.damageOnPlayer = mode.compPKM.damage(move,
                                        mode.player.level,mode.playerPKM.type_)
            elif mode.player.level == 1:
                move = random.choice(mode.moveEffective(mode.compPKM,
                                     mode.playerPKM)[effectivity[-1]])
                mode.damageOnPlayer = mode.compPKM.damage(move,
                                      mode.player.level,mode.playerPKM.type_)

            mode.compMove = MovesSprites(move, mode)
            mode.compMove.startX, mode.compMove.startY = 450, 180 
            mode.drawCompMove= True

            #mode.compDone = True

    def keyPressed(mode, event):
        if (mode.drawWinner) or (mode.successfulCapture):
            if event.key == 'Space':
                mode.app.setActiveMode(mode.app.regularGameMode)
        elif (event.key == 'c'):
            mode.cheat()
        elif (event.key == 'h'):
            mode.pause = True
            mode.app.setActiveMode(mode.app.helpMode)
        elif (event.key == 'p'):
            mode.pause = not mode.pause
        
        if mode.notEnoughItems:
            if event.key == 'Space':
                mode.notEnoughItems = False
        elif mode.notEnoughMoney:
            if (event.key == 'Space'):
                if mode.broke:
                    mode.storeFunction = False
                if mode.notEnoughMoney:
                    mode.notEnoughMoney = False

    def checkCompHit(mode):
        # Check if the position of the move drawn has reached 
        # player's pokemon yet
        if ((215 < mode.compMove.startX < 235) and
            (330 < mode.compMove.startY < 350)):
            mode.compDoneMoving = True
            mode.compDone = True
            mode.playerDoneMoving = False

    def determineWiner(mode, playerHP, compHP):
        # Determine the winner based on whose HP goes negative first
        if mode.decideWinnter:
            if (mode.playerPKM.hp > 0) and (mode.compPKM.hp <= 0):
                mode.player.exp += 10
                mode.drawWinner = True
                mode.decideWinnter = False
                mode.winner = 'You'
                mode.player.updateLevel()
                print(mode.player.level)
                
            elif (mode.compPKM.hp > 0) and (mode.playerPKM.hp <= 0):
                mode.drawWinner = True
                mode.winner = 'Computer'
                mode.decideWinnter = False
                if mode.player.exp >= 5:
                    mode.player.exp -= 5
                mode.player.updateLevel()

    def playerMoveMove(mode):
        # Start drawing player move's sprite if conditions are met
        if mode.drawPlayerMove:
            # Avoid running into bug because items don't have sprites
            try:
                mode.playerMove.spriteCounter = ((1 + mode.playerMove.spriteCounter)
                                                % len(mode.playerMove.sprites))
            except:
                pass
            mode.playerMove.startX += 11.25
            mode.playerMove.startY -= 8
            mode.checkPlayerHit()
            if mode.playerDoneMoving: 
                mode.drawPlayerMove = False
                mode.displayPlayerDamage = True
                mode.playerTurn = False
                mode.compPKM.hp -= mode.damageOnComp
                mode.actuallyRunCompMove = True

    def compMoveMove(mode):
        # Start drawing computer move's sprite if conditions are met
        if mode.drawCompMove:
            mode.compMove.spriteCounter = ((1 + mode.compMove.spriteCounter)
                                            % len(mode.compMove.sprites))
            mode.compMove.startX -= 11.25
            mode.compMove.startY += 8
            mode.checkCompHit()
            if mode.compDoneMoving: 
                mode.drawCompMove = False
                mode.playerTurn = True
                mode.playerPKM.hp -= mode.damageOnPlayer
                mode.actuallyRunPlayerMove = True


    def timerFired(mode):
        if (not mode.pause) and (not mode.battleOver):
            mode.playerMoveMove()
            mode.compMoveMove()

            # Computer and player take turns to attack
            if ((mode.playerTurn) and (mode.compDone) and (not mode.drawCompMove)
                and mode.actuallyRunPlayerMove):
                mode.determineWiner(mode.playerPKM.hp, mode.compPKM.hp)
                mode.playerMakeMove()
                mode.actuallyRunPlayerMove = False
            elif ((not mode.playerTurn) and (mode.playerDone) and 
                (not mode.drawPlayerMove) and mode.actuallyRunCompMove):
                mode.determineWiner(mode.playerPKM.hp, mode.compPKM.hp)
                mode.compMakeMove()
                mode.actuallyRunCompMove = False


            mode.determineWiner(mode.playerPKM.hp, mode.compPKM.hp)

    def mousePressed(mode, event):
        # Enable all the clicks when store is drawn
        if mode.useInven:
            if (10 < event.x < 190) and (70 < event.y < 180):
                if mode.player.inventory['Master Ball'] > 0:
                    mode.player.inventory['Master Ball'] = mode.player.inventory.get('Master Ball', 0) - 1
                    mode.itemUsed = 'Master Ball'
                    mode.itemIcon = mode.masterBall
                    
                    # Treat items and moves the same, except not having sprites 
                    # for items
                    mode.playerMove = MovesSprites(mode.itemUsed, mode)
                    mode.playerMove.startX, mode.playerMove.startY = 225, 340
                    mode.drawPlayerMove= True
                    mode.useInven = False
                else: mode.notEnoughItems = True

            elif (210 < event.x < 390) and (70 < event.y < 180):
                if mode.player.inventory['Full Restore'] > 0:
                    mode.player.inventory['Full Restore'] = mode.player.inventory.get('Full Restore', 0) - 1
                    mode.itemUsed = 'Full Restore'
                    mode.itemIcon = mode.fullRestore
                    mode.playerMove = MovesSprites(mode.itemUsed, mode)
                    mode.playerMove.startX, mode.playerMove.startY = 225, 340
                    mode.drawPlayerMove= True
                    mode.useInven = False
                else: mode.notEnoughItems = True

            elif (410 < event.x < 590) and (70 < event.y < 180):
                if mode.player.inventory['Poison'] > 0:
                    mode.player.inventory['Poison'] = mode.player.inventory.get('Poison', 0) - 1
                    mode.itemUsed = 'Poison'
                    mode.itemIcon = mode.poison
                    mode.playerMove = MovesSprites(mode.itemUsed, mode)
                    mode.playerMove.startX, mode.playerMove.startY = 225, 340
                    mode.drawPlayerMove= True
                    mode.useInven = False
                else: mode.notEnoughItems = True
            
            elif (10 < event.x < 190) and (220 < event.y < 325):
                if mode.player.inventory['Poké Ball'] > 0:
                    mode.player.inventory['Poké Ball'] = mode.player.inventory.get('Poké Ball', 0) - 1
                    mode.itemUsed = 'Poké Ball'
                    mode.itemIcon = mode.pokeBall
                    mode.playerMove = MovesSprites(mode.itemUsed, mode)
                    mode.playerMove.startX, mode.playerMove.startY = 225, 340
                    mode.drawPlayerMove= True
                    mode.useInven = False
                else: mode.notEnoughItems = True
            
            elif (210 < event.x < 390) and (220 < event.y < 325):
                if mode.player.inventory['Ultra Ball'] > 0:
                    mode.player.inventory['Ultra Ball'] = mode.player.inventory.get('Ultra Ball', 0) - 1
                    mode.itemUsed = 'Ultra Ball'
                    mode.itemIcon = mode.ultraBall
                    mode.playerMove = MovesSprites(mode.itemUsed, mode)
                    mode.playerMove.startX, mode.playerMove.startY = 225, 340
                    mode.drawPlayerMove= True
                    mode.useInven = False
                else: mode.notEnoughItems = True

            elif (410 < event.x < 590) and (220 < event.y < 325):
                if mode.player.inventory['Great Ball'] > 0:
                    mode.player.inventory['Great Ball'] = mode.player.inventory.get('Great Ball', 0) - 1
                    mode.itemUsed = 'Great Ball'
                    mode.itemIcon = mode.greatBall
                    mode.playerMove = MovesSprites(mode.itemUsed, mode)
                    mode.playerMove.startX, mode.playerMove.startY = 225, 340
                    mode.drawPlayerMove= True
                    mode.useInven = False
                else: mode.notEnoughItems = True
            
            elif (16 < event.x < 64) and (14 < event.y < 56):
                mode.purchase = True
                mode.useInven = False

        if mode.purchase:
            if (10 < event.x < 190) and (70 < event.y < 180):
                if mode.player.money - 100 > 0:
                    mode.player.inventory['Master Ball'] = mode.player.inventory.get('Master Ball', 0) + 1
                    mode.player.money -= 100
                else: mode.notEnoughMoney = True

            elif (210 < event.x < 390) and (70 < event.y < 180):
                if mode.player.money - 200 > 0:
                    mode.player.inventory['Full Restore'] = mode.player.inventory.get('Full Restore', 0) + 1
                    mode.player.money -= 200
                else: mode.notEnoughMoney = True

            elif (410 < event.x < 590) and (70 < event.y < 180):
                if mode.player.money - 250 > 0:
                    mode.player.inventory['Poison'] = mode.player.inventory.get('Poison', 0) + 1
                    mode.player.money -= 250
                else:mode.notEnoughMoney = True
            
            elif (10 < event.x < 190) and (220 < event.y < 325):
                if mode.player.money - 50 > 0:
                    mode.player.inventory['Poké Ball'] = mode.player.inventory.get('Poké Ball', 0) + 1
                    mode.player.money -= 50
                else: mode.notEnoughMoney = True
            
            elif (210 < event.x < 390) and (220 < event.y < 325):
                if mode.player.money - 70 > 0:
                    mode.player.inventory['Ultra Ball'] = mode.player.inventory.get('Ultra Ball', 0) + 1
                    mode.player.money -= 70
                else: mode.notEnoughMoney = True
            
            elif (410 < event.x < 590) and (220 < event.y < 325):
                if mode.player.money - 250 > 0:
                    mode.player.inventory['Great Ball'] = mode.player.inventory.get('Great Ball', 0) + 1
                    mode.player.money -= 250
                else: mode.notEnoughMoney = True
            elif (10 < event.x < 70) and (350 < event.y < 380):
                mode.useInven = True
                mode.purchase = False

    def drawMove(mode, canvas):
        if mode.drawPlayerMove:
            try:
                sprite = mode.playerMove.sprites[mode.playerMove.spriteCounter]
                canvas.create_image(mode.playerMove.startX, mode.playerMove.startY,
                                    image=ImageTk.PhotoImage(sprite))
            except:
                canvas.create_image(mode.playerMove.startX, mode.playerMove.startY,
                                    image=ImageTk.PhotoImage(mode.itemIcon))
        elif mode.drawCompMove:
            sprite = mode.compMove.sprites[mode.compMove.spriteCounter]
            canvas.create_image(mode.compMove.startX, mode.compMove.startY,
                                image=ImageTk.PhotoImage(sprite))
    
   
    def drawHPBar(mode, canvas):
        canvas.create_text(82,30, text = (f'{int(mode.playerPKM.hp)}/'
                                          f'{mode.playerPKM.oghp}'),
                                          fill = '#D63031')
        canvas.create_rectangle(60, 40, max(60, 60+(mode.playerPKM.hp*3)),
                                55, fill = '#D63031', outline = '#E84342')
        canvas.create_image(30,47.5,image=ImageTk.PhotoImage(mode.playerPKM.frontS))

        canvas.create_text(518,30, text = (f'{int(mode.compPKM.hp)}/'
                                           f'{mode.compPKM.oghp}'),
                                           fill = '#D63031')
        subtract  = mode.compPKM.oghp - mode.compPKM.hp
        canvas.create_rectangle(min(540-mode.compPKM.hp*3, 540), 40, 540,
                                55, fill = '#D63031', outline = '#E84342')
        canvas.create_image(570,47.5,
                            image=ImageTk.PhotoImage(mode.compPKM.frontS))

    def drawResult(mode, canvas):
        if mode.drawWinner:
            canvas.create_rectangle(0, 240, 600, 400, fill = '#EAF0F1')
            canvas.create_text(300,260,text=f'{mode.winner} WON!',fill ='black',
                               font = 'Georgia 20')
            canvas.create_text(300, 290, text=f'Your exp: {mode.player.exp}',
                               fill = 'black', font = 'Georgia 20')
            canvas.create_text(300, 320, text='Now your Pokemon list is:',
                               fill = 'black', font = 'Georgia 16')
            canvas.create_text(300, 340, text = f'{mode.player.charList}',
                               fill = 'black', font = 'Georgia 16')
            canvas.create_text(300,370, text= "Press 'Space' to go back.",
                               fill = 'black', font = 'Georgia 20')

    def drawCaptureResult(mode,canvas):
        if mode.successfulCapture:
            canvas.create_rectangle(0, 240, 600, 400, fill = '#EAF0F1')
            canvas.create_text(300, 260,
                               text = f'You just captured {mode.compPKM.name}!',
                               font = 'Georgia 18')
            canvas.create_text(300, 300, text='Now your Pokemon list is:',
                               fill = 'black', font = 'Georgia 18')
            canvas.create_text(300, 320, text = f'{mode.player.charList}',
                               fill = 'black', font = 'Georgia 18')
            canvas.create_text(300,360, text= "Press 'Space' to go back.",
                               fill = 'black', font = 'Georgia 18')

    def drawCheatMove(mode, canvas):
        if mode.displayCheatMove:
            canvas.create_rectangle(20, 235, 180, 265, fill = '#26ae60')
            canvas.create_text(100, 250, text = mode.cheatMove, fill = 'white',
                               font = 'Georgia 16 bold')

    def drawNotEnoughItems(mode, canvas):
        if mode.notEnoughItems:
            canvas.create_rectangle(0,100,600,300, fill = 'white')
            canvas.create_text(300,150, text="YOU DON'T HAVE THIS ITEM!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,200, text="CAN'T USE IT!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,250, text="Press 'Space' to go back",
                               font = 'Courier 22')
    
    def drawUseInven(mode, canvas):
        # Draw Inventory 
        if mode.useInven:
            canvas.create_image(300,200,image=ImageTk.PhotoImage(mode.inventory))       
            
            mode.drawItemsOwned(canvas)
            mode.drawNotEnoughItems(canvas)

            # Draw 'Store' button
            canvas.create_image(40, 35, image=ImageTk.PhotoImage(mode.storeIcon))
            canvas.create_text(313, 372,
                               text=mode.player.money,
                               font='Courier 18')

    def drawItemsOwned(mode, canvas):        
        #draw number of items owned
        canvas.create_text(143, 187,
            text=mode.player.inventory['Master Ball'],
            font='Courier 14')
        canvas.create_text(343, 187,
            text=mode.player.inventory['Full Restore'],
            font='Courier 14')
        canvas.create_text(543, 187,
            text=mode.player.inventory['Poison'],
            font='Courier 14')
        canvas.create_text(143, 337,
            text=mode.player.inventory['Poké Ball'],
            font='Courier 14')
        canvas.create_text(343, 337,
            text=mode.player.inventory['Ultra Ball'],
            font='Courier 14')
        canvas.create_text(543, 337,
            text=mode.player.inventory['Great Ball'],
            font='Courier 14')

    def drawBroke(mode, canvas):
        if mode.broke:
            canvas.create_rectangle(0,100,600,300, fill = 'white')
            canvas.create_text(300,150, text="YOU ARE BROKE!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,200, text="CAN'T BUY ANYTHING!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,250, text="Press 'Space' to go back",
                               font = 'Courier 22')
    
    def drawNotEnoughMoney(mode, canvas):
        if mode.notEnoughMoney:
            canvas.create_rectangle(0,100,600,300, fill = 'white')
            canvas.create_text(300,150, text="YOU DON'T HAVE ENOUGH MONEY!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,200, text="CAN'T BUY IT!",
                               font = 'Courier 24 bold')
            canvas.create_text(300,250, text="Press 'Space' to go back",
                               font = 'Courier 22')


    def drawStore(mode, canvas):
        if mode.purchase:
            canvas.create_image(300, 200, image=ImageTk.PhotoImage(mode.store))
            canvas.create_text(313, 372,
                               text=mode.player.money,
                               font='Courier 18')
            mode.drawItemsOwned(canvas)
            mode.drawBroke(canvas)
            mode.drawNotEnoughMoney(canvas)
            
            # Draw 'Back' button
            canvas.create_rectangle(10, 350, 70, 380, fill = '#DAE0E2')
            canvas.create_text(40, 365, text = 'Back', fill = '#333945',
                            font = 'Georgia 22')


    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,
                            image=ImageTk.PhotoImage(mode.scalePic))

        # Draw Pokemon
        if mode.drawCompPKM:
            canvas.create_image(450,180,image=ImageTk.PhotoImage(mode.compPKM.frontB))
        canvas.create_image(225,340,image=ImageTk.PhotoImage(mode.playerPKM.backB))

        mode.drawHPBar(canvas)
        mode.drawMove(canvas)
        mode.drawResult(canvas)
        mode.drawCheatMove(canvas)
        mode.drawUseInven(canvas)
        mode.drawStore(canvas)
        mode.drawCaptureResult(canvas)



class MazeStart(Mode):
    # User can choose different difficulty levels

    level = 'easy'
    def appStarted(mode):
        mode.startpic = mode.app.loadImage('splash.jpg')
        mode.colorEasy = '#26ae60'
        mode.colorIntermediate = '#26ae60'
        mode.colorHard = '#26ae60'

    def mousePressed(mode, event):
        if (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (160 < event.y < 190)):
            MazeStart.level = 'easy'
            mode.app.setActiveMode(mode.app.mazeGameMode)
        elif (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (220 < event.y < 250)):
            MazeStart.level = 'intermediate'
            mode.app.setActiveMode(mode.app.mazeGameMode)
        elif (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (280 < event.y < 310)):
            MazeStart.level = 'hard'
            mode.app.setActiveMode(mode.app.mazeGameMode)
        elif (10 < event.x < 70) and (350 < event.y < 380):
            mode.app.setActiveMode(mode.app.splashScreenMode)

    def mouseMoved(mode, event):
        if (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (160 < event.y < 190)):
            mode.colorEasy = "#218F76"
        elif (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (220 < event.y < 250)):
            mode.colorIntermediate = "#218F76"
        elif (((mode.width/2-100) < event.x < (mode.width/2+100)) and
            (280 < event.y < 310)):
            mode.colorHard = "#218F76"
        else:
            mode.colorEasy = '#26ae60'
            mode.colorIntermediate = '#26ae60'
            mode.colorHard = '#26ae60'


    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,
                            image=ImageTk.PhotoImage(mode.startpic))
        
        # Draw game name
        canvas.create_text(mode.width/2, 110, text = 'Maze Mode Level',
                           fill = '#EAF0F1', font = 'Georgia 36 bold')
        
        # Draw easy mode
        canvas.create_rectangle(mode.width/2-100, 160, mode.width/2+100, 190,
                                fill = mode.colorEasy, outline = '#10A881')
        canvas.create_text(mode.width/2, 175,
                           text='Easy', fill = '#EAF0F1',
                           font='Georgia 20')
        
        # Draw intermediate mode
        canvas.create_rectangle(mode.width/2-100, 220, mode.width/2+100, 250,
                                fill = mode.colorIntermediate, outline = '#10A881')
        canvas.create_text(mode.width/2, 235,
                           text='Intermediate', fill = '#EAF0F1',
                           font='Georgia 20')
        
        # Draw hard mode
        canvas.create_rectangle(mode.width/2-100, 280, mode.width/2+100, 310,
                                fill = mode.colorHard, outline = '#10A881')
        canvas.create_text(mode.width/2, 295,
                           text='Hard', fill = '#EAF0F1',
                           font='Georgia 20')
        
        # Draw 'Back' button
        canvas.create_rectangle(10, 350, 70, 380, fill = '#DAE0E2')
        canvas.create_text(40, 365, text = 'Back', fill = '#333945',
                           font = 'Georgia 22')

class MazeGameMode(Mode):
    player = Player(0,1)
    def appStarted(mode):
        mode.progressDict = dict()
        mode.win = False
        mode.drawWinBool = False
        mode.backButton = '#DAE0E2'

        # Different levels will have different numbers of rows and cols
        if MazeStart.level == 'easy':
            mode.rows, mode.cols = 8, 12
        elif MazeStart.level == 'intermediate':
            mode.rows, mode.cols = 10, 15
        elif MazeStart.level == 'hard':
            mode.rows, mode.cols = 12, 16
        
        mode.cellWidth = mode.width//mode.cols
        mode.cellHeight = mode.height//mode.rows

        mode.tree = Image.open('tree.png')
        mode.path = Image.open('path.png')
        mode.mazeBoard = []
        mode.solution = []
        mode.createMap()

        # Generate random wild pokemon on the map
        mode.wildPic = mode.app.loadImage('egg.png')
        mode.wildList = []
        mode.dropWildPokemon()

        mode.playerX, mode.playerY = mode.cellWidth//2, mode.cellHeight//2
        mode.right, mode.left, mode.up, mode.down = False, False, False, False

        mode.loadSprites()
        mode.username = 'hi'
        mode.newPlayer = True
        mode.loadProgress()
    
    def createMap(mode):
        # Use backtracking to create a solvable map
        easyLists = [([['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen']], [(1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (1, 3), (1, 4), (2, 4), (2, 5), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 7), (6, 8), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (2, 10), (1, 10), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11)]),
                     ([['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11)]),
                     ([['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (7, 1), (7, 2), (7, 3), (6, 3), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (6, 7), (7, 7), (7, 8), (6, 8), (6, 9), (7, 9), (7, 10), (7, 11)]),
                     ([['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (1, 4), (1, 5), (1, 6), (0, 6), (0, 7), (1, 7), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (6, 9), (5, 9), (4, 9), (4, 10), (4, 11), (5, 11), (6, 11), (7, 11)]),
                     ([['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (6, 2), (6, 3), (6, 4), (5, 4), (4, 4), (4, 5), (3, 5), (3, 6), (3, 7), (4, 7), (5, 7), (5, 8), (5, 9), (5, 10), (6, 10), (7, 10), (7, 11)])]


        intermediateLists = [([['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(0, 1), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (5, 2), (5, 3), (6, 3), (6, 4), (7, 4), (7, 5), (8, 5), (9, 5), (9, 6), (8, 6), (8, 7), (8, 8), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (9, 14)]),
                             ([['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (4, 1), (4, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 6), (4, 6), (3, 6), (2, 6), (2, 7), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (6, 9), (5, 9), (5, 10), (6, 10), (7, 10), (7, 11), (7, 12), (6, 12), (6, 13), (7, 13), (8, 13), (9, 13), (9, 14)]),
                             ([['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (4, 8), (5, 8), (5, 9), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13), (5, 13), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14)]),
                             ([['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (7, 3), (6, 3), (6, 4), (5, 4), (5, 5), (6, 5), (6, 6), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 10), (7, 10), (8, 10), (8, 11), (9, 11), (9, 12), (9, 13), (8, 13), (8, 14), (9, 14)]),
                             ([['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen']], [(0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4), (2, 5), (3, 5), (4, 5), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6), (7, 6), (7, 7), (8, 7), (8, 8), (7, 8), (7, 9), (8, 9), (9, 9), (9, 10), (8, 10), (7, 10), (7, 11), (7, 12), (7, 13), (8, 13), (9, 13), (9, 14)])]

        hardLists = [([['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (7, 2), (7, 3), (7, 4), (6, 4), (6, 5), (7, 5), (7, 6), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (11, 8), (11, 9), (11, 10), (10, 10), (10, 11), (10, 12), (10, 13), (11, 13), (11, 14), (11, 15)]),
                     ([['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (8, 4), (9, 4), (10, 4), (10, 5), (10, 6), (9, 6), (8, 6), (8, 7), (9, 7), (10, 7), (11, 7), (11, 8), (10, 8), (10, 9), (9, 9), (9, 10), (10, 10), (11, 10), (11, 11), (11, 12), (11, 13), (11, 14), (11, 15)]),
                     ([['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (1, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (2, 5), (1, 5), (0, 5), (0, 6), (1, 6), (2, 6), (2, 7), (2, 8), (1, 8), (0, 8), (0, 9), (1, 9), (1, 10), (2, 10), (3, 10), (3, 11), (3, 12), (4, 12), (5, 12), (5, 13), (5, 14), (6, 14), (7, 14), (7, 15), (8, 15), (9, 15), (9, 14), (10, 14), (11, 14), (11, 15)]),
                     ([['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen'], ['lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen']], [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (2, 5), (2, 6), (3, 6), (4, 6), (4, 7), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (8, 9), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (10, 13), (11, 13), (11, 14), (11, 15)]),
                     ([['lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen'], ['forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'forestgreen'], ['forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'forestgreen', 'forestgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'lightgreen', 'forestgreen', 'lightgreen', 'lightgreen']], [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3), (3, 3), (2, 3), (1, 3), (1, 4), (1, 5), (2, 5), (2, 6), (2, 7), (1, 7), (1, 8), (2, 8), (2, 9), (2, 10), (1, 10), (1, 11), (1, 12), (0, 12), (0, 13), (1, 13), (2, 13), (3, 13), (4, 13), (5, 13), (5, 14), (6, 14), (6, 15), (7, 15), (8, 15), (9, 15), (9, 14), (10, 14), (11, 14), (11, 15)])]

        if MazeStart.level == 'easy':
            choice = random.choice(easyLists)
        elif MazeStart.level == 'intermediate':
            choice = random.choice(intermediateLists)
        elif MazeStart.level == 'hard':
            choice = random.choice(hardLists)
            
        mode.mazeBoard = choice[0]
        mode.solution = choice[1]

        '''
        colors = ['lightgreen', 'forestgreen']
        solvable = False
        while solvable == False:
            mode.mazeBoard = [[random.choice(colors) for i in range(mode.cols)]
                               for i in range(mode.rows)]
            mode.mazeBoard[0][0] = 'lightgreen'
            (path, solution) = MazeSolver(mode.mazeBoard).solve(printReport=True)
            if solution != None:
                solvable = True
                mode.solution = path
        '''

    def loadProgress(mode):
        # Learnt and modified from
        # https://realpython.com/python-csv/#reading-csv-files-with-csv
        charSet = set()
        invenDict = dict()

        with open('PlayerProgress.csv', mode = 'r') as csvfile:
            csvReader = csv.reader(csvfile)
            next(csvReader, None)
            for row in csvReader:
                charRaw = row[4]
                charStr = charRaw.split(", ")
                charStr[0], charStr[-1] = charStr[0][1:], charStr[-1][:-1]
                for char in charStr:
                    char = char.strip(" '")
                    charSet.add(char)

                invenRaw = row[5]
                invenStr = invenRaw.split(", ")
                invenStr[0], invenStr[-1] = invenStr[0][1:], invenStr[-1][:-1]
                invenDict['Master Ball'] = int(invenStr[0])
                invenDict['Poké Ball'] = int(invenStr[1])
                invenDict['Full Restore'] = int(invenStr[2])
                invenDict['Ultra Ball'] = int(invenStr[3])
                invenDict['Poison'] = int(invenStr[4])
                invenDict['Great Ball'] = int(invenStr[5])

                mode.progressDict[row[0]] = {'exp': int(row[1]),
                                             'level': int(row[2]),
                                             'money': int(row[3]),
                                             'characters': charSet,
                                             'inventory': invenDict}

        print(mode.progressDict)

        mode.username = mode.getUserInput('What is your username').title()

        for key in mode.progressDict.keys():
            if mode.username == key:
                MazeGameMode.player = Player(mode.progressDict[key]['exp'],
                                         mode.progressDict[key]['level'],
                                         mode.progressDict[key]['money'],
                                         charSet, invenDict)
                    
        return mode.progressDict

    def dropWildPokemon(mode):
        # Only drop wild pokemon on player's path to solve the mode
        availableCell = []
        for row in range(mode.rows):
            for col in range(mode.cols):
                if (row,col) in mode.solution:
                    availableCell.append((row, col))

        for _ in range(10):
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
                mode.wildList.remove((row,col))

    def loadSprites(mode):
        # Codes modied from 
        # http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#ioMethods

        # Load player's sprites for going in all four directions
        # Up
        up = mode.app.loadImage('up.png')
        if MazeStart.level == 'easy':
            spriteUp = up
        elif MazeStart.level == 'intermediate': 
            spriteUp = mode.app.scaleImage(up, 6/7)
        elif MazeStart.level == 'hard':
            spriteUp = mode.app.scaleImage(up, 7/10)
        upWidth, upHeight = spriteUp.size
        cropUp = upWidth/4
        
        mode.spritesUp = [ ]
        for i in range(4):
            sprite = spriteUp.crop((cropUp*i, 0, cropUp*(i+1), cropUp))
            mode.spritesUp.append(sprite)

        # Down
        down = mode.app.loadImage('down.png')
        if MazeStart.level == 'easy':
            spriteDown = down
        elif MazeStart.level == 'intermediate': 
            spriteDown = mode.app.scaleImage(down, 6/7)
        elif MazeStart.level == 'hard':
            spriteDown = mode.app.scaleImage(down, 7/10)
        downWidth, downHeight = spriteDown.size
        cropDown = downWidth/4

        mode.spritesDown = [ ]
        for i in range(4):
            sprite = spriteDown.crop((cropDown*i, 0, cropDown*(i+1), cropDown))
            mode.spritesDown.append(sprite)

        # Left
        left = mode.app.loadImage('left.png')
        if MazeStart.level == 'easy':
            spriteLeft = left
        elif MazeStart.level == 'intermediate': 
            spriteLeft = mode.app.scaleImage(left, 6/7)
        elif MazeStart.level == 'hard':
            spriteLeft = mode.app.scaleImage(left, 7/10)
        leftWidth, leftHeight = spriteLeft.size
        cropLeft = leftWidth/4

        mode.spritesLeft = [ ]
        for i in range(4):
            sprite = spriteLeft.crop((cropLeft*i, 0, cropLeft*(i+1), cropLeft))
            mode.spritesLeft.append(sprite)
        
        # Right
        right = mode.app.loadImage('right.png')
        if MazeStart.level == 'easy':
            spriteRight = right
        elif MazeStart.level == 'intermediate': 
            spriteRight = mode.app.scaleImage(right, 6/7)
        elif MazeStart.level == 'hard':
            spriteRight = mode.app.scaleImage(right, 7/10)
        rightWidth, rightHeight = spriteRight.size
        cropRight = rightWidth/4

        mode.spritesRight = [ ]
        for i in range(4):
            sprite = spriteRight.crop((cropRight*i, 0, cropRight*(i+1), cropRight))
            mode.spritesRight.append(sprite)

        mode.spriteCounter = 0
        
    def playerInCell(mode, playerX, playerY):
        # Check whether player on the path rather than stepping on the trees
        row = int(playerY / mode.cellHeight)
        col = int(playerX / mode.cellWidth)

        return mode.mazeBoard[row][col] == 'lightgreen'

    def timerFired(mode):
        mode.spriteCounter = ((1 + mode.spriteCounter) % len(mode.spritesUp))

    def movePlayer(mode, dx, dy):
        # Make sure that player doesn't go off the map horizontally
        if ((mode.playerX + dx) > mode.width) or ((mode.playerX + dx) < 0 ):
            pass
        elif not mode.playerInCell((mode.playerX + dx), (mode.playerY)):
            pass
        else:
            mode.playerX += dx

        # Make sure that player doesn't go off the map vertically
        if ((mode.playerY + dy) < 0) or ((mode.playerY + dy) > mode.height):
            pass
        elif not mode.playerInCell((mode.playerX), (mode.playerY + dy)):
            pass
        else:
            mode.playerY += dy
        
        # Check if players has reached bottom-right
        # aka. solving the maze
        row = int(mode.playerY / mode.cellHeight)
        col = int(mode.playerX / mode.cellWidth)
        if (row, col) == (mode.rows-1, mode.cols-1):
            mode.win = True
            mode.drawWinBool = True
            if MazeStart.level == 'easy':
                MazeGameMode.player.exp += 10
            elif MazeStart.level == 'intermediate':
                MazeGameMode.player.exp += 20
            elif MazeStart.level == 'hard':
                MazeGameMode.player.exp += 30

    def keyPressed(mode, event):
        if event.key == 'Space':
            if (mode.drawWinBool):
                mode.app.setActiveMode(mode.app.splashScreenMode)
        elif (event.key == "Left"):
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
                        inventoryAmount = [MazeGameMode.player.inventory['Master Ball'],
                                    MazeGameMode.player.inventory['Poké Ball'],
                                    MazeGameMode.player.inventory['Full Restore'],
                                    MazeGameMode.player.inventory['Ultra Ball'],
                                    MazeGameMode.player.inventory['Poison'],
                                    MazeGameMode.player.inventory['Great Ball']]
                        info = [row[0], mode.player.exp,
                                MazeGameMode.player.level,
                                MazeGameMode.player.money,
                                MazeGameMode.player.charList,
                                inventoryAmount]
                    else:
                        info = [row[0], row[1], row[2], row[3], row[4], row[5]]
                    progressList.append(info)

            with open('PlayerProgress.csv', mode = 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['username','exp','level','chars','inventory'])
                for person in progressList:
                    writer.writerow(person)
                if mode.newPlayer:
                    inventoryAmount = [MazeGameMode.player.inventory['Master Ball'],
                                    MazeGameMode.player.inventory['Poké Ball'],
                                    MazeGameMode.player.inventory['Full Restore'],
                                    MazeGameMode.player.inventory['Ultra Ball'],
                                    MazeGameMode.player.inventory['Poison'],
                                    MazeGameMode.player.inventory['Great Ball']]
                    currentInfo = [username, MazeGameMode.player.exp,
                                    MazeGameMode.player.level,
                                    MazeGameMode.player.money,
                                    MazeGameMode.player.charList,
                                    inventoryAmount]
                    writer.writerow(currentInfo)

        mode.meetOpponent()

    def mouseMoved(mode, event):
        if (500 < event.x < 570) and (350 < event.y < 380):
            mode.backButton = '#7B8788'
        else:
            mode.backButton = '#DAE0E2'

    def mousePressed(mode, event):
        if (10 < event.x < 70) and (350 < event.y < 380):
            mode.app.setActiveMode(mode.app.mazeStart)


    def drawWin(mode, canvas):
        if mode.drawWinBool:
            canvas.create_rectangle(0, 100, 600, 300, fill = '#EAF0F1')
            canvas.create_text(300,150,text='You Solved it!',fill ='black',
                               font = 'Georgia 24')
            canvas.create_text(300, 200, text=f'Your exp: {mode.player.exp}',
                               fill = 'black', font = 'Georgia 24')
            canvas.create_text(300,250, text= "Press 'Space' to go back.",
                               fill = 'black', font = 'Georgia 24')

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
                image = (mode.tree if (mode.mazeBoard[row][col]=='forestgreen')
                        else mode.path)
                canvas.create_image(mode.cellWidth//2 + mode.cellWidth*col,
                                    mode.cellHeight//2 + mode.cellHeight*row,
                                    image=ImageTk.PhotoImage(image))
                

    def redrawAll(mode, canvas):
        mode.drawMaze(canvas)
        mode.drawPlayer(canvas)
        mode.drawWildPokemon(canvas)
        mode.drawWin(canvas)

        # Draw 'Back' buttom
        canvas.create_rectangle(10, 350, 70, 380, fill = '#DAE0E2')
        canvas.create_text(40, 365, text = 'Back', fill = '#333945',
                           font = 'Georgia 22')


class HelpMode(Mode):
    def appStarted(mode):
        mode.startpic = mode.app.loadImage('splash.jpg')
    
    def keyPressed(mode, event):
        if event.key == 'b':
            mode.app.setActiveMode(mode.app.battleMode)
        elif event.key == 'r':
            mode.app.setActiveMode(mode.app.regularGameMode)

        
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,
                            image=ImageTk.PhotoImage(mode.startpic))
        msg = '''
              This is a easy Pokémon game.
              If you defeat your opponent, your exp will increase.
              You level will also change based on your exp.
              If you want to know which move is the best against your
              opponent in exchange of your HP, press 'c' when you return
              to the mode you were on. 
              Press 'b' to return to battle or 'r' to the map.
              '''  
        canvas.create_text(mode.width/2, mode.height/2, text=msg,fill = 'white',
                           font = 'Georgia 18')


class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.regularGameMode = RegularGameMode()
        app.mazeGameMode = MazeGameMode()
        app.helpMode = HelpMode()
        app.battleMode = BattleMode()
        app.mazeStart = MazeStart()
        app.mazeGameMode = MazeGameMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

app = MyModalApp(width=600, height=400)

