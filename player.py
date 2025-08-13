import pygame
from config import PLAYER_RADIUS

class Player:
    def __init__(self, pos, color):
        self.pos = list(pos)
        self.home = tuple(pos)
        self.start_pos = list(pos)
        self.dest = list(pos)
        self.color = color
        self.radius = PLAYER_RADIUS
        self.strobe = 0
    def set_dest(self, dest):
        self.start_pos = self.pos[:]
        self.dest = list(dest)
    def update(self, t):
        self.pos[0] = self.start_pos[0] + (self.dest[0] - self.start_pos[0]) * t
        self.pos[1] = self.start_pos[1] + (self.dest[1] - self.start_pos[1]) * t
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        if self.strobe > 0:
            pygame.draw.circle(screen, (255, 240, 60), (int(self.pos[0]), int(self.pos[1])), self.radius+5, 2)
            self.strobe -= 1
