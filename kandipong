from kandinsky import *
from ion import *

SCREEN_SIZE : tuple[int, int] = (320, 222)
COLOR_NEAR_BLACK : tuple[int, int, int] = (25, 25, 25)
COLOR_NEAR_WHITE : tuple[int, int, int] = (225, 225, 225)
COLOR_GREY_LIGHT : tuple[int, int, int] = (128, 128, 128)
COLOR_GREY_DARK : tuple[int, int, int] = (80, 80, 80)

def draw_button(text : str, height : int, selected = False):
    fill_rect(int((SCREEN_SIZE[0] - 10 * len(text)) / 2) - 5, height, 10 * len(text) + 10, 30, COLOR_GREY_DARK if selected else COLOR_GREY_LIGHT)
    draw_string(text, int((SCREEN_SIZE[0] - 10 * len(text)) / 2), height + 5, COLOR_NEAR_BLACK, COLOR_GREY_LIGHT)

fill_rect(0, 0, *SCREEN_SIZE, COLOR_NEAR_BLACK)
draw_string("Pong", 140, 40, COLOR_NEAR_WHITE, COLOR_NEAR_BLACK)

draw_button("PLAY", 80, True)
draw_button("CREDITS", 150)

selected = 0
while 1:
    updated = False
    
    if keydown(KEY_DOWN) and selected == 0:
        selected = 1
        updated = True
    if keydown(KEY_UP) and selected:
        selected = 0
        updated = True
    
    if keydown(KEY_OK):
        if selected:
            fill_rect(0, 80, 320, 242, COLOR_NEAR_BLACK)
            draw_string(
"   Pong implementation for the\nNumworks calculator.\n\
    Distributed under the\nGNU GPL 2.0 lisence.\n\
    Made to teach programming\nto children.\n\
    Thanks to ... for the\nNumworks libraries on computer.", 0, 80, COLOR_NEAR_WHITE, COLOR_NEAR_BLACK)
            while not keydown(KEY_BACKSPACE):
                continue
            fill_rect(0, 80, 320, 242, COLOR_NEAR_BLACK)
            updated = True
        else:
            break

    if updated:
        draw_button("PLAY", 80, not bool(selected))
        draw_button("CREDITS", 150, bool(selected))
