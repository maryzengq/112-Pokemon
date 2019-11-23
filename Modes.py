from cmu_112_graphics import *
from tkinter import *
import random as rand

class Player(object):
    def __init__(self, exp):
        self.exp = exp
        # keeps track of player's exp points
        self.level = self.updateLevel()

    def updateLevel(self):
        # Update player's level based on its exp
        if 0 <= self.exp < 50:
            self.level = 1
        elif 50 <= self.exp <= 100:
            self.level = 2
        else:
            self.level = 3
        return self.level

    def characterList(self, defeated):
        # Returns the character list the player can choose from
        return set(['Bulbasaur', 'Charmander', 'Squirtle'] + defeated)

class SplashScreenMode(Mode):
    def appStarted(mode):
        mode.startpic = mode.app.loadImage('start.png')
        mode.scalePic = mode.app.scaleImage(mode.startpic, 1/4)

    def mousePressed(mode, event):
        if (((mode.width/6 - 40) < event.x < (mode.width/6 + 40)) and
            ((4*mode.height/5 - 20) < event.y < (4*mode.height/5 + 20))):
            mode.app.setActiveMode(mode.app.gameMode)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2+40,
                            image=ImageTk.PhotoImage(mode.scalePic))

        canvas.create_text(mode.width/6, 4*mode.height/5,
                           text='Start', fill = 'goldenrod',
                           font='Georgia 30 bold')

class GameMode(Mode):
    def appStarted(mode):
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

        mode.mapPlayerX = mode.mapLeftEnd + mode.mapWidth/2
        mode.mapPlayerY = mode.mapTopEnd + mode.mapHeight/2
        
        mode.c_pkmList = [(rand.randint(mode.mapLeftEnd + mode.scrollMargin,
                                          mode.mapRightEnd - mode.scrollMargin),
                           rand.randint(mode.mapTopEnd + mode.scrollMargin,
                                          mode.mapDownEnd - mode.scrollMargin)) 
                           for _ in range(3)]
    
    def makePlayerVisible(mode):
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
        for (pkmX, pkmY) in mode.c_pkmList:
            if (((pkmX - 2*mode.r) <= cx <= (pkmX + 2*mode.r)) and
               ((pkmY - 2*mode.r) <= cy <= (pkmY + 2*mode.r))):
               mode.app.setActiveMode(mode.app.battleMode)

    def keyPressed(mode, event):
        if (event.key == "Left"):
            mode.movePlayer(-20, 0)
            mode.mapPlayerX -= 20
        elif (event.key == "Right"):
            mode.movePlayer(+20, 0)
            mode.mapPlayerX += 20
        elif (event.key == 'Up'):
            mode.movePlayer(0, - 20)
            mode.mapPlayerY -= 20
        elif (event.key == 'Down'):
            mode.movePlayer(0, +20)
            mode.mapPlayerY += 20
        mode.meetOpponent(mode.mapPlayerX, mode.mapPlayerY)

    def redrawAll(mode, canvas):
        cx, cy = mode.playerX, mode.playerY
        cx -= mode.scrollX
        cy -= mode.scrollY

        # Draw the map
        canvas.create_image(mode.width/2 - mode.scrollX,
                            mode.height/2 - mode.scrollY,
                            image=ImageTk.PhotoImage(mode.scalePic))
        # Draw the player
        canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r,
                           fill='lightblue')

        # Draw the c_pkm, shifted by the scrollX offset
        for (pkmX, pkmY) in mode.c_pkmList:
            pkmX -= mode.scrollX  
            pkmY -= mode.scrollY
            canvas.create_oval(pkmX-mode.r, pkmY-mode.r,pkmX+mode.r,pkmY+mode.r, 
                               fill='lightGreen')

