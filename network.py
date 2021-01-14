import socket
import pickle


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self host should be the ip on which you run your server
        self.host = "192.168.1.177"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.color = self.connect()
        self.format = "utf-8"

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
        
    def getP(self):
        return self.color

    def get(self, data):
        try:
            self.client.send(str.encode(data))
            reply = pickle.loads(self.client.recv(2048))
            return reply
        except socket.error as e:
            return str(e)

    def send(self,data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            return str(e)