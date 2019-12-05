# This is the player class I use in the main game


class Player(object):
    def __init__(self, exp, level, money = None, chars = None, inventory = None):
        self.exp = exp
        self.level = level
        if money == None:
            self.money = 500
        else:
            self.money = money
        
        # Player's starting character list
        if chars == None:
            self.charList = set(['Bulbasaur', 'Charmander', 'Squirtle'])
        else:
            self.charList = chars
        
        if inventory == None:
            self.inventory = dict()
            self.inventory['Master Ball'] = 0
            self.inventory['Poké Ball'] = 0
            self.inventory['Full Restore'] = 0
            self.inventory['Ultra Ball'] = 0
            self.inventory['Poison'] = 0
            self.inventory['Great Ball'] = 0
        else:
            self.inventory = inventory

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