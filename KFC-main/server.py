import socket
import threading
import copy
from classes.board import Board

MAX_USERS = 2


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
        conns.append(conn)
        numPlayers += 1

    num_start_clicks = [0]

    board.start_timer() # tells the board to start timing
    thread1 = threading.Thread(target=client_loop, args=[conns[0], conns[1], colors[0], board, num_start_clicks])
    thread2 = threading.Thread(target=client_loop, args=[conns[1], conns[0], colors[1], board, num_start_clicks])
    
    threads = [thread1, thread2]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    s.close()

def client_loop(conn1, conn2, playerColor, board, num_start_clicks):
    conn1.send(str.encode(playerColor))
    conn1.send(str.encode(board.grid_to_string()))
    while True:
        try:
            msg = conn1.recv(2048).decode()
            if msg == "QUIT":
                conn1.send(str.encode("Quit" + '|'))
                conn1.close()
                break
            if msg.startswith("MOVE:"):
                move = msg[len("MOVE:"):]
                start, end = eval(move)
                piece = board.move(start, end, playerColor)
                if piece:
                    cooldown_str = board.getCooldownString(end)
                    conn1.send(str.encode("END:" + str(end) + ';' + cooldown_str + ';' + str(piece) + '|'))
                    conn2.send(str.encode("END-OTHER:" + str(end) + '|'))
                tosend = (board.grid_to_string())
                conn1.send(str.encode(str(tosend) + '|'))
                conn2.send(str.encode(str(tosend) + '|'))
            if msg.startswith("CLICK:"):
                click = eval(msg[len("CLICK:"):])
                if board.click(click, playerColor):
                    conn1.send(str.encode("CLICKED:" + str(click) + '|'))
            if msg == "START":
                print("in server, got message")
                num_start_clicks[0] += 1
                print("num_start_clicks is: ", num_start_clicks)

                if num_start_clicks[0] == 2:
                    print("2 players joined!")
                    conn1.send(str.encode("READY:"))
                    conn2.send(str.encode("READY:"))
            if msg == "PAUSE":
                print("In server got PAUSE!")
                conn1.send(str.encode("PAUSED:"))
                conn2.send(str.encode("PAUSED-OTHER:"))
            if msg == "RESUME":
                print("in server got resumed!")
                num_start_clicks[0] += 1
                print("num_start_clicks is: ", num_start_clicks)
                if num_start_clicks[0] % 2 == 0:
                    print("both players have hit resume")
                    conn1.send(str.encode("RESUME:"))
                    conn2.send(str.encode("RESUME:"))
            
        except:
            conn1.close()
            break



if __name__ == '__main__':
    main()