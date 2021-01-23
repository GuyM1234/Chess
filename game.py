
class Game(object):
    def __init__(self):
        self.turn = 'w'
        self.piece_spot = (None,None)
        self.chosen_spot = (None,None)
        self.ready = False
        self.status = " "
        self.time = {
            "w": 900,
            "b": 900
            }

    def move(self):
        return (f"{self.piece_spot} {self.chosen_spot}")
 
    def update_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'

    def reverse_spot(self,spot):
        return (7 - spot[0],spot[1])

    def update_times(self):
        self.time[self.turn] -= 1
    
    def game_over(self):
        if self.status == "CHECKMATE" or self.status == "PAT":
            return True
        return False

    def out_of_time(self):
        if self.time['w'] == 0 or self.time['b'] == 0:
            return True
        return False
    
class game_data(object):
    def __init__(self,message):
        self.message = message
        self.status = " "
        self.turnMade = ((None,None),(None,None))
    
    def print_data(self):
        print(self.status)
        print(self.turnMade)
        
