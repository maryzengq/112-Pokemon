# Copied from: http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random 
from pokemonclass import Pokemon
from movesSpritesClass import MovesSprites
from levelmoves import addMoves
import csv

# All the color codes are from https://uicolorpicker.com/

class Player(object):
    add = addMoves
    def __init__(self, exp, level, chars = None):
        self.exp = exp
        self.level = level
        # Player's starting character list
        if chars == None:
            self.charList = set(['Bulbasaur', 'Charmander', 'Squirtle'])
        else:
            self.charList = chars

    def updateLevel(self):
        # Calculate player's level based on its exp 
        if 0 <= self.exp < 10:
            self.level = 1
        elif 10 <= self.exp <= 20:
            self.level = 2
        elif self.exp > 20:
            self.level = 3
        return self.level


    def updateCharList(self, defeated):
        # Update available characters, adding defeated pokemon
        return self.charList.add(defeated)
        

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
            mode.app.setActiveMode(mode.app.mazeGameMode)

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

        mode.scrollX, mode.scrollY = 0, 0
        mode.scrollMargin = 70
        mode.playerX, mode.playerY = mode.width/2, mode.height/2
        mode.r = 10
    
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
        mode.loadProgress()
        
    
    def loadProgress(mode):
        # Leanrt and modified from
        # https://realpython.com/python-csv/#reading-csv-files-with-csv
        charSet = set()

        with open('PlayerProgress.csv', mode = 'r') as csvfile:
            csvReader = csv.reader(csvfile)
            next(csvReader, None)
            for row in csvReader:
                charRaw = row[3]
                charStr = charRaw.split(", ")
                charStr[0], charStr[-1] = charStr[0][1:], charStr[-1][:-1]
                for char in charStr:
                    char = char.strip(" '")
                    charSet.add(char)
                mode.progressDict[row[0]] = {'exp': int(row[1]),
                                             'level': int(row[2]),
                                             'characters': charSet}
        print(mode.progressDict)

        mode.username = mode.getUserInput('What is your username').title()
        for key in mode.progressDict.keys():
            if mode.username == key:
                RegularGameMode.player = Player(mode.progressDict[key]['exp'],
                                         mode.progressDict[key]['level'],
                                         charSet)
        return mode.progressDict

    def dropWildPokemon(mode):
        # Drop random, wild pokemon
        
        for i in range(3):
            wildX = random.randint(mode.mapLeftEnd + mode.scrollMargin,
                                   mode.mapRightEnd - mode.scrollMargin)
            wildY = random.randint(mode.mapTopEnd + mode.scrollMargin,
                                   mode.mapDownEnd - mode.scrollMargin)
            mode.wildList.append((wildX, wildY))
        '''
        for i in range(3):
            wildX = random.randint(200,300)
            wildY = random.randint(200,300)
            mode.wildList.append((wildX, wildY))
        '''
        
  
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
            mode.movePlayer(-20, 0)
            mode.mapPlayerX -= 20
            mode.left = True
            mode.up, mode.down, mode.right = False, False, False
        elif (event.key == "Right"):
            mode.movePlayer(+20, 0)
            mode.mapPlayerX += 20
            mode.right = True
            mode.up, mode.down, mode.left = False, False, False
        elif (event.key == 'Up'):
            mode.movePlayer(0, - 20)
            mode.mapPlayerY -= 20
            mode.up = True
            mode.down, mode.left, mode.right = False, False, False
        elif (event.key == 'Down'):
            mode.movePlayer(0, +20)
            mode.mapPlayerY += 20
            mode.down = True
            mode.up, mode.left, mode.right = False, False, False
        
        elif (event.key == 's'):
            # Leanrt and modified from
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
            
        mode.meetOpponent(mode.mapPlayerX, mode.mapPlayerY)

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

