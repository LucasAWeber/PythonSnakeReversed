# Snake Game Reversed
# June 2021
# ShockingRotom

# Press arrow keys to control the apple and avoid the snake (try to outlast the snake!)

import pygame
import random
import time
from extra import apple_library, segment_library

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15
# Margin between each segment
segment_margin = 3
# Speed/frames
game_speed = 25

# Determines the previous highscore
save = open(r"extra/Highscore.txt", "r").read()
previous_score = int(save)

# Set initial speed randomly (so snake can start going in any direction
# Also sets the snake_direction variable accordingly
if random.randrange(2) == 1:
    x_change_snake = random.choice([-1, 1]) * (segment_width + segment_margin)
    y_change_snake = 0
    if x_change_snake > 0:
        snake_direction = "right"
    else:
        snake_direction = "left"
else:
    x_change_snake = 0
    y_change_snake = random.choice([-1, 1]) * (segment_height + segment_margin)
    if y_change_snake > 0:
        snake_direction = "down"
    else:
        snake_direction = "up"

# Set initial speed randomly (so snake can start going in any direction
if random.randrange(2) == 1:
    x_change_apple = random.choice([-1, 1]) * (segment_width + segment_margin)
    y_change_apple = 0
else:
    x_change_apple = 0
    y_change_apple = random.choice([-1, 1]) * (segment_height + segment_margin)


# Segment add function is called whenever the snake grows
def segment_add(x, y):
    segment = segment_library.Segment(x, y, snake_direction)
    snake_segments.append(segment)
    allspriteslist.add(segment)


# Function that draws the ui or stats during the game
def ui_draw(screen, game_clock, highscore):
    # Draw the white boarders
    pygame.draw.rect(screen, WHITE, (0, 528, 800, 72))
    pygame.draw.rect(screen, WHITE, (0, 0, 1, 600))
    pygame.draw.rect(screen, WHITE, (0, 0, 800, 1))
    pygame.draw.rect(screen, WHITE, (799, 0, 1, 600))

    # Create the text

    txthighscore = myfont.render("Highscore: " + str(highscore), 1, BLACK)
    txtcurrenttime = myfont.render("Time: " + str(game_clock), 1, BLACK)

    # Draws the text to the screen
    screen.blit(txtcurrenttime, (20, 534))
    screen.blit(txthighscore, (470, 534))


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

# Creates font
myfont = pygame.font.SysFont('Comic Sans MS', 40, True)

# Set the title of the window
pygame.display.set_caption('Snake')

allspriteslist = pygame.sprite.Group()

# Create an initial snake (head)
snake_segments = []

# The x and y locations are randomized along a grid for the initial
segment_x = 4 + random.randrange(2, 43) * (segment_width + segment_margin) + len(snake_segments) * x_change_snake
segment_y = 4 + random.randrange(2, 28) * (segment_height + segment_margin) + len(snake_segments) * y_change_snake
segment_add(segment_x, segment_y)
segment_add(segment_x, segment_y)

# Creates apple
apple = apple_library.Apple(segment_margin, segment_width, segment_height, RED)
allspriteslist.add(apple)

clock = pygame.time.Clock()
done = False
growing = False
growing_start = 0
snake_move = True
snake_move_start = 0

# Gets the time when the game first starts
game_start_time = time.time()

game_tick = 0

winner = None

