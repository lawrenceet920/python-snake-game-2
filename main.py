# Ethan Lawrence 
# Feb 12 2025
# Pygame template ver 2

import pygame
import sys
import random


# Window dimentions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Window Caption
TITLE = 'Snake Ver-2'

# Frame rate
FPS = 60
clock = pygame.time.Clock()
# Colors
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# snake constants
CELL_SIZE = 10
# Snake globals
direction = 1 # ^v<>
score = 0
clicked = False
# Generic Functions
def init_game():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    return screen
def handle_events():
        global direction
        global clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_w and direction != 2:
                    direction = 1
                if event.key == pygame.K_s and direction != 1:
                    direction = 2
                if event.key == pygame.K_a and direction != 4:
                    direction = 3
                if event.key == pygame.K_d and direction != 3:
                    direction = 4
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
        return True
def main():
    running = True
    # On Startup
    snake = [[int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2)]]
    snake.append([int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2) + CELL_SIZE*1])
    snake.append([int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2) + CELL_SIZE*2])
    snake.append([int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2) + CELL_SIZE*3])
    food = [0, 0]
    new_piece = [0, 0]
    new_food = True
    key_frame = 0
    game_over = False
    pause = False

    # Buttons
    font = pygame.font.SysFont('Arial', 40)
    buttons = {
        'resume_button' : {},
        'quit_button' : {}
    }
    buttons['resume_button']['rect'] = pygame.Rect(0, WINDOW_HEIGHT // 3, 200, 50)
    buttons['resume_button']['rect'].centerx = WINDOW_WIDTH // 2
    buttons['resume_button']['text'] = font.render('RESUME', True, WHITE)
    buttons['resume_button']['text rect'] = buttons['resume_button']['text'].get_rect(center=buttons['resume_button']['rect'].center)

    buttons['quit_button']['rect'] = pygame.Rect(0, WINDOW_HEIGHT // 2, 200, 50)
    buttons['quit_button']['rect'].centerx = WINDOW_WIDTH // 2
    buttons['quit_button']['text'] = font.render('QUIT', True, WHITE)
    buttons['quit_button']['text rect'] = buttons['quit_button']['text'].get_rect(center=buttons['quit_button']['rect'].center)
    # Sounds
    pygame.mixer.music.load('main-theme.ogg')
    pygame.mixer.music.play(-1)
    global score
    global clicked
    global direction
    while running:
        # While Running
        draw_screen()
        draw_score()
        if game_over:
            return
        elif not pause:
            pause = not handle_events()
            # Movement
            key_frame += 1
            if key_frame >= FPS/10:
                key_frame = 0
                snake = snake[-1:] + snake[:-1] # move the last item to be the first item 
                snake[0][0] = snake[1][0] # set the new first item's coords to the old first item's
                snake[0][1] = snake[1][1]
                # Move the first item 1 unit
                if direction == 1: 
                    snake[0][1] -= CELL_SIZE
                if direction == 2:
                    snake[0][1] += CELL_SIZE
                if direction == 3:
                    snake[0][0] -= CELL_SIZE
                if direction == 4:
                    snake[0][0] += CELL_SIZE
            # Food
            if new_food:
                new_food = False
                food[0] = CELL_SIZE* random.randint(0, (WINDOW_WIDTH // CELL_SIZE)-1)
                food[1] = CELL_SIZE* random.randint(0, (WINDOW_HEIGHT // CELL_SIZE)-1)
            
            if food == snake[0]:
                new_food = True
                score += 1
                new_piece = list(snake[-1])
                if direction == 1:
                    new_piece[1] += CELL_SIZE
                if direction == 2:
                    new_piece[1] -= CELL_SIZE
                if direction == 3:
                    new_piece[0] -= CELL_SIZE
                if direction == 4:
                    new_piece[0] += CELL_SIZE
                snake.append(new_piece)
            game_over = check_game_over(snake)
        # End of gave over if statement
        if pause:
            pause = handle_events()
            if clicked:
                if buttons['resume_button']['rect'].collidepoint(pygame.mouse.get_pos()):
                    pause = False
                    clicked = False
                if buttons['quit_button']['rect'].collidepoint(pygame.mouse.get_pos()):
                    clicked = False
                    return
            screen.fill((100,100,50))
            for button in buttons: # Display Buttons
                pygame.draw.rect(screen, (100, 100, 200), buttons[button]['rect'])
                screen.blit(buttons[button]['text'], buttons[button]['text rect'])
        # End Of Pause
        head = True
        for x in snake:
            if head == False:
                pygame.draw.rect(screen, (0, 100, 0), (x[0], x[1], CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GREEN, (x[0]+1, x[1]+1, CELL_SIZE -2, CELL_SIZE-2))
            if head == True:
                pygame.draw.rect(screen, (100, 0, 0), (x[0], x[1], CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, RED, (x[0]+1, x[1]+1, CELL_SIZE -2, CELL_SIZE-2))
                head = False
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        clock.tick(FPS)
        # Limit clock to FPS & Update Screen
        pygame.display.flip()
        clock.tick(FPS)

# Other Functions
def draw_screen():
    screen.fill(YELLOW)
def draw_score():
    text = 'score: ' + str(score)
    img = pygame.font.SysFont(None, 40).render(text, True, BLUE)
    screen.blit(img, (0,0))
def check_game_over(snake):
    head =  True
    for segment in snake:
        if head:
            head = False
            continue
        if snake[0] == segment:
            pygame.mixer.music.load('game_over.ogg')
            pygame.mixer.music.play(-1)
            return True
    if not(0 < snake[0][0] < WINDOW_WIDTH):
        pygame.mixer.music.load('game_over.ogg')
        pygame.mixer.music.play(-1)
        return True
    if not(0 < snake[0][1] < WINDOW_HEIGHT):
        pygame.mixer.music.load('game_over.ogg')
        pygame.mixer.music.play(-1)
        return True
    return False
def main_menu():
    global clicked
    pygame.display.set_caption('Main Menu')
    font = pygame.font.SysFont('Arial', 40)
    buttons = {
        'play_button' : {},
        'quit_button' : {}
    }
    buttons['play_button']['rect'] = pygame.Rect(0, WINDOW_HEIGHT // 3, 200, 50)
    buttons['play_button']['rect'].centerx = WINDOW_WIDTH // 2
    buttons['play_button']['text'] = font.render('PLAY', True, WHITE)
    buttons['play_button']['text rect'] = buttons['play_button']['text'].get_rect(center=buttons['play_button']['rect'].center)

    buttons['quit_button']['rect'] = pygame.Rect(0, WINDOW_HEIGHT // 2, 200, 50)
    buttons['quit_button']['rect'].centerx = WINDOW_WIDTH // 2
    buttons['quit_button']['text'] = font.render('EXIT', True, WHITE)
    buttons['quit_button']['text rect'] = buttons['quit_button']['text'].get_rect(center=buttons['quit_button']['rect'].center)

    running_menu = True
    while running_menu:
        running_menu = handle_events()
        if clicked:
            if buttons['play_button']['rect'].collidepoint(pygame.mouse.get_pos()):
                clicked = False
                main()
            if buttons['quit_button']['rect'].collidepoint(pygame.mouse.get_pos()):
                clicked = False
                pygame.quit()
                sys.exit()
        screen.fill((50,50,50))
        for button in buttons: # Display Buttons
            pygame.draw.rect(screen, (100, 100, 200), buttons[button]['rect'])
            screen.blit(buttons[button]['text'], buttons[button]['text rect'])

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
# Startup
if __name__ == '__main__':
    screen = init_game()
    main_menu()