class BattleMode(Mode):
    def appStarted(mode):
        mode.pic = mode.app.loadImage('bi.png')
        mode.scalePic = mode.app.scaleImage(mode.pic, 4/3)
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

        mode.initiatePokemon()
    
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
            askMoveMsg = (f'The moves avaliable are {mode.playerPKM.moves}. '
                        f'Which move would you like?')
            move = mode.getUserInput(askMoveMsg).title()
                    
            # Check whether the move entered is available
            while move not in mode.playerPKM.moves:
                askMoveAgain = ('You did not input a possible move. '
                            'Please try again. Which move would you like? '
                            f'{mode.playerPKM.moves}')
                move = mode.getUserInput(askMoveAgain).title()

            mode.playerMove = MovesSprites(move, mode)
            mode.playerMove.startX, mode.playerMove.startY = 225, 340
            mode.drawPlayerMove= True

            # Calculate damage 
            mode.damageOnComp = mode.playerPKM.damage(move, mode.player.level,
                                                mode.compPKM.type_)
            
            mode.playerDone = True

        
    def checkPlayerHit(mode):
        # Check if the position of the move drawn has reached 
        # computer's pokemon yet
        if ((440 < mode.playerMove.startX < 460) and
            (170 < mode.playerMove.startY < 190)):
            mode.playerDoneMoving = True
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

            mode.compDone = True

    def keyPressed(mode, event):
        if mode.drawWinner:
            if event.key == 'Space':
                mode.app.setActiveMode(mode.app.regularGameMode)
        elif (event.key == 'c'):
            mode.cheat()
        elif (event.key == 'h'):
            mode.pause = True
            mode.app.setActiveMode(mode.app.helpMode)
        elif (event.key == 'p'):
            mode.pause = not mode.pause

    def checkCompHit(mode):
        # Check if the position of the move drawn has reached 
        # player's pokemon yet
        if ((215 < mode.compMove.startX < 235) and
            (330 < mode.compMove.startY < 350)):
            mode.compDoneMoving = True
            mode.playerDoneMoving = False

    def determineWiner(mode, playerHP, compHP):
        # Determine the winner based on whose HP goes negative first
        if mode.decideWinnter:
            if (mode.playerPKM.hp > 0) and (mode.compPKM.hp <= 0):
                mode.player.exp += 10
                mode.drawWinner = True
                mode.decideWinnter = False
                mode.winner = 'You'
                print('tyep of charList', type(RegularGameMode.player.charList))
                mode.player.updateCharList(f'{mode.compPKM.name}')
                mode.player.updateLevel()
                print(mode.player.level)
                
            elif (mode.compPKM.hp > 0) and (mode.playerPKM.hp <= 0):
                mode.drawWinner = True
                mode.winner = 'Computer'
                mode.decideWinnter = False
                if mode.player.exp >= 5:
                    mode.player.exp -= 5
                mode.player.updateLevel()

    def timerFired(mode):
        # Start drawing player move's sprite if conditions are met
        if not mode.pause:
            if mode.drawPlayerMove:
                mode.playerMove.spriteCounter = ((1 + mode.playerMove.spriteCounter)
                                                % len(mode.playerMove.sprites))
                mode.playerMove.startX += 11.25
                mode.playerMove.startY -= 8
                mode.checkPlayerHit()
                if mode.playerDoneMoving: 
                    mode.drawPlayerMove = False
                    mode.displayPlayerDamage = True
                    mode.playerTurn = False
                    mode.compPKM.hp -= mode.damageOnComp
                    mode.actuallyRunCompMove = True
            
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

    def drawMove(mode, canvas):
        if mode.drawPlayerMove:
            sprite = mode.playerMove.sprites[mode.playerMove.spriteCounter]
            canvas.create_image(mode.playerMove.startX, mode.playerMove.startY,
                                image=ImageTk.PhotoImage(sprite))
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
            canvas.create_rectangle(0, 100, 600, 300, fill = '#EAF0F1')
            canvas.create_text(300,120,text=f'{mode.winner} WON!',fill ='black',
                               font = 'Georgia 24')
            canvas.create_text(300, 160, text=f'Your exp: {mode.player.exp}',
                               fill = 'black', font = 'Georgia 24')
            canvas.create_text(300, 200, text='Now your Pokemon list is:',
                               fill = 'black', font = 'Georgia 16')
            canvas.create_text(300, 220, text = f'{mode.player.charList}',
                               fill = 'black', font = 'Georgia 16')
            canvas.create_text(300,260, text= "Press 'Space' to go back.",
                               fill = 'black', font = 'Georgia 24')

    def drawCheatMove(mode, canvas):
        if mode.displayCheatMove:
            canvas.create_rectangle(20, 235, 180, 265, fill = '#26ae60')
            canvas.create_text(100, 250, text = mode.cheatMove, fill = 'white',
                               font = 'Georgia 16 bold')

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,
                            image=ImageTk.PhotoImage(mode.scalePic))
        # Draw Pokemon
        canvas.create_image(450,180,image=ImageTk.PhotoImage(mode.compPKM.frontB))
        canvas.create_image(225,340,image=ImageTk.PhotoImage(mode.playerPKM.backB))

        mode.drawHPBar(canvas)
        mode.drawMove(canvas)
        mode.drawResult(canvas)
        mode.drawCheatMove(canvas)

class MazeGameMode(Mode):
    pass


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
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

app = MyModalApp(width=600, height=400)

