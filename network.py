import socket

class Network:
    def __init__(self, host):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = 5555
        self.addr = (self.host, self.port)
        self.client.connect(self.addr)
        self.color = self.receive()
        
    def getColor(self):
        return self.color

    def receive(self):
        return self.client.recv(2048).decode()
    
    def sendMove(self, move):
        self.client.send(str.encode(move))