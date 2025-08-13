import asyncio
import pygame
import os
import math
import colorsys
import importlib
# subprocess is imported but subprocess.run is commented out below
#import subprocess
from config import *
from field import Field
from player import Player
from ball import Ball
from utils import init_team, get_bpm
from song_menu import song_selection_menu
from visuals import draw_pitch, draw_bpm
from player_manager import lerp_hsv, init_players, pulse_random_players, update_player_states
from game_logic import all_same_color, next_palette_color, handle_pass_and_color
from input_handlers import process_events
import rave


async def main():
      
    rave_mode = False
    rave_banner_timer = 0
    _last_pulse = -1000.0
    music_file = song_selection_menu()
    print(f"Analyzing {music_file} for beats...")
    # Commented out because blocking subprocess freezes async loop in browser
    # subprocess.run(["python", "analyze_and_save_beats.py", music_file], check=True)
    import beats
    importlib.reload(beats)
    beat_times = beats.beat_times

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rhythm Soccer Modularized")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)

    field = Field()
    blue_team = init_team(TEAM1_COLOR, True)
    red_team = init_team(TEAM2_COLOR, False)
    players = blue_team + red_team
    num_players = len(players)

    starter_color = (0, 255, 236)
    other_color = (255, 0, 0)
    starting_idx = 0
    NORMAL_RADIUS = PLAYER_RADIUS
    RAVE_RADIUS = int(PLAYER_RADIUS * 2.5)
    PULSE_MAGNITUDE = 0.30

    player_data = init_players(num_players, starter_color, other_color, NORMAL_RADIUS)
    ball = Ball(blue_team[0].pos[:])
    for p in players:
        p.set_dest(p.pos[:])
        p.radius = NORMAL_RADIUS

    current_idx = starting_idx
    next_idx = 1
    beat_index = 0
    cycling_started = False

    running = True
    while running:
        events = pygame.event.get()
        running, rave_mode, rave_banner_timer = process_events(events, rave_mode, rave_banner_timer)

        song_pos_ms = pygame.mixer.music.get_pos()
        song_time = max(0, song_pos_ms / 1000.0)
        if beat_index + 1 < len(beat_times):
            this_beat = beat_times[beat_index]
            next_beat = beat_times[beat_index + 1]
            beat_len = max(next_beat - this_beat, 1e-6)
            beat_phase = (song_time - this_beat) / beat_len
            beat_phase = max(0, min(beat_phase, 1))
        else:
            beat_phase = 1.0

        if rave_mode:
            rave.draw_rave_pitch(screen, WIDTH, HEIGHT)
            rave.draw_rave_overlays(screen, WIDTH, HEIGHT)
            rave.draw_rave_confetti(screen, WIDTH, HEIGHT)
            rave.set_rave_players(players, PLAYER_RADIUS)
            rave.set_rave_ball(ball)
            field.draw(screen)
            for p in players:
                p.draw(screen)
            ball.draw(screen)
            rave.draw_rave_banner(screen, font, WIDTH, rave_banner_timer)
        else:
            draw_pitch(screen, beat_phase, rave_mode, WIDTH, HEIGHT)
            _last_pulse = pulse_random_players(player_data, song_time, _last_pulse, num_players, 0.07)
            update_player_states(
                players, player_data, beat_phase, rave_mode, NORMAL_RADIUS, RAVE_RADIUS, PULSE_MAGNITUDE
            )
            ball.color = tuple(player_data[current_idx]["current_color"])
            field.draw(screen)
            for p in players:
                p.draw(screen)
            ball.draw(screen)

        if beat_index + 1 < len(beat_times):
            t = beat_phase
            rx, ry = players[next_idx].pos
            ox, oy = players[current_idx].pos
            ball.pos[0] = ox + (rx - ox) * t
            ball.pos[1] = oy + (ry - oy) * t

            for p in players:
                p.update(t)
            if song_time >= next_beat:
                (current_idx, next_idx, beat_index, cycling_started) = handle_pass_and_color(
                    player_data, players, beat_phase, beat_index, beat_times, cycling_started,
                    current_idx, next_idx, NORMAL_RADIUS
                )
                ball.last_strobe_pos = players[current_idx].pos[:]
                ball.strobe_timer = STROBE_MAX
                ball.trail = [tuple(ball.pos)]

        for idx, pos in enumerate(ball.trail):
            fade = idx / (len(ball.trail) or 1)
            color = tuple(player_data[current_idx]["current_color"])
            alpha = int(160 * (1 - fade))
            surf = pygame.Surface((ball.radius * 2, ball.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color, alpha), (ball.radius, ball.radius), ball.radius)
            screen.blit(surf, (pos[0] - ball.radius, pos[1] - ball.radius))
        if ball.strobe_timer > 0 and ball.last_strobe_pos is not None:
            field.draw_strobe_segment(screen, ball.last_strobe_pos, ball.radius)
            ball.strobe_timer -= 1

        draw_bpm(screen, font, get_bpm(beat_index, beat_times), WIDTH)
        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
