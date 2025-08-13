import pygame
import math
import colorsys
import random

def draw_rave_pitch(screen, width, height):
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            hue = ((pygame.time.get_ticks() / 350.0) + (x + y) / 280.) % 1.0
            r, g, b = [int(i * 255) for i in colorsys.hsv_to_rgb(hue, 1, 1)]
            pygame.draw.rect(screen, (r, g, b), (x, y, 8, 8))

def draw_rave_overlays(screen, width, height):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    light_intensity = int(50 + 45 * math.sin(pygame.time.get_ticks() / 80))
    pygame.draw.ellipse(overlay, (255, 255, 255, light_intensity),
                        [width // 2 - 450, height // 3 - 80, 900, 140])
    pygame.draw.ellipse(overlay, (255, 255, 100, int(light_intensity * 1.5)),
                        [width // 2 - 250, height // 2, 500, 90])
    screen.blit(overlay, (0, 0))

def draw_rave_confetti(screen, width, height):
    for i in range(32):
        t = (pygame.time.get_ticks() + i * 60) / 120.0
        x_pos = int((math.sin(t) + 1) * width * 0.5)
        y_pos = int((math.cos(t + i) + 1) * height * 0.5)
        confetti_hue = ((pygame.time.get_ticks() / 150.0) + i * 0.075) % 1.0
        r, g, b = [int(j * 255) for j in colorsys.hsv_to_rgb(confetti_hue, 0.7, 1)]
        pygame.draw.circle(screen, (r, g, b), (x_pos, y_pos), random.randint(2, 4))

def set_rave_players(players, PLAYER_RADIUS):
    for i, ply in enumerate(players):
        target_radius = int(PLAYER_RADIUS * 2.5)
        prev_rad = getattr(ply, "radius", PLAYER_RADIUS)
        if prev_rad < target_radius:
            ply.radius = min(prev_rad + 2, target_radius)
        elif prev_rad > target_radius:
            ply.radius = max(prev_rad - 2, target_radius)
        else:
            ply.radius = target_radius
        hue = ((pygame.time.get_ticks() / 250.0) + i * 0.19) % 1.0
        r, g, b = [int(k * 255) for k in colorsys.hsv_to_rgb(hue, 1, 1)]
        ply.color = (r, g, b)
        
def set_rave_ball(ball):
    ball.color = [int(x * 255) for x in colorsys.hsv_to_rgb((pygame.time.get_ticks() / 250.0) % 1.0, 1, 1)]

def draw_rave_banner(screen, font, width, banner_timer):
    if banner_timer > 0:
        banner = pygame.Surface((width, 80), pygame.SRCALPHA)
        pygame.draw.rect(banner, (0, 255, 236, 180), banner.get_rect(), border_radius=30)
        rave_text = font.render("RAVE MODE!", True, (255, 255, 255))
        banner.blit(rave_text, ((width - rave_text.get_width()) // 2, 18))
        screen.blit(banner, (0, 48))
