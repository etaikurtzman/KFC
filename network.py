'''
network.py
contains implementation for network class
handles communication between the player and the server
4/29
'''

import socket

class Network:
    """
    A class to represent the socket client-server connection for a player

    Members
    -------
    client: socket
        socket to host the connection

    cooldown: str
        the player color that this network hosts

    Functions
    ---------
    get_color():
        get the player color associated with this network
    
    receive():
        receive a message from the server
    
    send_move(move):
        send a move to the server

    send_click(start):
        send a click to the server
    
    send_quit():
        send quit message to the server
    
    send_start():
        send start message to the server

    """
    def __init__(self, host):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, 5555))
        self.color = self.receive()
        
    def get_color(self):
        """
        Gets the network's color

        Returns
        -------
        string representing the user's color
        """
        return self.color

    def receive(self):
        """
        Waits until a message is sent from the server, then returns that
        message.

        Returns
        -------
        string representing the decoded message
        """
        try:
            return self.client.recv(2048).decode()
        except:
            print("Network error: unable to connect")
    
    def send_move(self, move):
        """
        Sends a move message to the server.

        Parameters
        ----------
        move : str
            The move's data as a string (tuples containing the start and end
            coordinates)
        """
        self.client.send(str.encode("MOVE:" + move))
        
    def send_click(self, start):
        """
        Sends a click message to the server.

        Parameters
        ----------
        start : str
            The click's data as a string (a tuple containing the click's
            coordinates)
        """
        self.client.send(str.encode("CLICK:" + start))
    
    def send_quit(self):
        """
        Sends a quit message to the server.
        """
        self.client.send(str.encode("QUIT"))

    def send_start(self):
        """
        Sends a start message to the server.
        """
        self.client.send(str.encode("START"))
    
    def send_pause(self):
        """
        Sends a pause message to the server.
        """
        self.client.send(str.encode("PAUSE"))
    
    def send_resume(self):
        """
        Sends a resume message to the server.
        """
        self.client.send(str.encode("RESUME"))