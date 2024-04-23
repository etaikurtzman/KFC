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
        try:
            return self.client.recv(2048).decode()
        except:
            print("Network error: unable to connect")
    
    def sendMove(self, move):
        self.client.send(str.encode("MOVE:" + move))
        
    def sendClick(self, start):
        self.client.send(str.encode("CLICK:" + start))
    
    def sendQuit(self):
        self.client.send(str.encode("QUIT"))