# Copied from: http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random 

class MovesSprites(object):
    def __init__(self, move, app):
        movesSprites = {
        'Nuzzle': 'electric.png',
        'Quick Attack': 'normal.png',
        'Thunder Shock': 'electric.png', 
        'Spark': 'electric.png',
        'Slam': 'normal.png',
        'Ember': 'fire.png', 
        'Scratch': 'normal.png', 
        'Air Slash': 'flying.png',
        'Slash': 'normal.png',
        'Flare Blitz': 'fire.png',
        'Tackle': 'normal.png', 
        'Water Gun': 'water.png',    
        'Bite': 'dark.png', 
        'Aqua Tail': 'water.png',
        'Confusion': 'psychic.png',
        'Ancient Power': 'rock.png', 
        'Psycho Cut': 'psychic.png',
        'Psystrike': 'psychic.png',
        'Future Sight': 'psychic.png',
        'Lick': 'ghost.png', 
        'Shadow Punch': 'ghost.png',
        'Sucker Punch': 'dark.png', 
        'Dream Eater': 'psychic.png',
        'Covet': 'normal.png',
        'Sand Attack': 'ground.png', 
        'Take Down': 'normal.png',
        'Last Resort': 'normal.png',
        'Thunderbolt': 'electric.png', 
        'Flash Cannon': 'steel.png', 
        'Vine Whip': 'grass.png', 
        'Razor Leaf': 'grass.png',
        'Solar Beam': 'grass.png', 
        'Fire Spin': 'fire.png',
        'Flamethrower': 'fire.png', 
        'Wrap': 'normal.png',
        'Knock Off': 'dark.png', 
        'Pursuit': 'dark.png', 
        'Psycho Boost':'psychic.png',
        'Rock Throw': 'rock.png', 
        'Mega Punch': 'normal.png',
        'Rock Slide': 'rock.png',
        'Earthquake': 'ground.png',  
        'Aqua Jet': 'water.png', 
        'Headbutt': 'normal.png',
        'Ice Shard': 'ice.png',
        'Waterfall': 'water.png',  
        'Double Edge': 'normal.png',
        'Absorb': 'grass.png', 
        'Fairy Wind': 'fairy.png', 
        'Struggle Bug':'bug png', 
        'Draining Kiss': 'fairy.png',
        'Bug Buzz': 'bug.png',
        'Skull Bash': 'normal.png'}
        self.move = move
        self.app = app
        self.startX = 0
        self.startY = 0
        if self.move in movesSprites.keys():
            self.image = movesSprites[self.move]
            self.spritestrip = self.app.loadImage(self.image)
            self.sprites = [ ]
            for i in range(4):
                sprite = self.spritestrip.crop((32*i, 0, 32*(i+1), 32))
                self.sprites.append(sprite)
        self.spriteCounter = 0
