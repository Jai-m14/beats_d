import random
from config import MARGIN, WIDTH, HEIGHT, STROBE_MAX

def all_same_color(clist):
    """Check if all RGB triplets in a list are equal."""
    return all(tuple(c) == tuple(clist[0]) for c in clist)

def next_palette_color(current):
    """
    Cycle to the next color in the palette after the given RGB color.
    If current is not found, return the first palette color.
    """
    palette = [
        (0, 255, 236),
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 90),
        (255, 0, 140)
    ]
    try:
        idx = palette.index(tuple(current))
        return palette[(idx + 1) % len(palette)]
    except ValueError:
        return palette[0]

def handle_pass_and_color(
    player_data, players, beat_phase, 
    beat_index, beat_times, cycling_started, 
    current_idx, next_idx, normal_radius
):
    """
    Handles color inheritance, beat-based passing, color cycling, and player randomization.

    Returns:
        current_idx, next_idx, beat_index, cycling_started
    """
    previous_idx = current_idx
    current_idx = next_idx
    prev_col = tuple(player_data[previous_idx]["current_color"])
    cur_col = tuple(player_data[current_idx]["current_color"])
    player_data[current_idx]["start_color"] = list(cur_col)
    player_data[current_idx]["target_color"] = list(prev_col)
    player_data[current_idx]["transitioning"] = True

    group_colors = [tuple(d["current_color"]) for d in player_data]
    if all_same_color(group_colors):
        newcol = next_palette_color(player_data[current_idx]["current_color"])
        player_data[current_idx]["start_color"] = list(player_data[current_idx]["current_color"])
        player_data[current_idx]["target_color"] = list(newcol)
        player_data[current_idx]["transitioning"] = True
        cycling_started = True
    elif cycling_started and not all_same_color(group_colors):
        cycling_started = False

    beat_index += 1

    num_players = len(players)
    next_idx = random.choice([i for i in range(num_players) if i != current_idx])
    for i, p in enumerate(players):
        d = 3 * p.radius if i == current_idx else 2 * p.radius
        dest = [
            min(max(p.home[0] + random.randint(-d, d), MARGIN + 10), WIDTH - MARGIN - 10),
            min(max(p.home[1] + random.randint(-d, d), MARGIN + 10), HEIGHT - MARGIN - 10)
        ]
        p.set_dest(dest)
    players[current_idx].strobe = STROBE_MAX
    return current_idx, next_idx, beat_index, cycling_started
