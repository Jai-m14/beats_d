import os
import pygame

def song_selection_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Select Song")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    browser_upload_dir = "/browserfs"
    default_songs_dir = "songs"

    songs = []

    # Uploaded songs
    if os.path.exists(browser_upload_dir):
        for f in sorted(os.listdir(browser_upload_dir)):
            if f.lower().endswith(".mp3"):
                songs.append((f, os.path.join(browser_upload_dir, f)))

    # Default songs
    if os.path.exists(default_songs_dir):
        for f in sorted(os.listdir(default_songs_dir)):
            if f.lower().endswith(".mp3"):
                songs.append((f, os.path.join(default_songs_dir, f)))

    if not songs:
        display_list = ["(No songs found — please upload one)"]
    else:
        display_list = [name for name, _ in songs]

    selected_index = 0
    running = True

    while running:
        screen.fill((30, 30, 30))

        for i, name in enumerate(display_list):
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            screen.blit(font.render(name, True, color), (50, 50 + 40 * i))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and songs:
                    selected_index = (selected_index + 1) % len(display_list)
                elif event.key == pygame.K_UP and songs:
                    selected_index = (selected_index - 1) % len(display_list)
                elif event.key == pygame.K_RETURN:
                    if not songs or display_list[selected_index].startswith("("):
                        break
                    return songs[selected_index][1]  # return full path

        clock.tick(30)

    pygame.quit()
    return None
