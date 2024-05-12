from cs1lib import *
import random

# Initialization of variables
WIND_SIZE = 600
HEIGHT_P_Y = 80
WIDTH_P_X = 20
B_SIZE = 5

b_vx, b_vy = 0, 0
bx, by = WIND_SIZE // 2, WIND_SIZE // 2
left_pad_y = right_pad_y = WIND_SIZE // 2 - HEIGHT_P_Y // 2

# Checking the paddles for the four keys
left_pad_up = left_pad_down = False
right_pad_up = right_pad_down = False

# For starting the game
start_game = False

# Speed of going up and down
MOVE = 5

# Initialization of score variables
score_player_1 = 0
score_player_2 = 0
game_over = False

# Initialization of variables for the second ball
second_ball_active = False
bx2, by2, b_vx2, b_vy2 = WIND_SIZE // 2, WIND_SIZE // 2, 0, 0
hit_count = 0

# Drawing ball
def draw_ball():
    set_fill_color(1, 1, 1)
    draw_circle(bx, by, B_SIZE)
    if second_ball_active:
        draw_circle(bx2, by2, B_SIZE)


# Updating ball
def update_ball():
    global bx, by, b_vx, b_vy, bx2, by2, b_vx2, b_vy2, start_game, second_ball_active

    if start_game:
        # Update and check collision for the first ball
        bx += b_vx
        by += b_vy
        paddle_collision(bx, by)

        # Update and check collision for the second ball if active
        if second_ball_active:
            bx2 += b_vx2
            by2 += b_vy2
            paddle_collision(bx2, by2)

        # Check for wall collisions
        wall_collision()

        # Check if the ball goes out of bounds to reset the game
        if bx <= 0 or bx >= WIND_SIZE or (second_ball_active and (bx2 <= 0 or bx2 >= WIND_SIZE)):
            reset_game()

# Drawing paddles
def draw_paddle():
    global left_pad_y, right_pad_y
    set_fill_color(0.9, 0, 0.1)
    draw_rectangle(0, left_pad_y, WIDTH_P_X, HEIGHT_P_Y)
    draw_rectangle(WIND_SIZE - WIDTH_P_X, right_pad_y, WIDTH_P_X, HEIGHT_P_Y)

    if right_pad_up and right_pad_y > 0:
        right_pad_y -= MOVE
    if right_pad_down and right_pad_y + HEIGHT_P_Y < WIND_SIZE:
        right_pad_y += MOVE
    if left_pad_up and left_pad_y > 0:
        left_pad_y -= MOVE
    if left_pad_down and left_pad_y + HEIGHT_P_Y < WIND_SIZE:
        left_pad_y += MOVE
def paddle_collision(ball_x, ball_y):
    global b_vx, b_vy, b_vx2, b_vy2, hit_count, second_ball_active, bx, by, bx2, by2

    # Handle collision for the first ball
    if ball_x == bx and ball_y == by:
        # Collision with left paddle
        if bx - B_SIZE <= WIDTH_P_X and left_pad_y <= by <= left_pad_y + HEIGHT_P_Y:
            b_vx *= -1
            bx = WIDTH_P_X + B_SIZE  # Position the ball just outside the left paddle
            hit_count += 1
        # Collision with right paddle
        elif bx + B_SIZE >= WIND_SIZE - WIDTH_P_X and right_pad_y <= by <= right_pad_y + HEIGHT_P_Y:
            b_vx *= -1
            bx = WIND_SIZE - WIDTH_P_X - B_SIZE  # Position the ball just outside the right paddle
            hit_count += 1

    # Handle collision for the second ball, if active
    if second_ball_active and ball_x == bx2 and ball_y == by2:
        # Collision with left paddle
        if bx2 - B_SIZE <= WIDTH_P_X and left_pad_y <= by2 <= left_pad_y + HEIGHT_P_Y:
            b_vx2 *= -1
            bx2 = WIDTH_P_X + B_SIZE  # Position the ball just outside the left paddle
        # Collision with right paddle
        elif bx2 + B_SIZE >= WIND_SIZE - WIDTH_P_X and right_pad_y <= by2 <= right_pad_y + HEIGHT_P_Y:
            b_vx2 *= -1
            bx2 = WIND_SIZE - WIDTH_P_X - B_SIZE  # Position the ball just outside the right paddle

    # Check for second ball activation
    if hit_count >= 7 and not second_ball_active:
        second_ball_active = True
        bx2, by2 = bx, by  # Start second ball at the position of the first ball
        b_vx2 = random.choice([-3, -2, 2, 3])  # Choose a random speed and direction
        b_vy2 = random.choice([-3, -2, 2, 3])  # Choose a random speed and direction.


