from cmu_112_graphics import *
from tkinter import *
from PIL import Image 
import random 

class Pokemon(object):
    def __init__(self, name):
        startPokemon = {
    'Pikachu': {'Type': ['Electric'], 'HP': 35, 'Moves': ['Nuzzle', 
                'Quick Attack', 'Thunder Shock'], 'Speed': 90,
                'Front': 'pikachufront.png', 'Back': 'pikachuback.png'},
    'Charizard': {'Type': ['Fire', 'Flying'], 'HP': 78, 'Moves':
                    ['Air Slash', 'Ember', 'Scratch'], 'Speed': 100,
                    'Front': 'charifront.png', 'Back': 'chariback.png'},
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
        self.front = mode.loadImage(self.pokemonList[name]['Front'])
        self.front = self.front.resize((100,100))
        self.back = mode.loadImage(self.pokemonList[name]['Back'])
        self.back = self.back.resize((100,100))
        
        for item in startPokemon.keys():
            item['Front'] = f'{item.name}front.png'
            item['Back'] = f'{item.name}back.png'        

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
    
    def drawFront(self, canvas):
        canvas.create_image(450, 180,
                            image=ImageTk.PhotoImage(self.front))
    
    def drawBack(self, canvas):
        canvas.create_image(225, 340,
                            image=ImageTk.PhotoImage(self.back))