while not done:

    # Closes game when user presses quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        # We also keep track of the direction we are going for rotation purposes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change_apple = (segment_width + segment_margin) * -1
                y_change_apple = 0
            if event.key == pygame.K_RIGHT:
                x_change_apple = (segment_width + segment_margin)
                y_change_apple = 0
            if event.key == pygame.K_UP:
                x_change_apple = 0
                y_change_apple = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change_apple = 0
                y_change_apple = (segment_height + segment_margin)

    # Figure out where new segment will be
    x_apple = apple.rect.x + x_change_apple
    y_apple = apple.rect.y + y_change_apple

    # Checks if the segment is going off screen
    if x_apple < 4 or x_apple > 780 or y_apple < 4 or y_apple > 520:
        winner = "snake"
        done = True

    apple.rect.x = x_apple
    apple.rect.y = y_apple

    if snake_move:
        # snake movement
        if snake_segments[0].rect.x > x_apple and snake_direction != "right":
            snake_direction = "left"
        elif snake_segments[0].rect.x < x_apple and snake_direction != "left":
            snake_direction = "right"
        elif snake_segments[0].rect.y < y_apple and snake_direction != "up":
            snake_direction = "down"
        elif snake_segments[0].rect.y > y_apple and snake_direction != "down":
            snake_direction = "up"

        if snake_direction == "left":
            x_change_snake = (segment_width + segment_margin) * -1
            y_change_snake = 0
        if snake_direction == "right":
            x_change_snake = (segment_width + segment_margin)
            y_change_snake = 0
        if snake_direction == "up":
            x_change_snake = 0
            y_change_snake = (segment_height + segment_margin) * -1
        if snake_direction == "down":
            x_change_snake = 0
            y_change_snake = (segment_height + segment_margin)

        # Replace current head with body so it can create the new head thats moved over
        snake_segments[0].head_swap(screen)

        # Figure out where new segment will be
        x_snake = snake_segments[0].rect.x + x_change_snake
        y_snake = snake_segments[0].rect.y + y_change_snake

        # Checks if the segment is going off screen
        if x_snake < 4 or x_snake > 780 or y_snake < 4 or y_snake > 520:
            winner = "YOU"
            done = True

        # Create an instance and add it to the lists
        segment = segment_library.Segment(x_snake, y_snake, snake_direction)

        # Insert new segment into the list
        snake_segments.insert(0, segment)
        allspriteslist.add(segment)

    # Checks collision against the apple
    if pygame.sprite.spritecollide(apple, snake_segments, False):
        winner = "snake"
        done = True

    if snake_move:
        if not growing:
            growing_start = time.time()
            growing = True
        elif time.time() - growing_start >= 1:
            segment_add(0, 0)
            growing = False

    # These are all things I want to happen as long as there are more than 1 snake segment
    if len(snake_segments) > 1:
        # Checks collision against the front segment and the rest of the snake, ends game if they have made contact
        # I make copy of original list so I can pop off first segment (head)
        # So we can compare the head to every OTHER segment
        col_check_list = snake_segments.copy()
        col_check_list.pop(0)
        if pygame.sprite.spritecollide(snake_segments[0], col_check_list, False):
            winner = "YOU"
            done = True

    if snake_move:
        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        old_segment = snake_segments.pop()
        allspriteslist.remove(old_segment)

        # This has to be separated from the collision check above because collision must be checked before the last
        # segment
        # Is removed and this code needs to be ran after the last segment was popped off
        if len(snake_segments) > 1:
            # This determines the rotation of the tail
            # Takes the location of the tail and segment beside the tail and compares them determining the rotation of
            # tail
            # So the sprite looks connected
            if snake_segments[-1].rect.x - snake_segments[-2].rect.x > 0:
                segment_rotation = -90
            elif snake_segments[-1].rect.x - snake_segments[-2].rect.x < 0:
                segment_rotation = 90
            elif snake_segments[-1].rect.y - snake_segments[-2].rect.y > 0:
                segment_rotation = 180
            else:
                segment_rotation = 0
            # Calls the tail function that will turn the last segment into tail and passes in the rotation of image
            snake_segments[-1].body_swap(screen, segment_rotation)

            snake_move = False
            snake_move_start = game_tick
    else:
        if game_tick != snake_move_start:
            snake_move = True

    # Determines the time the game has been running
    game_time = int(time.time() - game_start_time)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)
    allspriteslist.draw(screen)
    ui_draw(screen, game_time, previous_score)

    # Game tick
    game_tick += 1

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(game_speed)

# Determining your current score for this play through and your previous high score saved in the txt file
# Compares the two values to determine your new high score and saves it to the txt file to be loaded next play through
# If the user presses the STOP button within the IDE it will close the game prematurely without being able to save data
current_score = game_time
if current_score > previous_score:
    high_score = current_score
else:
    high_score = previous_score
save = open(r"extra/Highscore.txt", "w")
save.write(str(high_score))
save.close()

# End screen where the scores are displayed
# Clear screen
screen.fill(BLACK)

# Creates the text
txtWinner = myfont.render(str(winner) + " won!", 1, WHITE)
txtCurrentScore = myfont.render("You lasted a total of " + str(current_score) + " seconds!", 1, WHITE)
txtPreviousScore = myfont.render("You previously lasted " + str(previous_score) + " seconds!", 1, WHITE)
txtHighscore = myfont.render("Your highscore is now " + str(high_score) + " seconds!", 1, WHITE)

# Displays/Blits text to screen
screen.blit(txtWinner, (300, 25))
screen.blit(txtCurrentScore, (75, 125))
screen.blit(txtPreviousScore, (75, 200))
screen.blit(txtHighscore, (75, 275))

# Flip screen
pygame.display.flip()

# Keeps the display on the screen until the user closes window
while done:
    # Closes game when user presses quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

pygame.quit()
