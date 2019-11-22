class Pokemon(object):
    def __init__(self, name):
        startPokemon = {
    'Pikachu': {'Type': ['Electric'], 'HP': 35, 'Moves': ['Nuzzle', 
                'Quick Attack', 'Thunder Shock'], 'Attack': 55, 'Defense': 40,
                'Speed': 90, 'exp': 0},
    'Charizard': {'Type': ['Fire', 'Flying'], 'HP': 78, 'Moves': [ 'Air Slash',
                  'Ember', 'Scratch'], 'Attack': 84,
                  'Defense': 78, 'Speed': 100, 'exp': 0},
    'Squirtle': {'Type': ['Water'], 'HP': 44, 'Moves': ['Tackle', 'Water Gun',
                 'Bite'], 'Attack': 48, 'Defense': 65, 'Speed': 43, 'exp': 0},
    'Mewtwo': {'Type': ['Psychic'], 'HP': 106, 'Moves': ['Confusion',
               'Ancient Power', 'Psycho Cut'], 'Attack': 110, 'Defense': 90,
               'Speed': 130, 'exp': 0},
    'Gengar': {'Type': ['Ghost', 'Poison'], 'HP': 60, 'Moves': ['Lick',
               'Shadow Punch'], 'Attack': 65, 'Defense': 60, 'Speed': 110,
               'exp': 0},
    'Eevee': {'Type': ['Normal'], 'HP': 55, 'Moves': ['Covet', 'Sand Attack',
              'Quick Attack'], 'Attack': 55, 'Defense': 50, 'Speed': 55,
              'exp': 0},
    'Magnemite': {'Type': ['Electric', 'Steel'], 'HP': 25, 'Moves': [ 'Tackle',
                  'Thunder Shock'], 'Attack': 35, 'Defense': 70, 'Speed': 45,
                  'exp': 0},
    'Bulbasaur': {'Type': ['Grass', 'Poison'], 'HP': 45, 'Moves': ['Tackle',
                  'Vine Whip', 'Razor Leaf'], 'Attack': 49, 'Defense': 49,
                  'Speed': 45, 'exp': 0},
    'Charmander': {'Type': ['Fire'], 'HP': 39, 'Moves': ['Scratch', 'Ember',
                   'Fire Spin'], 'Attack': 52, 'Defense': 43, 'Speed': 65,
                   'exp': 0},
    'Deoxys': {'Type': ['Psychic'], 'HP': 50, 'Moves': ['Wrap', 'Pursuit',
               'Knock Off'], 'Attack': 150, 'Defense': 50,
               'Speed': 150, 'exp': 0},
    'Golem': {'Type': ['Rock', 'Ground'], 'HP': 80, 'Moves': [ 'Tackle',
              'Rock Throw', 'Mega Punch'], 'Attack': 120, 'Defense': 130,
              'Speed': 45, 'exp': 0},
    'Dewgong': {'Type': ['Water', 'Ice'], 'HP': 90, 'Moves': ['Aqua Jet',
                'Ice Shard', 'Headbutt'], 'Attack': 70, 'Defense': 80,
                'Speed': 70, 'exp': 0},
    'Cutiefly': {'Type': ['Fairy', 'Bug'], 'HP': 40, 'Moves': ['Absorb',
                 'Fairy Wind', 'Struggle Bug'], 'Attack': 45,
                 'Defense': 40, 'Speed': 84, 'exp': 0}
}
        self.name = name
        self.pokemonList = startPokemon
        self.type_ = self.pokemonList[name]['Type']
        self.HP = self.pokemonList[name]['HP']
        self.moves = self.pokemonList[name]['Moves']
        self.attack = self.pokemonList[name]['Attack']
        self.defense = self.pokemonList[name]['Defense']
        self.speed = self.pokemonList[name]['Speed']
        self.exp = self.pokemonList[name]['exp']
        self.level = 1

    def damage(self, move, level, opponent_type):
        # calculate the damage using the formula
        # Damage=((2×Level5+2)×Power×AD50)×Modifier
        SUPER_EFFECTIVE = {
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

        NOT_VERY_EFFECTIVE = {
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

        MOVES = {
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
          "Psychic": ['Confusion', 'Psycho Cut','Psystrike', 'Future Sight',
                      'Dream Eater', 'Psycho Boost'],
          "Bug": ['Struggle Bug', 'Bug Buzz'],
          "Rock": ['Ancient Power', 'Rock Throw', 'Rock Slide'],
          "Ghost": ['Lick', 'Shadow Punch'],
          "Dragon": ['Outrage'],
          "Dark": ['Bite', 'Sucker Punch', 'Knock Off', 'Pursuit'],
          "Steel": ['Flash Cannon'],
          "Fairy": ['Fairy Wind', 'Draining Kiss']
                }
        # Run through the moves in the moves dictionary to see
        # if it matches one of moves of the selected pokemon
        # if the loop finds one matching move according to the pokemon's type,
        # the loop will stop.
        done = False
        for type_, all_move in MOVES.items():
            for single_move in all_move:
                if single_move == move:
                    move_type = type_
                    done = True
                    break
            if done is True:
                break
        # figure out the type modifier:
        # if one of the move of the opponent is in the super_effective dict,
        # the type modifier is multiplied by 2
        # if the in not very effetive dict, it is multiplied by 0.5
        # else, the type modifier is multiplied by 1.
        t_modifier = 1
        for _type in opponent_type:
            if _type in SUPER_EFFECTIVE[move_type]:
                t_modifier *= 2
            elif _type in NOT_VERY_EFFECTIVE[move_type]:
                t_modifier *= 0.5
            else:
                t_modifier *= 1
        self.speed = self.speed/2
        # generate random number between 0 to 511 and figure out
        # if the damage is critical.
        import random as rand
        random_critical_number = rand.randint(0, 511)
        if random_critical_number < self.speed:
            critical = 2
            print('Critical Damage!!!!')
        else:
            critical = 1
        random_float = rand.randint(85, 100)/100
        modifier = critical*random_float*t_modifier
        POWERS = {
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
            'Wrap': 15
            'Knock Off': 65,
            'Pursuit': 40,
            'Psycho Boost': 140
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
            'Bug Buzz': 90
                }
        # apply the formula to calculate the total damage
        damage = ((((2 * level) / 5 + 2) * POWERS[move] *
                   self.attack/self.defense)/50)*modifier
        return damage


def best_move(self, computer, player):
    movesDict = {
    'Nuzzle': {'name': 'Nuzzle', 'power': 20, 'type': 'Electric', 
               'super effective against': ["Water", "Flying"], 
               'not very effective against': ["Electric", "Grass", "Dragon"],
               'acc': 100},
    'Quick Attack': {'name': 'Quick Attack', 'power': 40, 'type': 'Normal', 
                     'super effective against': ["N/A"], 
                     'not very effective against': ["Rock", "Steel"],
                     'acc': 100},
    'Thunder Shock': {'name': 'Thunder Shock', 'power': 40, 'type': 'Electric',
                      'super effective against': ['Water', 'Flying'],
                      'not very effective against': ['Electric', 'Grass',
                      'Dragon'], 'acc': 100}, 
    'Spark': {'name': 'Spark', 'power': 65, 'type': 'Electric',
              'super effective against': ['Water', 'Flying'],
              'not very effective against': ['Electric', 'Grass',
              'Dragon'], 'acc': 100}
    'Slam': {'name': 'Slam', 'power': 80, 'type': 'Normal',
             'super effective against': ["N/A"], 
             'not very effective against': ["Rock", "Steel"],
             'acc': 75}
    'Ember': {'name': 'Ember', 'power': 40, 'type': 'Fire',
              'super effective against': ['Grass', 'Ice', 'Bug', 'Steel'],
              'not very effective against': ['Fire', 'Water', 'Rock', 'Dragon'],
              'acc': 100}, 
    'Scratch': {'name': 'Scratch', 'power': 40,'type': 'Normal',
                'super effective against': ['N/A'],
                'not very effective against': ['Rock', 'Steel'], 'acc': 100}, 
    'Air Slash': {'name': 'Air Slash', 'power': 75, 'type': 'Flying',
                  'super effective against': ["Grass", "Fighting", "Bug"],
                  'not very effective against': ["Electric", "Rock", "Steel"],
                  'acc': 95},
    'Slash': {'name': 'Slash', 'power': 70, 'type': 'Normal',
              'super effective against': ["N/A"], 
              'not very effective against': ["Rock", "Steel"],
              'acc': 100},
    'Flare Blitz': {'name': 'Flare Blitz', 'power': 120, 'type': 'Fire',
                    'super effective against': ['Grass', 'Ice', 'Bug', 'Steel'],
                    'not very effective against': ['Fire', 'Water', 'Rock',
                    'Dragon'], 'acc': 90},
    'Tackle': {'name': 'Tackle', 'power': 40, 'type': 'Normal', 
               'super effective against': ['N/A'], 
               'not very effective against': ['Rock', 'Steel'], 'acc': 100}, 
    'Water Gun': {'name': 'Water Gun', 'power': 40, 'type': 'Water', 
                  'super effective against': ["Fire", "Ground", "Rock"], 
                  'not very effective against': ["Water", "Grass", "Dragon"],
                  'acc': 100},    
    'Bite': {'name': 'Bite', 'power': 60, 'type': 'Dark',
             'super effective against': ['Psychic', 'Ghost'],
             'not very effective against': ['Fighting', 'Dark', 'Fairy'],
             'acc': 100}, 
    'Aqua Tail': {'name': 'Aqua Tail', 'power': 90, 'type': 'Water', 
                  'super effective against': ["Fire", "Ground", "Rock"], 
                  'not very effective against': ["Water", "Grass", "Dragon"],
                  'acc': 90}, 
    'Skull Bash': {'name': 'Skull Bash', 'power': 130, 'type': 'Normal', 
                   'super effective against': ['N/A'], 
                   'not very effective against': ['Rock', 'Steel'], 'acc': 100},
    'Confusion': {'name': 'Confusion', 'power': 50, 'type': 'Psychic',
                  'super effective against': ['Fighting', 'Poison'],
                  'not very effective against': ['Psychic', 'Steel'],
                  'acc': 100},
    'Ancient Power': {'name': 'Ancient Power', 'power': 60, 'type': 'Rock',
                      'super effective against': ['Fire','Ice','Flying','Bug'],
                      'not very effective against': ['Fighting', 'Ground',
                      'Steel'], 'acc': 80}, 
    'Psycho Cut': {'name': 'Psycho Cut', 'power': 70, 'type': 'Psychic',
                   'super effective against': ['Fighting', 'Poison'],
                   'not very effective against': ['Psychic', 'Steel'],
                   'acc': 100},
    'Psystrike': {'name': 'Psystrike', 'power': 100, 'type': 'Psychic',
                  'super effective against': ['Fighting', 'Poison'],
                  'not very effective against': ['Psychic', 'Steel'],
                  'acc': 100},
    'Future Sight': {'name': 'Future Sight', 'power': 120, 'type': 'Psychic',
                     'super effective against': ['Fighting', 'Poison'],
                     'not very effective against': ['Psychic', 'Steel'],
                     'acc': 80},
    'Lick': {'name': 'Lick', 'power': 30, 'type': 'Ghost',
             'super effective against': ['Psychic', 'Ghost'],
             'not very effective against': ['Dark'], 'acc': 100}, 
    'Shadow Punch': {'name': 'Shadow Punch', 'power': 60, 'type': 'Ghost',
                     'super effective against': ['Psychic', 'Ghost'],
                     'not very effective against': ['Dark'], 'acc': 80},
    'Sucker Punch': {'name': 'Sucker Punch', 'power': 70, 'type': 'Dark',
                     'super effective against': ['Psychic', 'Ghost'],
                     'not very effective against': ['Fighting', 'Dark', 'Fairy'],
                     'acc': 100}, 
    'Dream Eater': {'name': 'Dream Eater', 'power': 100, 'type': 'Psychic',
                    'super effective against': ['Fighting', 'Poison'],
                    'not very effective against': ['Psychic', 'Steel'],
                    'acc': 80},
    'Covet': {'name': 'Covet', 'power': 60, 'type': 'Normal', 
              'super effective against': ['N/A'], 
              'not very effective against': ['Rock', 'Steel'], 'acc': 100},
    'Sand Attack': {'name': 'Sand Attack', 'power': 55, 'type': 'Ground',
                    'super effective against': ['Fire', 'Electric', 'Poison',
                    'Rock', 'Steel'],
                    'not very effective against': ['Grass', 'Bug'], 'acc': 85}, 
    'Take Down': {'name': 'Take Down', 'power': 90, 'type': 'Normal', 
                  'super effective against': ['N/A'], 
                  'not very effective against': ['Rock', 'Steel'], 'acc': 80},
    'Last Resort': {'name': 'Last Resort', 'power': 140, 'type': 'Normal', 
                    'super effective against': ['N/A'], 
                    'not very effective against': ['Rock','Steel'], 'acc': 70},
    'Thunderbolt': {'name': 'Thunderbolt', 'power': 90, 'type': 'Electric',
                    'super effective against': ['Water', 'Flying'],
                    'not very effective against': ['Electric','Grass','Dragon'],
                    'acc': 90}, 
    'Flash Cannon': {'name': 'Flash Cannon', 'power': 80, 'type': 'Steel',
                     'super effective against': ['Ice', 'Rock', 'Fairy'],
                     'not very effective against': ['Fire', 'Water', 'Electric',
                     'Steel'], 'acc': 100}, 
    'Vine Whip': {'name': 'Vine Whip', 'power': 45, 'type': 'Grass',
                  'super effective against': ['Water', 'Ground', 'Rock'],
                  'not very effective against': ['Fire', 'Grass', 'Poison',
                  'Flying', 'Bug', 'Dragon', 'Steel'], 'acc': 100}, 
    'Razor Leaf': {'name': 'Razor Leaf', 'power': 55, 'type': 'Grass',
                   'super effective against': ['Water', 'Ground', 'Rock'],
                   'not very effective against': ['Fire', 'Grass', 'Poison',
                   'Flying', 'Bug', 'Dragon', 'Steel'], 'acc': 95},
    'Solar Beam': {'name': 'Solar Beam', 'power': 120, 'type': 'Grass',
                   'super effective against': ['Water', 'Ground', 'Rock'],
                   'not very effective against': ['Fire', 'Grass', 'Poison',
                   'Flying', 'Bug', 'Dragon', 'Steel'], 'acc': 90}, 
    'Fire Spin': {'name': 'Fire Spin', 'power': 35, 'type': 'Fire',
                  'super effective against': ['Grass', 'Ice', 'Bug', 'Steel'],
                  'not very effective against': ['Fire', 'Water', 'Rock',
                  'Dragon'], 'acc': 85},
    'Flamethrower': {'name': 'Flamethrower', 'power': 90, 'type': 'Fire',
                     'super effective against': ['Grass', 'Ice', 'Bug','Steel'],
                     'not very effective against': ['Fire', 'Water', 'Rock',
                     'Dragon'], 'acc': 100}, 
    'Wrap': {'name': 'Wrap', 'power': 15, 'type': 'Normal', 
             'super effective against': ['N/A'], 
             'not very effective against': ['Rock', 'Steel'], 'acc': 90},
    'Knock Off': {'name': 'Knock Off', 'power': 65, 'type': 'Dark',
                  'super effective against': ['Psychic', 'Ghost'],
                  'not very effective against': ['Fighting', 'Dark', 'Fairy'],
                  'acc': 90}, 
    'Pursuit': {'name': 'Pursuit', 'power': 40, 'type': 'Dark',
                'super effective against': ['Psychic', 'Ghost'],
                'not very effective against': ['Fighting', 'Dark', 'Fairy'],
                'acc': 100}, 
    'Psycho Boost': {'name': 'Psycho Boost', 'power': 140, 'type': 'Psychic',
                     'super effective against': ['Fighting', 'Poison'],
                     'not very effective against': ['Psychic', 'Steel'],
                     'acc': 90},
    'Rock Throw': {'name': 'Rock Throw', 'power': 50, 'type': 'Rock',
                   'super effective against': ['Fire', 'Ice', 'Flying', 'Bug'],
                   'not very effective against': ['Fighting', 'Ground','Steel'],
                   'acc': 90}, 
    'Mega Punch': {'name': 'Mega Punch', 'power': 80, 'type': 'Normal', 
                   'super effective against': ['N/A'], 
                   'not very effective against': ['Rock', 'Steel'], 'acc': 85},
    'Rock Slide': {'name': 'Rock Slide', 'power': 75, 'type': 'Rock',
                   'super effective against': ['Fire', 'Ice', 'Flying', 'Bug'],
                   'not very effective against': ['Fighting', 'Ground','Steel'],
                   'acc': 90},
    'Earthquake': {'name': 'Earthquake', 'power': 100, 'type': 'Ground',
                   'super effective against': ['Fire', 'Electric', 'Poison',
                   'Rock', 'Steel'], 'not very effective against':
                   ['Grass', 'Bug'], 'acc': 100},  
    'Aqua Jet': {'name': 'Aqua Jet', 'power': 40, 'type': 'Water',
                 'super effective against': ['Fire', 'Ground', 'Rock'],
                 'not very effective against': ['Water', 'Grass', 'Dragon'],
                 'acc': 100}, 
    'Headbutt': {'name': 'Headbutt', 'power': 70, 'type': 'Normal',
                 'super effective against': ['N/A'],
                 'not very effective against': ['Rock', 'Steel'], 'acc': 100},
    'Ice Shard': {'name': 'Ice Shard', 'power': 40, 'type': 'Ice',
                  'super effective against': ['Grass', 'Ground', 'Flying',
                  'Dragon'], 'not very effective against': ['Fire', 'Water',
                  'Ice', 'Steel'], 'acc': 100},
    'Waterfall': {'name': 'Waterfall', 'power': 80, 'type': 'Water', 
                  'super effective against': ["Fire", "Ground", "Rock"], 
                  'not very effective against': ["Water", "Grass", "Dragon"],
                  'acc': 100},  
    'Double Edge': {'name': 'Double Edge', 'power': 120, 'type': 'Normal',
                    'super effective against': ['N/A'],
                    'not very effective against': ['Rock', 'Steel'],'acc': 100},
    'Pound': {'name': 'Pound', 'power': 40, 'type': 'Normal',
              'super effective against': ['N/A'],
              'not very effective against': ['Rock', 'Steel'], 'acc': 100}, 
    'Absorb': {'name': 'Absorb', 'power': 20, 'type': 'Grass',
               'super effective against': ['Water', 'Ground', 'Rock'],
               'not very effective against': ['Fire', 'Grass', 'Poison',
               'Flying', 'Bug', 'Dragon', 'Steel'], 'acc': 100}, 
    'Fairy Wind': {'name': 'Fairy Wind', 'power': 40, 'type': 'Fairy',
                   'super effective against': ['Fighting', 'Dragon', 'Dark'],
                   'not very effective against': ['Fire', 'Poison', 'Steel'],
                   'acc': 100}, 
    'Struggle Bug': {'name': 'Struggle Bug', 'power': 50, 'type': 'Bug',
                     'super effective against': ['Grass', 'Psychic', 'Dark'],
                     'not very effective against': ['Fire', 'Fighting',
                     'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy'], 'acc': 90}, 
    'Draining Kiss': {'name': 'Draining Kiss', 'power': 50, 'type': 'Fairy',
                      'super effective against': ['Fighting', 'Dragon', 'Dark'],
                      'not very effective against': ['Fire', 'Poison', 'Steel'],
                      'acc': 100},
    'Bug Buzz': {'name': 'Bug Buzz', 'power': 90, 'type': 'Bug',
                 'super effective against': ['Grass', 'Psychic', 'Dark'],
                 'not very effective against': ['Fire', 'Fighting',
                 'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy'], 'acc': 100},
}

        # initializes dictionary to hold the results
        good_or_bad = {}


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

            good_or_bad[effective] = good_or_bad.get(effective, []) + [move]

        return good_or_bad


