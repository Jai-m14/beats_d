import random
from config import WIDTH, HEIGHT, MARGIN, GOAL_WIDTH, TEAM1_COLOR, TEAM2_COLOR
from player import Player

def init_team(color, left_to_right):
    ylines = [MARGIN+GOAL_WIDTH//2, HEIGHT//2-150, HEIGHT//2, HEIGHT//2+150, HEIGHT-MARGIN-GOAL_WIDTH//2]
    lineup = []
    if left_to_right:
        xcols = [MARGIN+80, MARGIN+180, WIDTH//2-70, WIDTH//2+20, WIDTH-MARGIN-80]
    else:
        xcols = [WIDTH-MARGIN-80, WIDTH-MARGIN-180, WIDTH//2+70, WIDTH//2-20, MARGIN+80]
    lineup.append(Player((xcols[0], HEIGHT//2), color))
    for i in range(4):
        y = ylines[i+1]
        lineup.append(Player((xcols[1], y), color))
    lineup.append(Player((xcols[2], HEIGHT//2-70), color))
    lineup.append(Player((xcols[2], HEIGHT//2+70), color))
    lineup.append(Player((xcols[3], ylines[0]), color))
    lineup.append(Player((xcols[3], ylines[-1]), color))
    for i in range(2):
        y = HEIGHT//2-70+140*i
        lineup.append(Player((xcols[4], y), color))
    return lineup

def get_bpm(current_beat_idx, beat_times, N=8):
    if current_beat_idx < N:
        return 0
    interval = (beat_times[current_beat_idx] - beat_times[current_beat_idx-N]) / N
    if interval == 0:
        return 0
    bpm = 60.0 / interval
    return int(bpm)
