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
    conns = []
    while numPlayers < MAX_USERS:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        #playerColor = colors[numPlayers]
        # thread = threading.Thread(target=client_loop, args=[conn, playerColor, board])
        # threads.append(thread)
        # thread.start()
        conns.append(conn)
        numPlayers += 1
        if numPlayers == MAX_USERS:
            thread1 = threading.Thread(target=client_loop, args=[conns[0], conns[1], colors[0], board])
            thread2 = threading.Thread(target=client_loop, args=[conns[1], conns[0], colors[1], board])
            threads = [thread1, thread2]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


    # for thread in threads:
    #     thread.join()
    


def client_loop(conn1, conn2, playerColor, board):
    conn1.send(str.encode(playerColor))
    conn1.sendall(str.encode(board.grid_to_string()))
    while True:
        try:
            start, end = eval(conn1.recv(2048))
            board.move(start, end)
            conn1.sendall(str.encode(board.grid_to_string()))
            conn2.sendall(str.encode(board.grid_to_string()))
        except:
            break
    # receive a move
    # attempt to grab squares
    # if sucessful, update board
    # send board to all players



if __name__ == '__main__':
    main()