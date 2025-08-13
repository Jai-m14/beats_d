import pygame

def process_events(events, rave_mode, rave_banner_timer):
    running = True
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rave_mode = not rave_mode
                if rave_mode:
                    rave_banner_timer = 120
    return running, rave_mode, rave_banner_timer
