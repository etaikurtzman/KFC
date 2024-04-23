import pygame

class Piece:
    def __init__(self, color):
        self.color = color
        self.lastMoved = None # last time the piece was moved
        self.cooldown = 3.0 # cooldown of the piece in seconds
        # self.x
        # self.y
    def updateTimer(self, time):
        self.lastMoved = time

    def movedRecently(self, time):
        if self.lastMoved:
            #print(time - self.lastMoved)
            return time - self.lastMoved < self.cooldown
        return False
    
    def getCooldown(self):
        return self.cooldown