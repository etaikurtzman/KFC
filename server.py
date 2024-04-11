import socket
import threading
from classes.board import Board

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = input("Enter your IPv4: ")
port = 5555

### board = Board()

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

def client_loop(conn):
    pass
    # while True:
    #     try:
    #         pass
    #     except:
    #         break
    # receive a move
    # attempt to grab squares
    # if sucessful, update board
    # send board to all players

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    threading.Thread(target=client_loop, args=[conn]).start()
