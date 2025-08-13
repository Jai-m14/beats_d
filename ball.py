import pygame
from config import BALL_RADIUS, BALL_COLOR

def draw_spotlight(screen, pos, color, intensity=1.0, radius=6):
    s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    for i in range(radius, 0, -2):
        alpha = int(60 * intensity * (i / radius))
        col = (*color, alpha)
        pygame.draw.circle(s, col, (radius, radius), i)
    screen.blit(s, (int(pos[0])-radius, int(pos[1])-radius), special_flags=pygame.BLEND_RGBA_ADD)

class Ball:
    def __init__(self, pos):
        self.pos = list(pos)
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR
        self.last_strobe_pos = None
        self.strobe_timer = 0
        self.trail = []
    def draw(self, screen):
        trail_length = 10
        for i, pos in enumerate(self.trail[-trail_length:]):
            alpha = int(90 * (i+1) / trail_length)
            color = (*self.color, alpha)
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (self.radius, self.radius), self.radius)
            screen.blit(s, (int(pos[0])-self.radius, int(pos[1])-self.radius))
        pygame.draw.circle(screen, self.color, [int(x) for x in self.pos], self.radius)
        draw_spotlight(screen, self.pos, (255,240,90), intensity=1.0, radius=self.radius+2)
