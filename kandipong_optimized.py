from kandinsky import *
from ion import *
import time, random
import kandipongMenu

# hardware / implementation specifics
SCREEN_SIZE : tuple[int, int] = (320, 222)
CHARACTER_WIDTH = 8

# colors
COLOR_NEAR_BLACK : tuple[int, int, int] = (25, 25, 25)
COLOR_NEAR_WHITE : tuple[int, int, int] = (225, 225, 225)

# other constants
FRAME_TIME : int = 40
BALL_RADIUS : int = 8

# object definitions
class Paddle:
    def __init__(self, position_x) -> None:
        self.position_x = position_x
        self.position = 111
        self.height   = 50
        self.width    = 8

        self.clear_position_x = position_x
        self.clear_position = self.position
        self.clear_height = self.height
        self.clear_width = self.width
        self.redraw_needed = False
    def draw(self) -> None:
        if self.redraw_needed:
            fill_rect(self.clear_position_x, int(self.clear_position - self.clear_height / 2), self.clear_width, self.clear_height, COLOR_NEAR_BLACK)
            self.clear_position_x = self.position_x
            self.clear_position = self.position
            self.clear_height = self.height
            self.clear_width = self.width
            self.redraw_needed = False
        fill_rect(self.position_x, int(self.position - self.height / 2), self.width, self.height, COLOR_NEAR_WHITE)

class Vector2:
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y
    def add(self, other):
        self.x += other.x
        self.y += other.y
    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
    def scale(self, scalar : float):
        self.x *= scalar
        self.y *= scalar
    def as_int(self) -> tuple[int, int]:
        return round(self.x), round(self.y)

# main
paddle_left = Paddle(2)
paddle_right = Paddle(SCREEN_SIZE[0] - 10)

ball_position : Vector2 = Vector2(160, 111)
ball_direction : Vector2 = Vector2(random.randint(0,1) * 2 - 1, random.randint(0,1) * 2 - 1)
ball_direction.scale(3.5)

pl_score = 0
pr_score = 0

# clear
fill_rect(0, 0, *SCREEN_SIZE, COLOR_NEAR_BLACK)
rounded_old_bp = (0,0)

scored = False

while 1:
    fb_time : int = int(time.monotonic() * 1000)
    rounded_bp = ball_position.as_int()
    
    # handle keys
    if keydown(KEY_MINUS):
        paddle_right.position += 10
        paddle_right.redraw_needed = True
    if keydown(KEY_DIVISION):
        paddle_right.position -= 10
        paddle_right.redraw_needed = True
    if keydown(KEY_FOUR):
        paddle_left.position += 10
        paddle_left.redraw_needed = True
    if keydown(KEY_ONE):
        paddle_left.position -= 10
        paddle_left.redraw_needed = True

    ## ball physics
    # collisions with the solid boundaries
    if (ball_position.y - BALL_RADIUS <= 0 and ball_direction.y < 0) or (ball_position.y + BALL_RADIUS >= SCREEN_SIZE[1] and ball_direction.y > 0):
        ball_direction.y *= -1
    # collisions with the paddles
    pll = int(paddle_left.position_x - paddle_left.width / 2) + BALL_RADIUS
    plr = int(paddle_left.position_x + paddle_left.width / 2) + BALL_RADIUS
    plt = int(paddle_left.position - paddle_left. height / 2) - BALL_RADIUS
    plb = int(paddle_left.position + paddle_left.height / 2) + BALL_RADIUS
    prl = int(paddle_right.position_x - paddle_right.width / 2) + BALL_RADIUS
    prr = int(paddle_right.position_x + paddle_right.width / 2) + BALL_RADIUS
    prt = int(paddle_right.position - paddle_right. height / 2) - BALL_RADIUS
    prb = int(paddle_right.position + paddle_right.height / 2) + BALL_RADIUS
    if (rounded_bp[1] in range(plt, plb) and rounded_bp[0] in range(pll, plr) and ball_direction.x < 0
    or rounded_bp[1] in range(prt, prb) and rounded_bp[0] in range(prl, prr) and ball_direction.x > 0):
        ball_direction.x *= -1
    # movement
    ball_position.add(ball_direction)

    # detect scoring
    if ball_position.x + BALL_RADIUS < 0:
        pr_score += 1
        scored = True
    if ball_position.x - BALL_RADIUS > SCREEN_SIZE[0]:
        pl_score += 1
        scored = True
    
    if scored:
        ball_position = Vector2(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
        rounded_bp = ball_position.as_int()
        paddle_left.position = int(SCREEN_SIZE[1] / 2)
        paddle_right.position = int(SCREEN_SIZE[1] / 2)
        ball_direction.x *= -1
        fill_rect(0, 0, *SCREEN_SIZE, COLOR_NEAR_BLACK)

    # draw paddles
    paddle_left.draw()
    paddle_right.draw()

    # draw net
    for i in range(int(SCREEN_SIZE[1] / 20)):
        fill_rect(int(SCREEN_SIZE[0] / 2) - 1, i * int(SCREEN_SIZE[1] / 10), 2, int(SCREEN_SIZE[1] / 20), COLOR_NEAR_WHITE)

    # draw ball
    fill_rect(rounded_old_bp[0] - BALL_RADIUS, rounded_old_bp[1] - BALL_RADIUS, BALL_RADIUS, BALL_RADIUS, COLOR_NEAR_BLACK)
    fill_rect(rounded_bp[0] - BALL_RADIUS, rounded_bp[1] - BALL_RADIUS, BALL_RADIUS, BALL_RADIUS, COLOR_NEAR_WHITE)
    
    # draw score
    draw_string(str(pr_score), round(SCREEN_SIZE[0] / 2) + 5, 0, COLOR_NEAR_WHITE, COLOR_NEAR_BLACK)
    draw_string(str(pl_score), round(SCREEN_SIZE[0] / 2) - (10 * len(str(pl_score))) - 5, 0, COLOR_NEAR_WHITE, COLOR_NEAR_BLACK)

    if scored:
        scored = False
        time.sleep(3)

    rounded_old_bp = rounded_bp

    fe_time : int = int(time.monotonic() * 1000)

    time.sleep(max(0, FRAME_TIME - (fe_time - fb_time)) / 1000)
