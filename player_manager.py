import math
import random
import colorsys

def lerp_hsv(c1, c2, t):
    import colorsys
    hsv1 = colorsys.rgb_to_hsv(*(v/255. for v in c1))
    hsv2 = colorsys.rgb_to_hsv(*(v/255. for v in c2))
    h1,s1,v1 = hsv1
    h2,s2,v2 = hsv2
    dh = h2-h1
    if abs(dh)>0.5: h1 += 1.0 if dh < 0 else -1.0
    h = (h1+(h2-h1)*t)%1.0
    s = s1+(s2-s1)*t
    v = v1+(v2-v1)*t
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    return (int(r*255), int(g*255), int(b*255))

def init_players(num_players, starter_color, other_color, normal_radius):
    pdata = []
    for i in range(num_players):
        col = starter_color if i==0 else other_color
        pdata.append({
            "current_color": list(col),
            "target_color": list(col),
            "start_color": list(col),
            "transitioning": False,
            "radius": normal_radius
        })
    return pdata

def pulse_random_players(player_data, song_time, last_pulse, num_players, magnitude=0.07):
    if song_time - last_pulse > 0.42:
        nk = max(1, num_players//3)
        pulsing_indices = random.sample(range(num_players), k=nk)
        for idx in pulsing_indices:
            old_col = tuple(player_data[idx]["current_color"])
            h, s, v = colorsys.rgb_to_hsv(*(val / 255 for val in old_col))
            h = (h + 0.11 + random.uniform(-magnitude, magnitude)) % 1.0
            new_col = colorsys.hsv_to_rgb(h, 0.7 + 0.25*random.random(), v)
            target = [int(c * 255) for c in new_col]
            player_data[idx]["start_color"] = list(player_data[idx]["current_color"])
            player_data[idx]["target_color"] = list(target)
            player_data[idx]["transitioning"] = True
        return song_time
    return last_pulse

def update_player_states(players, player_data, beat_phase, rave_mode, NORMAL_RADIUS, RAVE_RADIUS, PULSE_MAGNITUDE):
    for i, ply in enumerate(players):
        pdata = player_data[i]
        if rave_mode:
            target_radius = RAVE_RADIUS
            prev_rad = getattr(ply, "radius", NORMAL_RADIUS)
            if prev_rad < target_radius:
                ply.radius = min(prev_rad + 2, target_radius)
            elif prev_rad > target_radius:
                ply.radius = max(prev_rad - 2, target_radius)
            else:
                ply.radius = target_radius
        else:
            beat_pulse = 1.0 + PULSE_MAGNITUDE * math.sin(beat_phase * math.pi)
            target_radius = int(NORMAL_RADIUS * beat_pulse)
            prev_rad = getattr(ply, "radius", NORMAL_RADIUS)
            if prev_rad < target_radius:
                ply.radius = min(prev_rad + 1, target_radius)
            elif prev_rad > target_radius:
                ply.radius = max(prev_rad - 1, target_radius)
            else:
                ply.radius = target_radius
        # Color transition:
        if pdata["transitioning"]:
            t = beat_phase
            if t >= 1.0:
                pdata["current_color"] = list(pdata["target_color"])
                pdata["transitioning"] = False
            else:
                pdata["current_color"] = list(lerp_hsv(pdata["start_color"], pdata["target_color"], t))
        ply.color = tuple(pdata["current_color"])
