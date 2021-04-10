import pygame
import sys
import random

pygame.init() ##initliazing the pygame package

WIDTH = 800
HEIGHT = 600 

RED = (255,0,0) #initailaize red color(rgb)
BLUE = (0,0,255) #initialize blue color
Background_color =(0,0,0)
YELLOW = (255,255,0)

Speed = 10

Player_size = 50 #size of the block
Player_pos = [WIDTH/2, HEIGHT-2*Player_size] #player position on the screen

enemy_size = 50 #size of the enemy block
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0] #enemy position on the screen
enemy_list =[enemy_pos]


screen = pygame.display.set_mode((WIDTH,HEIGHT)) ##setting up the screen

game_over = False

score = 0

myFont = pygame.font.SysFont("monospace",35)

#setting the time
clock = pygame.time.Clock()

def set_level(score,Speed):
    if score < 20:
        Speed = 5
    elif score <40:
        Speed = 8
    elif score < 60:
        Speed = 12
    else:
        Speed = 15

    return Speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 8 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0],enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += Speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, Player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos,Player_pos):
            return True
    
    return False

def detect_collision(Player_pos, enemy_pos):
    p_x = Player_pos[0]
    p_y = Player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + Player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and p_x <(p_y + Player_size)) or (p_y >= e_y and p_y < (p_x + enemy_size)):
            return True
    return False


while not game_over:
    for event in pygame.event.get():
         
         # to quit the game when we close the terminal window
         if event.type == pygame.QUIT:
             sys.exit()
        
         if event.type == pygame.KEYDOWN:

             x = Player_pos[0]
             y = Player_pos[1]

             if event.key == pygame.K_LEFT:
                 x-=Player_size
            
             elif event.key == pygame.K_RIGHT:
                 x += Player_size

             Player_pos = [x,y]

    screen.fill(Background_color)

    drop_enemies(enemy_list)

    score = update_enemy_positions(enemy_list, score)

    Speed = set_level(score, Speed)

    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)

    screen.blit(label,(WIDTH-200, HEIGHT-40))
    
    if collision_check(enemy_list, Player_pos):
        game_over =True
        break
    
    draw_enemies(enemy_list)

    ## drawing a rectangle block on the screen 
    ## refer pygame documentation

    pygame.draw.rect(screen, RED, (Player_pos[0], Player_pos[1], Player_size, Player_size))

    clock.tick(30) ## FPS

    pygame.display.update() ##updating displaying the screen everytime
