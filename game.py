
class Game(object):
    def __init__(self):
        self.turn = 'w'
        self.piece_spot = (None,None)
        self.chosen_spot = (None,None)
        self.ready = False
        self.status = " "
        self.white_time = 900
        self.black_time = 900

    def move(self):
        return (f"{self.piece_spot} {self.chosen_spot}")
 
    def update_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'

    def reverse_spot(self,spot):
        return (7 - spot[0],spot[1])

class game_data(object):
    def __init__(self):
        self.get_game = False
        self.status = " "
        self.turnMade = ((None,None),(None,None))
