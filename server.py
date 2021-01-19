from _thread import start_new_thread
import socket
import pickle
import sys
from game import Game

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


def threaded_client(conn,color,game):
    conn.send(str.encode(color))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if data:
                if data.get_game:
                    conn.sendall(pickle.dumps(game))
                else:       
                    game.piece_spot = game.reverse_spot(data.turnMade[0])
                    game.chosen_spot = game.reverse_spot(data.turnMade[1])
                    game.update_turn()
                    game.status = data.status
                    conn.sendall(pickle.dumps(game))




                # if type(data) is str:
                #     if data == 'get':
                #         conn.sendall(pickle.dumps(game))
                #     elif data == "disconnect":
                #         break
                #     elif data.isdigit():
                #         if game.turn == 'w':
                #             game.white_time = int(data)
                #         else:
                #             game.black_time = int(data)
                #         conn.sendall(pickle.dumps(game))
                #     else:
                #         pass
                # else:
                    
        except:
            print(data)
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

    start_new_thread(threaded_client, (conn,color,game))
