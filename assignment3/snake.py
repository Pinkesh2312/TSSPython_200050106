import pygame
import sys
import time
import random

from pygame.constants import KEYDOWN

# initial game variables

# Window size
frame_size_x = 720
frame_size_y = 480

# Parameters for Snake
snake_pos = [100, 50]
snake_body = [[80, 50], [90, 50], [100, 50]]
direction = 'RIGHT'
change_to = direction

# Parameters for food
food_pos = [400, 300]
food_spawn = False

score = 0


# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()


def check_for_events():
    """
    This should contain the main for loop (listening for events). You should close the program when
    someone closes the window, update the direction attribute after input from users. You will have to make sure
    snake cannot reverse the direction i.e. if it turned left it cannot move right next.
    """
    global direction

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'


def update_snake():
    """
     This should contain the code for snake to move, grow, detect walls etc.
     """
    # Code for making the snake move in the expected direction
    global snake_body
    global snake_pos
    global direction
    global game_window
    global score
    global food_spawn

    if direction == 'RIGHT':
        snake_body.append([snake_pos[0]+10, snake_pos[1]])
        snake_pos[0] += 10
    if direction == 'LEFT':
        snake_body.append([snake_pos[0]-10, snake_pos[1]])
        snake_pos[0] -= 10
    if direction == 'UP':
        snake_body.append([snake_pos[0], snake_pos[1]-10])
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_body.append([snake_pos[0], snake_pos[1]+10])
        snake_pos[1] += 10

    if snake_pos[0] <= 10 or snake_pos[0] >= frame_size_x - 10 or snake_pos[1] <= 10 or snake_pos[1] >= frame_size_x - 10:
        game_over()

    for blocks in snake_body[:-1]:
        if pygame.Rect(snake_pos[0], snake_pos[1], 10, 10).colliderect(pygame.Rect(blocks[0], blocks[1], 10, 10)):
            game_over()


    if pygame.Rect(snake_pos[0], snake_pos[1], 10, 10).colliderect(food_pos[0], food_pos[1], 10, 10):
        food_spawn = True
        score += 10
    
    else:
        snake_body.pop(0)

    for part in snake_body:
        pygame.draw.rect(game_window, (255, 0, 0),
                         pygame.Rect(part[0], part[1], 9, 9))

    # Make the snake's body respond after the head moves. The responses will be different if it eats the food.
    # Note you cannot directly use the functions for detecting collisions
    # since we have not made snake and food as a specific sprite or surface.

    # End the game if the snake collides with the wall or with itself.


def create_food():
    """ 
    This function should set coordinates of food if not there on the screen. You can use randrange() to generate
    the location of the food.
    """
    global frame_size_x
    global frame_size_y
    global food_pos
    global food_spawn
    global game_window

    if food_spawn==True:
        food_pos = [random.randrange(20, frame_size_x - 20), random.randrange(20, frame_size_y - 20)]
        food_spawn = False
    
    pygame.draw.rect(game_window, (0, 140, 200), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

def show_score():
    """
    It takes in the above arguements and shows the score at the given pos according to the color, font and size.
    """
    global score
    global game_window
    global frame_size_y
    global frame_size_x

    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render(str(score), True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (frame_size_x/2, 40)
    game_window.blit(text, textRect)



def update_screen():
    """
    Draw the snake, food, background, score on the screen
    """

    game_window.fill((0, 0, 0))
    update_snake()
    create_food()
    show_score()
    pygame.display.flip()


def game_over():
    """ 
    Write the function to call in the end. 
    It should write game over on the screen, show your score, wait for 3 seconds and then exit
    """
    global score

    font1 = pygame.font.Font('freesansbold.ttf', 80)
    font2 = pygame.font.Font('freesansbold.ttf', 50)
    text1 = font1.render("GAME OVER !!!", True, (255, 0, 0), (0, 0, 0))
    text2 = font2.render("SCORE : " + str(score), True, (255, 0, 0), (0, 0, 0))
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect1.center = (frame_size_x/2, 150)
    textRect2.center = (frame_size_x/2, 350)
    game_window.blit(text1, textRect1)
    game_window.blit(text2, textRect2)

    pygame.display.update()
    time.sleep(3)
    sys.quit()



# Main loop
while True:
    # Make appropriate calls to the above functions so that the game could finally run

    check_for_events()
    update_screen()

    # To set the speed of the screen
    fps_controller.tick(25)
