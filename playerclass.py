class Player(object):
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