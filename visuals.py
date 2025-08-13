import math
import pygame
import colorsys

def smooth_pulsing_green(beat_phase, x=0, y=0):
    base_hue = 0.33
    hue = base_hue + 0.06 * math.sin(2 * math.pi * (beat_phase + x/400. + y/300.))
    val = 0.6 + 0.35 * math.sin(2 * math.pi * beat_phase)
    r, g, b = colorsys.hsv_to_rgb(hue % 1.0, 1, val)
    return (int(r*255), int(g*255), int(b*255))

def draw_pitch(screen, beat_phase, rave_mode, width, height):
    if not rave_mode:
        for y in range(0, height, 8):
            for x in range(0, width, 8):
                col = smooth_pulsing_green(beat_phase, x, y)
                pygame.draw.rect(screen, col, (x, y, 8, 8))
    else:
        for y in range(0, height, 8):
            for x in range(0, width, 8):
                hue = ((pygame.time.get_ticks() / 350.0) + (x + y)/280.) % 1.0
                r,g,b = [int(x*255) for x in colorsys.hsv_to_rgb(hue, 1, 1)]
                pygame.draw.rect(screen, (r,g,b), (x, y, 8,8))

def draw_rave_effects(screen, width, height):
    # Stadium lighting overlays/ellipses
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    light_int = int(50 + 45 * math.sin(pygame.time.get_ticks()/80))
    pygame.draw.ellipse(overlay, (255,255,255,light_int), [width//2-450,height//3-80,900,140])
    pygame.draw.ellipse(overlay, (255,255,100,int(light_int*1.5)), [width//2-250, height//2, 500,90])
    screen.blit(overlay, (0,0))
    # Confetti/sparkles
    for i in range(32):
        t = (pygame.time.get_ticks() + i*60) / 120.0
        x_pos = int((math.sin(t)+1)*width*0.5)
        y_pos = int((math.cos(t+i)+1)*height*0.5)
        confetti_hue = ((pygame.time.get_ticks()/150.0)+i*0.075)%1.0
        r,g,b = [int(j*255) for j in colorsys.hsv_to_rgb(confetti_hue,0.7,1)]
        pygame.draw.circle(screen, (r,g,b), (x_pos, y_pos), random.randint(2,4))

def draw_banner(screen, font, width, show_banner):
    if show_banner > 0:
        banner = pygame.Surface((width, 80), pygame.SRCALPHA)
        pygame.draw.rect(banner, (0,255,236,180), banner.get_rect(), border_radius=30)
        rave_text = font.render("RAVE MODE!", True, (255, 255, 255))
        banner.blit(rave_text, ((width - rave_text.get_width())//2, 18))
        screen.blit(banner, (0, 48))

def draw_bpm(screen, font, bpm, width):
    bpm_col = (80,255,80) if bpm < 90 else (255,140,0) if bpm > 130 else (255,255,255)
    bpm_surf = font.render(f"BPM: {bpm}", True, bpm_col)
    screen.blit(bpm_surf, (width-bpm_surf.get_width()-40, 22))
