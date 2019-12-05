# This is the file where I kept my addMoves ditionary so that Pokémon's moves 
# are depended on its level.

# Copied from: http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random 

addMoves = {
            'Pikachu':{1: ['Nuzzle','Quick Attack', 'Thunder Shock'],
                       2: ['Nuzzle','Quick Attack', 'Thunder Shock', 'Spark'],
                       3: ['Nuzzle','Quick Attack', 'Thunder Shock', 'Spark', 'Slam']},
            'Charizard':{1: ['Air Slash', 'Ember', 'Scratch'],
                         2: ['Air Slash', 'Ember', 'Scratch', 'Slash'],
                         3: ['Air Slash', 'Ember', 'Scratch', 'Slash','Flare Blitz']},
            'Squirtle': {1: ['Tackle', 'Water Gun', 'Bite'],
                         2: ['Tackle', 'Water Gun', 'Bite', 'Aqua Tail'],
                         3: ['Tackle', 'Water Gun', 'Bite', 'Aqua Tail', 'Skull Bash']},
            'Mewtwo': {1: ['Confusion', 'Ancient Power', 'Psycho Cut'], 
                       2: ['Confusion', 'Ancient Power', 'Psycho Cut', 'Psystrike'],
                       3: ['Confusion', 'Ancient Power', 'Psycho Cut', 'Psystrike', 'Future Sight']},
            'Gengar': {1: ['Lick', 'Shadow Punch'],
                       2: ['Lick', 'Shadow Punch', 'Sucker Punch'],
                       3: ['Lick', 'Shadow Punch', 'Sucker Punch', 'Dream Eater']},
            'Eevee': {1: ['Covet', 'Sand Attack', 'Quick Attack'],
                      2: ['Covet', 'Sand Attack', 'Quick Attack', 'Take Down'],
                      3: ['Covet', 'Sand Attack', 'Quick Attack', 'Take Down', 'Last Resort']},
            'Magnemite': {1: ['Tackle', 'Thunder Shock'],
                          2: ['Tackle', 'Thunder Shock', 'Flash Cannon'],
                          3: ['Tackle', 'Thunder Shock', 'Flash Cannon', 'Thunderbolt']},
            'Bulbasaur': {1: ['Tackle', 'Vine Whip', 'Razor Leaf'],
                          2: ['Tackle', 'Vine Whip', 'Razor Leaf', 'Take Down'],
                          3: ['Tackle', 'Vine Whip', 'Razor Leaf', 'Take Down', 'Solar Beam']},
            'Charmander': {1: ['Scratch', 'Ember', 'Fire Spin'],
                           2: ['Scratch', 'Ember', 'Fire Spin', 'Flamethrower'],
                           3: ['Scratch', 'Ember', 'Fire Spin', 'Flamethrower', 'Flare Blitz']},
            'Deoxys': {1: ['Wrap','Pursuit', 'Knock Off'],
                       2: ['Wrap','Pursuit', 'Knock Off', 'Psystrike'],
                       3: ['Wrap','Pursuit', 'Knock Off', 'Psystrike', 'Psycho Boost']},
            'Golem': {1: ['Tackle', 'Rock Throw', 'Mega Punch'],
                      2: ['Tackle', 'Rock Throw', 'Mega Punch', 'Rock Slide'],
                      3: ['Tackle', 'Rock Throw', 'Mega Punch', 'Rock Slide', 'Earthquake']},
            'Dewgong': {1: ['Aqua Jet', 'Ice Shard', 'Headbutt'],
                        2: ['Aqua Jet', 'Ice Shard', 'Headbutt', 'Waterfall'],
                        3: ['Aqua Jet', 'Ice Shard', 'Headbutt', 'Waterfall', 'Double Edge']},
            'Cutiefly': {1: ['Absorb', 'Fairy Wind', 'Struggle Bug'],
                         2: ['Absorb', 'Fairy Wind', 'Struggle Bug', 'Draining Kiss'],
                         3: ['Absorb', 'Fairy Wind', 'Struggle Bug', 'Draining Kiss', 'Bug Buzz']}}