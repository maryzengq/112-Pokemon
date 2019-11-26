# Copied from: http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random 

addMoves = {
            'Pikachu':{2: 'Spark', 3: 'Slam'},
            'Charizard':{2: 'Slash', 3: 'Flare Blitz'},
            'Squirtle': {2: 'Aqua Tail', 3: 'Skull Bash'},
            'Mewtwo': {2: 'Psystrike', 3: 'Future Sight'},
            'Gengar': {2: 'Sucker Punch', 3: 'Dream Eater'},
            'Eevee': {2: 'Take Down', 3: 'Last Resort'},
            'Magnemite': {2: 'Flash Cannon', 3: 'Thunderbolt'},
            'Bulbasaur': {2: 'Take Down', 3: 'Solar Beam'},
            'Charmander': {2: 'Flamethrower', 3: 'Flare Blitz'},
            'Deoxys': {2: 'Psystrike', 3: 'Psycho Boost'},
            'Golem': {2: 'Rock Slide', 3: 'Earthquake'},
            'Dewgong': {2: 'Waterfall', 3: 'Double Edge'},
            'Cutiefly': {2: 'Draining Kiss', 3: 'Bug Buzz'}}