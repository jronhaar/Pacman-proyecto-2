import copy
from board import boards
import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
player_images = []
for i in range (1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'player_images/{i}.png'), (45, 45)))
    rojo_img = pygame.transform.scale(pygame.image.load(f'ghost_images/red.png'), (45, 45))
    pink_img = pygame.transform.scale(pygame.image.load(f'ghost_images/pink.png'), (45, 45))
    azul_img = pygame.transform.scale(pygame.image.load(f'ghost_images/blue.png'), (45, 45))
    naranja_img = pygame.transform.scale(pygame.image.load(f'ghost_images/orange.png'), (45, 45))
    asustado_img = pygame.transform.scale(pygame.image.load(f'ghost_images/powerup.png'), (45, 45))
    dead_img = pygame.transform.scale(pygame.image.load(f'ghost_images/dead.png'), (45, 45))
player_x = 450
player_y = 663
direction = 0
direction_command = 0
rojo_x = 56
rojo_y = 58
rojo_direction = 2
pink_x = 440
pink_y = 388
pink_direction = 2
azul_x = 440
azul_y = 438
azul_direction = 2
naranja_x = 440
naranja_y = 438
naranja_direction = 2
counter = 0
valid_turns = [False, False, False, False] # R, L, UP, Down
player_speed = 2
score = 0
powerUp = False
powerUp_count = 0
ghosts_comidos = [False, False,False,False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
rojo_dead = False
pink_dead = False
azul_dead = False
naranja_dead = False
rojo_box = False
pink_box = False
azul_box = False
naranja_box = False
moving = False
count_inicio = 0
vida = 5
def draw_texto():
    score_text = font.render(f'Score: {score}',True, 'white') #True es para hacer el texto mas bonito
    screen.blit(score_text,(30,485))
    if powerUp:
        pygame.draw.circle(screen,'red',(50, 550),15)
    for i in range(vida):
        screen.blit(pygame.transform.scale(player_images[0],(30, 30)), (650 + i * 40, 915)) # i * 40 hace que se mueva 40 pix a la derecha
def check_colision(scor, powerUp, powerUp_count, ghosts_comidos):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            powerUp = True
            powerUp_count = 0
            ghosts_comidos = [False,False,False,False]

    return scor, powerUp,powerUp_count,ghosts_comidos

# codigo del cuadrado.
def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_player():
    # 0= derecha, 1 = izq, 2 = arriba, 3= abaj0
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], -90), (player_x, player_y))

def check_position(centerx, centery):
        turns = [False, False, False, False]
        num1 = (HEIGHT - 50) // 32
        num2 = (WIDTH // 30)
        num3 = 15

        # check de colisiones
        if centerx // 30 < 29:
            if direction == 0:
                if level[centery//num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
            if direction == 1:
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
            if direction == 2:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
            if direction == 3:
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True

            if direction == 2 or direction == 3: # direcciones up y down
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num3) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num3) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num2) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num2) // num2] < 3:
                        turns[0] = True

            if direction == 0 or direction == 1: # direcciones derecha e izquierda
                if 12 <= centerx % num2 <= 18:
                    if level[(centery + num1) // num1][centerx // num2] < 3:
                        turns[3] = True
                    if level[(centery - num1) // num1][centerx // num2] < 3:
                        turns[2] = True
                if 12 <= centery % num1 <= 18:
                    if level[centery // num1][(centerx - num3) // num2] < 3:
                        turns[1] = True
                    if level[centery // num1][(centerx + num3) // num2] < 3:
                        turns[0] = True

        else:
            turns[0] = True
            turns[1] = True

        return turns

def move_player(play_x, play_y):
        # d, i, ar, ab
    if direction == 0 and valid_turns[0]:
            play_x += player_speed
    elif direction == 1 and valid_turns[1]:
            play_x -= player_speed
    if direction == 2 and valid_turns[2]:
            play_y -= player_speed
    elif direction == 3 and valid_turns[3]:
            play_y += player_speed
    return play_x, play_y

run = True
Paused = False
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
    else:
        counter = 0

    if powerUp and powerUp_count < 600: #600 es 10 sec a 60fps
        powerUp_count += 1
    elif powerUp and powerUp_count >= 600:
        powerUp_count = 0
        powerUp = False
        ghosts_comidos = [False,False,False,False]
    if count_inicio < 180: # 3s en 60fps
        moving = False
        count_inicio += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    draw_player()
    draw_texto()
    center_x = player_x + 23
    center_y = player_y + 24
    valid_turns = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    score, powerUp, powerUp_count, ghosts_comidos = check_colision(score, powerUp, powerUp_count, ghosts_comidos)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            elif event.key == pygame.K_LEFT:
                direction_command = 1
            elif event.key == pygame.K_UP:
                direction_command = 2
            elif event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction


        for i in range(4):
            if direction_command == i and valid_turns[i]:
                direction = i
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()

pygame.quit()
