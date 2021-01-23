from _thread import start_new_thread
import threading
import socket
import pickle
import sys
from game import Game
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 2525
server = ''
# server = '192.168.1.177'

# server_ip = socket.gethostbyname(socket.gethostname())

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("waiting for connection")

def update_time(game):
    while True:
        if game.game_over() or game.out_of_time():
            break
        time.sleep(1)
        game.update_times()
        

def threaded_client(conn,color,game):
    conn.send(str.encode(color))

    
    while True:
        try:
            data = pickle.loads(conn.recv(8196 * 3))
            if data:
                if data.message == "get_game":
                    conn.sendall(pickle.dumps(game))
                elif data.message == "update":
                    data.print_data()
                    game.piece_spot = game.reverse_spot(data.turnMade[0])
                    game.chosen_spot = game.reverse_spot(data.turnMade[1])
                    game.update_turn()
                    game.status = data.status
                    conn.sendall(pickle.dumps(game))
            
        except:
            break
        
    print (color + ' LEFT')
    conn.close()

p = 0
color = 'w'
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    if p % 2 == 0:
        p += 1
        game = Game()
        color ='w'
        print("waiting for another player")   
    else:
        color = 'b'
        print("creating the game")  
        game.ready = True
        timer = threading.Thread(target=update_time, args=[game])
        timer.start()

    start_new_thread(threaded_client, (conn,color,game))