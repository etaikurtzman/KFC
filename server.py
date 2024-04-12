import socket
import threading
from classes.board import Board

MAX_USERS = 2


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server = input("Enter your IPv4: ")
    port = 5555

    board = Board()
    
    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    s.listen(MAX_USERS)
    print("Waiting for a connection")

    numPlayers = 0
    threads = []
    colors = ['white', 'black']
    while numPlayers < MAX_USERS:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        playerColor = colors[numPlayers]
        thread = threading.Thread(target=client_loop, args=[conn, playerColor, board])
        threads.append(thread)
        thread.start()
        numPlayers += 1

    for thread in threads:
        thread.join()
    


def client_loop(conn, playerColor, board):
    conn.send(str.encode(playerColor))
    conn.sendall(str.encode(board.grid_to_string()))
    while True:
        try:
            start, end = eval(conn.recv(2048))
            board.move(start, end)
            conn.sendall(str.encode(board.grid_to_string()))
        except:
            break
    # receive a move
    # attempt to grab squares
    # if sucessful, update board
    # send board to all players



if __name__ == '__main__':
    main()