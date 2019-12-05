# This is a file where I kept my raw dictionaries data during planning


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