class BattleMode(Mode):
    def appStarted(mode):
        #mode.loadProgress
        mode.pic = mode.app.loadImage('bi.png')
        mode.scalePic = mode.app.scaleImage(mode.pic, 4/3)
        mode.player = Player(0)

        mode.battle()

    
    def best_move(self, computer, player):
        movesDict = {
        'Nuzzle': {'name': 'Nuzzle', 'power': 20, 'type': 'Electric', 
                'super effective against': ["Water", "Flying"], 
                'not very effective against': ["Electric", "Grass", "Dragon"]},
        'Quick Attack': {'name': 'Quick Attack', 'power': 40, 'type': 'Normal', 
                        'super effective against': ["N/A"], 
                        'not very effective against': ["Rock", "Steel"]},
        'Thunder Shock': {'name': 'Thunder Shock', 'power': 40, 'type': 'Electric',
                        'super effective against': ['Water', 'Flying'],
                        'not very effective against': ['Electric', 'Grass',
                        'Dragon']}, 
        'Spark': {'name': 'Spark', 'power': 65, 'type': 'Electric',
                'super effective against': ['Water', 'Flying'],
                'not very effective against': ['Electric', 'Grass',
                'Dragon']},
        'Slam': {'name': 'Slam', 'power': 80, 'type': 'Normal',
                'super effective against': ["N/A"], 
                'not very effective against': ["Rock", "Steel"]},
        'Ember': {'name': 'Ember', 'power': 40, 'type': 'Fire',
                'super effective against': ['Grass', 'Ice', 'Bug', 'Steel'],
                'not very effective against': ['Fire', 'Water', 'Rock',
                'Dragon']}, 
        'Scratch': {'name': 'Scratch', 'power': 40,'type': 'Normal',
                    'super effective against': ['N/A'],
                    'not very effective against': ['Rock', 'Steel']}, 
        'Air Slash': {'name': 'Air Slash', 'power': 75, 'type': 'Flying',
                    'super effective against': ["Grass", "Fighting", "Bug"],
                    'not very effective against': ["Electric", "Rock","Steel"]},
        'Slash': {'name': 'Slash', 'power': 70, 'type': 'Normal',
                'super effective against': ["N/A"], 
                'not very effective against': ["Rock", "Steel"]},
        'Flare Blitz': {'name': 'Flare Blitz', 'power': 120, 'type': 'Fire',
                        'super effective against': ['Grass', 'Ice', 'Bug', 'Steel'],
                        'not very effective against': ['Fire', 'Water', 'Rock',
                        'Dragon']},
        'Tackle': {'name': 'Tackle', 'power': 40, 'type': 'Normal', 
                'super effective against': ['N/A'], 
                'not very effective against': ['Rock', 'Steel']}, 
        'Water Gun': {'name': 'Water Gun', 'power': 40, 'type': 'Water', 
                    'super effective against': ["Fire", "Ground", "Rock"], 
                    'not very effective against': ["Water", "Grass", "Dragon"]},    
        'Bite': {'name': 'Bite', 'power': 60, 'type': 'Dark',
                'super effective against': ['Psychic', 'Ghost'],
                'not very effective against': ['Fighting', 'Dark', 'Fairy']}, 
        'Aqua Tail': {'name': 'Aqua Tail', 'power': 90, 'type': 'Water', 
                    'super effective against': ["Fire", "Ground", "Rock"], 
                    'not very effective against': ["Water", "Grass", "Dragon"]}, 
        'Skull Bash': {'name': 'Skull Bash', 'power': 130, 'type': 'Normal', 
                    'super effective against': ['N/A'], 
                    'not very effective against': ['Rock', 'Steel']},
        'Confusion': {'name': 'Confusion', 'power': 50, 'type': 'Psychic',
                    'super effective against': ['Fighting', 'Poison'],
                    'not very effective against': ['Psychic', 'Steel']},
        'Ancient Power': {'name': 'Ancient Power', 'power': 60, 'type': 'Rock',
                        'super effective against': ['Fire','Ice','Flying','Bug'],
                        'not very effective against': ['Fighting', 'Ground',
                        'Steel']}, 
        'Psycho Cut': {'name': 'Psycho Cut', 'power': 70, 'type': 'Psychic',
                    'super effective against': ['Fighting', 'Poison'],
                    'not very effective against': ['Psychic', 'Steel']},
        'Psystrike': {'name': 'Psystrike', 'power': 100, 'type': 'Psychic',
                    'super effective against': ['Fighting', 'Poison'],
                    'not very effective against': ['Psychic', 'Steel']},
        'Future Sight': {'name': 'Future Sight', 'power': 120, 'type': 'Psychic',
                        'super effective against': ['Fighting', 'Poison'],
                        'not very effective against': ['Psychic', 'Steel']},
        'Lick': {'name': 'Lick', 'power': 30, 'type': 'Ghost',
                'super effective against': ['Psychic', 'Ghost'],
                'not very effective against': ['Dark']}, 
        'Shadow Punch': {'name': 'Shadow Punch', 'power': 60, 'type': 'Ghost',
                        'super effective against': ['Psychic', 'Ghost'],
                        'not very effective against': ['Dark']},
        'Sucker Punch': {'name': 'Sucker Punch', 'power': 70, 'type': 'Dark',
                        'super effective against': ['Psychic', 'Ghost'],
                        'not very effective against': ['Fighting', 'Dark',
                        'Fairy']}, 
        'Dream Eater': {'name': 'Dream Eater', 'power': 100, 'type': 'Psychic',
                        'super effective against': ['Fighting', 'Poison'],
                        'not very effective against': ['Psychic', 'Steel']},
        'Covet': {'name': 'Covet', 'power': 60, 'type': 'Normal', 
                'super effective against': ['N/A'], 
                'not very effective against': ['Rock', 'Steel']},
        'Sand Attack': {'name': 'Sand Attack', 'power': 55, 'type': 'Ground',
                        'super effective against': ['Fire', 'Electric', 'Poison',
                        'Rock', 'Steel'],
                        'not very effective against': ['Grass', 'Bug']}, 
        'Take Down': {'name': 'Take Down', 'power': 90, 'type': 'Normal', 
                    'super effective against': ['N/A'], 
                    'not very effective against': ['Rock', 'Steel']},
        'Last Resort': {'name': 'Last Resort', 'power': 140, 'type': 'Normal', 
                        'super effective against': ['N/A'], 
                        'not very effective against': ['Rock','Steel']},
        'Thunderbolt': {'name': 'Thunderbolt', 'power': 90, 'type': 'Electric',
                        'super effective against': ['Water', 'Flying'],
                        'not very effective against': ['Electric','Grass',
                        'Dragon']}, 
        'Flash Cannon': {'name': 'Flash Cannon', 'power': 80, 'type': 'Steel',
                        'super effective against': ['Ice', 'Rock', 'Fairy'],
                        'not very effective against': ['Fire', 'Water',
                        'Electric','Steel']}, 
        'Vine Whip': {'name': 'Vine Whip', 'power': 45, 'type': 'Grass',
                    'super effective against': ['Water', 'Ground', 'Rock'],
                    'not very effective against': ['Fire', 'Grass', 'Poison',
                    'Flying', 'Bug', 'Dragon', 'Steel']}, 
        'Razor Leaf': {'name': 'Razor Leaf', 'power': 55, 'type': 'Grass',
                    'super effective against': ['Water', 'Ground', 'Rock'],
                    'not very effective against': ['Fire', 'Grass', 'Poison',
                    'Flying', 'Bug', 'Dragon', 'Steel']},
        'Solar Beam': {'name': 'Solar Beam', 'power': 120, 'type': 'Grass',
                    'super effective against': ['Water', 'Ground', 'Rock'],
                    'not very effective against': ['Fire', 'Grass', 'Poison',
                    'Flying', 'Bug', 'Dragon', 'Steel']}, 
        'Fire Spin': {'name': 'Fire Spin', 'power': 35, 'type': 'Fire',
                    'super effective against': ['Grass', 'Ice', 'Bug', 'Steel'],
                    'not very effective against': ['Fire', 'Water', 'Rock',
                    'Dragon']},
        'Flamethrower': {'name': 'Flamethrower', 'power': 90, 'type': 'Fire',
                        'super effective against': ['Grass', 'Ice', 'Bug',
                        'Steel'],'not very effective against': ['Fire', 'Water',
                        'Rock','Dragon']}, 
        'Wrap': {'name': 'Wrap', 'power': 15, 'type': 'Normal', 
                'super effective against': ['N/A'], 
                'not very effective against': ['Rock', 'Steel']},
        'Knock Off': {'name': 'Knock Off', 'power': 65, 'type': 'Dark',
                    'super effective against': ['Psychic', 'Ghost'],
                    'not very effective against': ['Fighting', 'Dark','Fairy']}, 
        'Pursuit': {'name': 'Pursuit', 'power': 40, 'type': 'Dark',
                    'super effective against': ['Psychic', 'Ghost'],
                    'not very effective against': ['Fighting', 'Dark','Fairy']}, 
        'Psycho Boost': {'name': 'Psycho Boost', 'power': 140, 'type':'Psychic',
                        'super effective against': ['Fighting', 'Poison'],
                        'not very effective against': ['Psychic', 'Steel']},
        'Rock Throw': {'name': 'Rock Throw', 'power': 50, 'type': 'Rock',
                    'super effective against': ['Fire', 'Ice', 'Flying', 'Bug'],
                    'not very effective against': ['Fighting', 'Ground',
                    'Steel']}, 
        'Mega Punch': {'name': 'Mega Punch', 'power': 80, 'type': 'Normal', 
                    'super effective against': ['N/A'], 
                    'not very effective against': ['Rock', 'Steel']},
        'Rock Slide': {'name': 'Rock Slide', 'power': 75, 'type': 'Rock',
                    'super effective against': ['Fire', 'Ice', 'Flying', 'Bug'],
                    'not very effective against': ['Fighting', 'Ground',
                    'Steel']},
        'Earthquake': {'name': 'Earthquake', 'power': 100, 'type': 'Ground',
                    'super effective against': ['Fire', 'Electric', 'Poison',
                    'Rock', 'Steel'], 'not very effective against':
                    ['Grass', 'Bug']},  
        'Aqua Jet': {'name': 'Aqua Jet', 'power': 40, 'type': 'Water',
                    'super effective against': ['Fire', 'Ground', 'Rock'],
                    'not very effective against': ['Water', 'Grass', 'Dragon']}, 
        'Headbutt': {'name': 'Headbutt', 'power': 70, 'type': 'Normal',
                    'super effective against': ['N/A'],
                    'not very effective against': ['Rock', 'Steel']},
        'Ice Shard': {'name': 'Ice Shard', 'power': 40, 'type': 'Ice',
                    'super effective against': ['Grass', 'Ground', 'Flying',
                    'Dragon'], 'not very effective against': ['Fire', 'Water',
                    'Ice', 'Steel']},
        'Waterfall': {'name': 'Waterfall', 'power': 80, 'type': 'Water', 
                    'super effective against': ["Fire", "Ground", "Rock"], 
                    'not very effective against': ["Water", "Grass", "Dragon"]},  
        'Double Edge': {'name': 'Double Edge', 'power': 120, 'type': 'Normal',
                        'super effective against': ['N/A'],
                        'not very effective against': ['Rock', 'Steel']},
        'Pound': {'name': 'Pound', 'power': 40, 'type': 'Normal',
                'super effective against': ['N/A'],
                'not very effective against': ['Rock', 'Steel']}, 
        'Absorb': {'name': 'Absorb', 'power': 20, 'type': 'Grass',
                'super effective against': ['Water', 'Ground', 'Rock'],
                'not very effective against': ['Fire', 'Grass', 'Poison',
                'Flying', 'Bug', 'Dragon', 'Steel']}, 
        'Fairy Wind': {'name': 'Fairy Wind', 'power': 40, 'type': 'Fairy',
                    'super effective against': ['Fighting', 'Dragon', 'Dark'],
                    'not very effective against': ['Fire', 'Poison', 'Steel']}, 
        'Struggle Bug': {'name': 'Struggle Bug', 'power': 50, 'type': 'Bug',
                        'super effective against': ['Grass', 'Psychic', 'Dark'],
                        'not very effective against': ['Fire', 'Fighting',
                        'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy']}, 
        'Draining Kiss': {'name': 'Draining Kiss', 'power': 50, 'type': 'Fairy',
                        'super effective against': ['Fighting','Dragon','Dark'],
                        'not very effective against':['Fire','Poison','Steel']},
        'Bug Buzz': {'name': 'Bug Buzz', 'power': 90, 'type': 'Bug',
                    'super effective against': ['Grass', 'Psychic', 'Dark'],
                    'not very effective against': ['Fire', 'Fighting',
                    'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy']}}

        # initializes dictionary to hold the results
        effectiveOrNot = {}

        # Computer will be an instance of the pokemon class
        for move in computer.moves:
            moveType = movesDict[move]['type']

            effective = 1
            for type_ in player.type_:
                if type_ in movesDict[move]['super effective against']:
                    effective *= 2
                elif type_ in movesDict[move]['not very effective against']:
                    effective *= 0.5
                else:
                    effective *= 1

            effectiveOrNot[effective] = effectiveOrNot.get(effective, [])+[move]

        return effectiveOrNot

    def move_help(self, p_pkm, o_pkm):
        # Creating a dictionary that contains player's move
        # and its corresponding damage 
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
        for type_mod, moves in mode.best_move(p_pkm, o_pkm).items():
            for move in moves:
                bestmove.append((movesPower[move]*type_mod, move))
        return sorted(bestmove)[-1]
   

    def battle(mode):
        class Pokemon(object):
            def __init__(self, name):
                startPokemon = {
            'Pikachu': {'Type': ['Electric'], 'HP': 35, 'Moves': ['Nuzzle', 
                        'Quick Attack', 'Thunder Shock'], 'Speed': 90},
            'Charizard': {'Type': ['Fire', 'Flying'], 'HP': 78, 'Moves':
                          ['Air Slash', 'Ember', 'Scratch'], 'Speed': 100},
            'Squirtle': {'Type': ['Water'], 'HP': 44, 'Moves': ['Tackle',
                         'Water Gun', 'Bite'], 'Speed': 43},
            'Mewtwo': {'Type': ['Psychic'], 'HP': 106, 'Moves': ['Confusion',
                    'Ancient Power', 'Psycho Cut'], 'Speed': 130},
            'Gengar': {'Type': ['Ghost', 'Poison'], 'HP': 60, 'Moves': ['Lick',
                    'Shadow Punch'], 'Speed': 110},
            'Eevee': {'Type': ['Normal'], 'HP': 55, 'Moves': ['Covet',
                      'Sand Attack', 'Quick Attack'], 'Speed': 55},
            'Magnemite': {'Type': ['Electric', 'Steel'], 'HP': 25,
                          'Moves': [ 'Tackle', 'Thunder Shock'], 'Speed': 45},
            'Bulbasaur': {'Type': ['Grass', 'Poison'], 'HP': 45,
                          'Moves': ['Tackle', 'Vine Whip', 'Razor Leaf'],
                          'Speed': 45},
            'Charmander': {'Type': ['Fire'], 'HP': 39, 'Moves': ['Scratch',
                           'Ember', 'Fire Spin'], 'Speed': 65},
            'Deoxys': {'Type': ['Psychic'], 'HP': 50, 'Moves':['Wrap','Pursuit',
                       'Knock Off'], 'Speed': 150},
            'Golem': {'Type': ['Rock', 'Ground'], 'HP': 80, 'Moves': [ 'Tackle',
                    'Rock Throw', 'Mega Punch'], 'Speed': 45},
            'Dewgong': {'Type': ['Water', 'Ice'], 'HP': 90, 'Moves':['Aqua Jet',
                        'Ice Shard', 'Headbutt'], 'Speed': 70},
            'Cutiefly': {'Type': ['Fairy', 'Bug'], 'HP': 40, 'Moves': ['Absorb',
                        'Fairy Wind', 'Struggle Bug'], 'Speed': 84}}
                self.name = name
                self.pokemonList = startPokemon
                self.type_ = self.pokemonList[name]['Type']
                self.hp = self.pokemonList[name]['HP']
                self.moves = self.pokemonList[name]['Moves']
                self.speed = self.pokemonList[name]['Speed']

            def damage(self, move, level, opponent_type):
                # Calculate damage based on the move and opponent type
                
                superEffective = {
                "Normal": ["N/A"],
                "Fire": ["Grass", "Ice", "Bug", "Steel"],
                "Water": ["Fire", "Ground", "Rock"],
                "Electric": ["Water", "Flying"],
                "Grass": ["Water", "Ground", "Rock"],
                "Ice": ["Grass", "Ground", "Flying", "Dragon"],
                "Ground": ["Fire", "Electric", "Poison", "Rock", "Steel"],
                "Flying": ["Grass", "Fighting", "Bug"],
                "Psychic": ["Fighting", "Poison"],
                "Bug": ["Grass", "Psychic", "Dark"],
                "Rock": ["Fire", "Ice", "Flying", "Bug"],
                "Ghost": ["Psychic", "Ghost"],
                "Dragon": ["Dragon"],
                "Dark": ["Psychic", "Ghost"],
                "Steel": ["Ice", "Rock", "Fairy"],
                "Fairy": ["Fighting", "Dragon", "Dark"]
                            }

                notEffective = {
                "Normal": ["Rock", "Steel"],
                "Fire": ["Fire", "Water", "Rock", "Dragon"],
                "Water": ["Water", "Grass", "Dragon"],
                "Electric": ["Electric", "Grass", "Dragon"],
                "Grass": ["Fire", "Grass", "Poison", "Flying",
                            "Bug", "Dragon", "Steel"],
                "Ice": ["Fire", "Water", "Ice", "Steel"],
                "Ground": ["Grass", "Bug"],
                "Flying": ["Electric", "Rock", "Steel"],
                "Psychic": ["Psychic", "Steel"],
                "Bug": ["Fire", "Fighting", "Poison", "Flying",
                        "Ghost", "Steel", "Fairy"],
                "Rock": ["Fighting", "Ground", "Steel"],
                "Ghost": ["Dark"],
                "Dragon": ["Steel"],
                "Dark": ["Fighting", "Dark", "Fairy"],
                "Steel": ["Fire", "Water", "Electric", "Steel"],
                "Fairy": ["Fire", "Poison", "Steel"]
                                }

                moves = {
                "Normal": ['Quick Attack', 'Slam', 'Scratch', 'Slash',
                            'Tackle', 'Skull Bash', 'Covet', 'Take Down',
                            'Last Resort', 'Wrap', 'Mega Punch', 'Headbutt',
                            'Double Edge', 'Pound'],
                "Fire": ['Ember', 'Flare Blitz', 'Fire Spin', 'Flamethrower'],
                "Water": ['Water Gun', 'Aqua Tail', 'Aqua Jet', 'Waterfall'],
                "Electric": ['Nuzzle', 'Thunder Shock', 'Spark', 'Thunderbolt'],
                "Grass": ['Vine Whip', 'Razor Leaf', 'Solar Beam', 'Absorb'],
                "Ice": ['Ice Shard'],
                "Ground": ['Sand Attack', 'Earthquake'],
                "Flying": ['Air Slash'],
                "Psychic": ['Confusion','Psycho Cut','Psystrike','Future Sight',
                            'Dream Eater', 'Psycho Boost'],
                "Bug": ['Struggle Bug', 'Bug Buzz'],
                "Rock": ['Ancient Power', 'Rock Throw', 'Rock Slide'],
                "Ghost": ['Lick', 'Shadow Punch'],
                "Dragon": ['Outrage'],
                "Dark": ['Bite', 'Sucker Punch', 'Knock Off', 'Pursuit'],
                "Steel": ['Flash Cannon'],
                "Fairy": ['Fairy Wind', 'Draining Kiss']}

                # Loop throught the moves dictionary to find out the move_type
                done = False
                for type_, allMoves in moves.items():
                    for singleMove in allMoves:
                        if singleMove == move:
                            moveType = type_
                            done = True
                            break
                    if done is True:
                        break

                # Figure out the damage modifier based on opponent's type and
                # the move type the player is using
                d_modifier = 1
                for _type in opponent_type:
                    if _type in superEffective[moveType]:
                        d_modifier *= 2
                    elif _type in notEffective[moveType]:
                        d_modifier *= 0.5
                    else:
                        d_modifier *= 1
                self.speed = self.speed/2

                
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

                # apply the formula to calculate the total damage
                damage = (movesPower[move] * 0.1 * d_modifier) + (level*4)
                return damage

        # Provide all the available pokemons 
        #ask_p_pkm = (f'Your character choices are'
                     #f'{mode.player.characterList([])}. Which character would'
                     #f'you like?')
        #character = mode.getUserInput(ask_p_pkm).title()
        character = input(f'Your character choices are'
                     f'{mode.player.characterList([])}. Which character would'
                     f' you like?').title()

        # Check whether the name entered is correct
        while character not in mode.player.characterList([]):
            character = input(f'Your character choices are'
                     f'{mode.player.characterList([])}. Which character would'
                     f' you like?').title()
        # Initializes the player's pokémon
        p_pkm = Pokemon(character)

        # Opponent pokemons based on player's level
        opponentL1 = ['Magnemite', 'Pikachu', 'Charmander', 'Cutiefly',
                          'Squirtle', 'Bulbasaur']
        opponentL2 = ['Deoxys','Eevee', 'Gengar', 'Charizard']
        opponentL3 = ['Golem', 'Dewgong', 'Mewtwo']

        # Opponent randomly chooses a pokemon character based on player's level
        # Initialize computer's pokemon
        if mode.player.level == 1:
            levelChoice = rand.choices(population=[opponentL1, opponentL2,
                                       opponentL3], weights=[0.6,0.3,0.1])
            for choices in levelChoice:
                comp_character = rand.choice(choices)
        elif mode.player.level == 2:
            levelChoice = rand.choices(population=[opponentL1, opponentL2,
                                       opponentL3], weights=[0.2,0.6,0.2])
            for choices in levelChoice:
                comp_character = rand.choice(choices)
        elif mode.player.level == 3:
            levelChoice = rand.choices(population=[opponentL1, opponentL2,
                                       opponentL3], weights=[0.1,0.3,0.6])
            for choices in levelChoice:
                comp_character = rand.choice(choices)
        print(f'Your opponent has chosen a {comp_character}.')
        o_pkm = Pokemon(comp_character)

        # Determines the starter based on speed
        if p_pkm.speed >= o_pkm.speed:
            counter = 2
            print('Player starts!')
        else:
            counter = 1
            print('Opponent starts.')

        
        # Finds the most damaging moves (according to type)
        # from the list generated from mode.best_move
        highest = 0
        effectivity = []
        for key in mode.best_move(o_pkm, p_pkm).keys():
            effectivity.append(key)
            if key > highest:
                highest = key

        '''
        sacrifice = input("Would you like to sacrifice 10% "
                          "of your HP in exchange for the best "
                          "move against your opponent? yes/no ")
        if sacrifice == "yes":
            p_pkm.hp = 0.9 * p_pkm.hp
            print('Your best move is', mode.move_help(p_pkm, o_pkm)[-1])
            print("Your current hp: ", p_pkm.hp)
        '''

        # Attacking starts, alternating between the two
        while (p_pkm.hp > 0 and o_pkm.hp > 0):
            if counter % 2 == 0:
                print('\nYour turn:')
                print(f'The moves avaliable are {p_pkm.moves}')
                move = input('Which move would you like? ').title()

                # Ensures that player only picks a move in the list
                while move not in p_pkm.moves:
                    print(('You did not input a possible move. '
                          'Please try again.'))
                    move = input('Which move would you like ').title()

                # Calculate damage and substract it from other's HP
                o_pkm.hp -= p_pkm.damage(move, mode.player.level, o_pkm.type_)
                print(f"Your HP: {p_pkm.hp:.2f} Opponent's HP: {o_pkm.hp:.2f}")

            else:
                print("\nOpponent's turn: ")

                # Computer chooses a move based on player's level
                # When calculating damage, the computer always uses 
                # player's level to ensure they are evenly matched
                print("bestmove list:", mode.best_move(o_pkm, p_pkm))
                if mode.player.level == 3:
                    p_pkm.hp -= o_pkm.damage(rand.choice(mode.best_move(o_pkm,
                                             p_pkm)[highest]),mode.player.level,
                                             p_pkm.type_)
                elif mode.player.level == 2:
                    move = rand.choice(mode.best_move(o_pkm,
                                                      p_pkm)[effectivity[-2]])
                    p_pkm.hp -= o_pkm.damage(move,mode.player.level,p_pkm.type_)
                elif mode.player.level == 1:
                    move = rand.choice(mode.best_move(o_pkm,
                                                      p_pkm)[effectivity[-1]])
                    p_pkm.hp -= o_pkm.damage(move,mode.player.level,p_pkm.type_)

                print(f"Your HP: {p_pkm.hp:.2f} Opponent's HP: {o_pkm.hp:.2f}")

            counter += 1

        # returns a tuple stating the winner of the game.
        # In the case that the player wins, the program returns
        # the computer pokémon's name and experience points
        if p_pkm.hp >= o_pkm.hp:
            print('Player wins!!')
            mode.player.exp += 10
        elif o_pkm.hp > p_pkm.hp:
            print('Computer wins!!')
            if mode.player.exp >= 5:
                mode.player.exp -= 5
            return 'computer'
        
    
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,
                            image=ImageTk.PhotoImage(mode.scalePic))



class HelpMode(Mode):
    pass

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.battleMode = BattleMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

app = MyModalApp(width=600, height=400)