# Wall collision
def wall_collision():
    global by, b_vy, by2, b_vy2

    # Collision for the first ball
    if by - B_SIZE <= 0 or by + B_SIZE >= WIND_SIZE:
        b_vy *= -1

    # Collision for the second ball
    if second_ball_active and (by2 - B_SIZE <= 0 or by2 + B_SIZE >= WIND_SIZE):
        b_vy2 *= -1

# Key press functions
def kpressed_down(value):
    global left_pad_down, left_pad_up, right_pad_up, right_pad_down, start_game, b_vx, b_vy
 # it can be either of these two letters
    if value in ["a", "A"]:
        left_pad_up = True
    elif value in ["z", "Z"]:
        left_pad_down = True
    elif value in ["k", "K"]:
        right_pad_up = True
    elif value in ["m", "M"]:
        right_pad_down = True
    elif value == " ":
        if game_over:
            restart_game()
        elif not start_game:
            start_game = True
            b_vx, b_vy = 4, 4  # Setting initial ball speed
    elif value in ["q", "Q"]:
        cs1_quit()  # Quit function

def kpressed_up(value):
    global right_pad_up, right_pad_down, left_pad_down, left_pad_up

    if value in ["a", "A"]:
        left_pad_up = False
    elif value in ["k", "K"]:
        right_pad_up = False
    elif value in ["m", "M"]:
        right_pad_down = False
    elif value in ["z", "Z"]:
        left_pad_down = False

# Reset the game and update scores
def reset_game():
    global bx, by, b_vx, b_vy, start_game, score_player_1, score_player_2, game_over, second_ball_active, hit_count, bx2, by2, b_vx2, b_vy2

    if not game_over:
        # Update scores based on who scored
        if bx <= 0:  # Player 2 scored
            score_player_2 += 1
        elif bx >= WIND_SIZE:  # Player 1 scored
            score_player_1 += 1

        # Check for win condition
        if score_player_1 >= 10 or score_player_2 >= 10:
            game_over = True

    # Resetting ball to center and deactivating the second ball
    bx, by = WIND_SIZE // 2, WIND_SIZE // 2
    b_vx, b_vy = 0, 0
    second_ball_active = False
    bx2, by2 = WIND_SIZE // 2, WIND_SIZE // 2
    b_vx2, b_vy2 = 0, 0
    hit_count = 0
    start_game = False

def restart_game():
    global score_player_1, score_player_2, game_over
    score_player_1 = 0
    score_player_2 = 0
    game_over = False
def draw_scores():
    set_font_size(16)
    set_stroke_color(1, 1, 1)  # White color
    set_fill_color(1, 1, 1)    # White color

    if not game_over:
        draw_text("Player 1: " + str(score_player_1), 50, 30)
        draw_text("Player 2: " + str(score_player_2), WIND_SIZE - 150, 30)
    else:
        win_text = "Player 1 wins!" if score_player_1 >= 10 else "Player 2 wins!"
        draw_text(win_text, WIND_SIZE // 2 - get_text_width(win_text) // 2, WIND_SIZE // 2 - 20)
        draw_text("Press Space to Restart", WIND_SIZE // 2 - get_text_width("Press Space to Restart") // 2,
                  WIND_SIZE // 2 + 20)
# Main draw function
def main_draw():
    set_clear_color(0, 0, 0)
    clear()
    draw_paddle()
    draw_ball()
    update_ball()
    draw_scores()
    if not start_game:
        set_font_size(16)
        set_stroke_color(1, 1, 1)  # White color
        set_fill_color(1, 1, 1)  # White color for t
        text = "Press Space to Start"
        text_width = get_text_width(text)
        text_x = WIND_SIZE // 2 - text_width // 2
        text_y = WIND_SIZE // 2 + 30
        draw_text(text, text_x, text_y)

# Start the graphics
start_graphics(main_draw, key_press=kpressed_down, key_release=kpressed_up, width=WIND_SIZE, height=WIND_SIZE)
