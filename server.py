from _thread import start_new_thread
import socket
import pickle
import sys
from game import Game

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 5555

server_ip = socket.gethostbyname(socket.gethostname())

try:
    s.bind((server_ip, port))

except socket.error as e:
    print(str(e))

s.listen()
print("waiting for connection")


def threaded_client(conn,color,game):
    conn.send(str.encode(color))
    while True:
        try:
            data = conn.recv(2048).decode()
            if data == "disconnect":
                break
            elif data == "get":
                conn.sendall(pickle.dumps(game))
            elif data[0] == '(':
                game.piece_spot = (7 - int(data[1]), int(data[4]))
                game.chosen_spot = (7 - int(data[8]), int(data[11]))
                game.update_turn()
            elif data.isdigit():
                if game.turn == 'w':
                    game.white_time = int(data)
                else:
                    
                    game.black_time = int(data)
            elif data:
                game.status = data
        except:
            break
        
    print ("Connection Closed")
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
