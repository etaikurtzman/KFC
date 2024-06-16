'''
server.py
Contains implementation for the server
Starts the game and connects 2 players to the network. Handles message recieving
and message passing. Contains the current state of the shared board between the 
2 players. 
4/29
'''

import socket
import threading
from board import Board

MAX_USERS = 2

def main():
    # initialize and start a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # start the server
    server = input("Enter your IPv4: ")
    port = 5555

    # get the initial board
    board = Board()
    
    # Bind the socket to the server address and port
    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))

    # listen for incomming connections from players
    s.listen(MAX_USERS)
    print("Waiting for a connection")

    # initialize variables for the 2 players
    numPlayers = 0
    threads = []
    colors = ['white', 'black']
    conns = []

    # accept connections until the max number of players has been reached
    while numPlayers < MAX_USERS:
        conn, addr = s.accept()
        print("Connected to: ", addr)
        conns.append(conn)
        numPlayers += 1

    # initializes array to keep track of number of players ready to play
    num_start_clicks = [0]
    num_start_clicks_lock = threading.Lock()

    # starts the game timer
    board.start_timer()

    # create threads for both players, set target to client_loop
    thread1 = threading.Thread(target=client_loop, args=[conns[0], 
                               conns[1], colors[0], board, 
                               num_start_clicks, num_start_clicks_lock])

    thread2 = threading.Thread(target=client_loop, args=[conns[1], 
                               conns[0], colors[1], board, 
                               num_start_clicks, num_start_clicks_lock])
    
    # start and join threads
    threads = [thread1, thread2]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # close the socket
    s.close()

def client_loop(conn1, conn2, playerColor, board, 
                num_start_clicks,num_start_clicks_lock):
    """
    Manages the game loop for a client.

    Parameters
    ----------
    Player 1's socket connection: conn1
        Connection object for player 1.
    Player 2's socket connection: conn2
        Connection object for player 2.
    Player 1's Color: playerColor
        Color assigned to the player ('white' or 'black').
    Board object: board
        The game board object representing the current state of the game.
    Start list: num_start_clicks
        A list containing the number of start clicks by each player.
    Start list Lock: num_start_clicks_lock
        A lock to ensure safe access to `num_start_clicks`.

    Returns
    -------
    None
    """
    # send the player's assigned color and initial board state to the player
    conn1.send(str.encode(playerColor))
    conn1.send(str.encode(board.grid_to_string()))

    while True:
        try:
            # recieve messages
            msg = conn1.recv(2048).decode()
            match msg:
                case "START":
                    # acquire lock to increment number in the array.
                    with num_start_clicks_lock:
                        num_start_clicks[0] += 1

                        # if both players have incremented the number in the 
                        # array than both players are ready to start.
                        if num_start_clicks[0] == 2:
                            # send ready message to both players.
                            conn1.send(str.encode("READY:"))
                            conn2.send(str.encode("READY:"))

                case click if msg.startswith("CLICK:"):
                    # determine if valid click
                    click = eval(msg[len("CLICK:"):])
                    if board.click(click, playerColor):
                        # send coordinates back to the player that clicked. 
                        conn1.send(str.encode("CLICKED:" + str(click) + '|'))

                case move if msg.startswith("MOVE:"):
                    move = msg[len("MOVE:"):]
                    start, end = eval(move)

                    # give player coordinates to board to determine if it's a 
                    # valid move.
                    piece = board.move(start, end, playerColor)

                    # if a piece is returned that means it is a valid move.
                    if piece:
                        cooldown_str = board.get_cooldown_string(end)

                        # NOTE: the string representation of the piece is sent 
                        # to the player but the player never does anything with 
                        # it. This is because we returned the piece to do click 
                        # and drag but were unable to implement it in time 
                        # before the final submission deadline. 

                        # send the end coordinates, cooldown string and piece 
                        # image to player 1
                        conn1.send(str.encode("END:" + str(end)       + ':' 
                                                     + cooldown_str   + ':' 
                                                     + str(piece)     + '|'))

                        # send the end coordinates to player 2.
                        conn2.send(str.encode("END-OTHER:" + str(end) + '|'))

                    # get the current state of the board as a string and send it
                    # to both players
                    tosend = (board.grid_to_string())
                    conn1.send(str.encode(str(tosend) + '|'))
                    conn2.send(str.encode(str(tosend) + '|'))

                case "PAUSE":
                    conn1.send(str.encode("PAUSED:"))
                    conn2.send(str.encode("PAUSED-OTHER:"))

                case "RESUME":
                    with num_start_clicks_lock:
                        num_start_clicks[0] += 1
                        # check if both players have clicked resume
                        if num_start_clicks[0] % 2 == 0:
                            conn1.send(str.encode("RESUME:"))
                            conn2.send(str.encode("RESUME:"))

                case "QUIT":
                    # send quit message, close the connection
                    conn1.send(str.encode("Quit" + '|'))
                    conn1.close()
                    break
            
        except Exception as e:
            # if error with recieving messages break from the client loop.
            print("Error processing messages in server: ", e)
            conn1.close()
            break

if __name__ == '__main__':
    main()