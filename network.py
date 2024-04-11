import socket

class Network:
    def __init__(self, host):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()