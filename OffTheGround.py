import pygame
import math
import random

#character = pygame.image.load("standing.png")


#player varubales:
player = (50,50)
bg_width = 600
bg_hight = 400
screen_width = 800
screen_hight = 600
x = bg_width / 2
y = bg_hight / 2
player_width = 30
player_hight = 60
shoting_vel = 10
x_vel = 0
y_vel = 0
gravity = 0.3
bouncing_factor = 0.5
rightClicks_pressed = False
score_radius = 20
new_score = True
score_x = 0
score_y = 0
win = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("just testing this shit")


class bullets:
    def __init__(self):
        self.fromx = x
        self.fromy = y  
        self.tox = mouse[0]
        self.toy = mouse[1]
        self.bcos = 0
        self.bsin = 0

    def sin_cos(self,mouse):
        watr = math.sqrt((mouse[0] - x - player_width/2)**2  + (mouse[1] - y - player_hight/2)**2)
        self.bcos = (mouse[0] - screen_width) / watr
        self.bsin = (mouse[1] - screen_hight) / watr


def generate_new_score():
    global score_x, score_y, new_score
    i = 1
    while True:
        score_x = random.randint(score_radius, bg_width - score_radius)
        score_y = random.randint(score_radius, bg_hight - score_radius)
        if abs(score_x - x) > player_width and abs(score_y - y) > player_hight:
            break
    print(i)
    i+=1
    new_score = False



running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if not(y >= bg_hight - player_hight):
        y_vel += gravity
    elif y >= bg_hight - player_hight:
        if y_vel > 4:
            y_vel = y_vel * -bouncing_factor
            x_vel = x_vel * bouncing_factor
        else:
            y_vel = 0
            x_vel = 0
    if y <= 0:
        y_vel = y_vel * -bouncing_factor
        x_vel = x_vel * bouncing_factor
    if x <= 0 or x >=  bg_width - player_width:
        y_vel = y_vel * bouncing_factor
        x_vel = x_vel * -bouncing_factor
    if x_vel != 0:
        #x_vel -= (abs(x_vel) / x_vel) / 30
        pass


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    mouse = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and rightClicks_pressed == False:
        watr = math.sqrt((mouse[0] - screen_width/2)**2  + (mouse[1] - screen_hight/2)**2)
        tcos = (mouse[0] - screen_width/2) / watr
        tsin = (mouse[1] - screen_hight/2) / watr

        x_vel = x_vel * 0.5 + shoting_vel * tcos
        y_vel = y_vel * 0.5 + shoting_vel * tsin

        rightClicks_pressed = True
    elif not pygame.mouse.get_pressed()[0]:
        rightClicks_pressed = False


    x += x_vel
    y += y_vel
    
    if y >= bg_hight - player_hight:
        y = bg_hight - player_hight
    if x >= bg_width - player_width:
        x = bg_width - player_width
    if x <= 0:
        x = 0
    if y <= 0:
        y = 0


    if score_x - score_radius - player_width < x < score_x + score_radius  and score_y - score_radius - player_hight < y < score_y + score_radius:
        new_score = True

    if new_score:
        generate_new_score()


    pygame.draw.rect(win, (0, 0, 30), (0, 0, screen_width, screen_hight))
    #win.blit(bg, (-(x - screen_width / 2 + player_width/2), -(y - screen_hight / 2 +player_hight/2)))
    pygame.draw.rect(win, (100, 70, 55), (-(x - screen_width / 2 + player_width/2), -(y - screen_hight / 2 +player_hight/2), screen_width, screen_hight))

    pygame.draw.rect(win, (255, 0, 0), (screen_width/2 - player_width/2, screen_hight/2 - player_hight/2, player_width, player_hight))
    #win.blit(character, (bg_width / 2 - player_width/2, bg_hight / 2 - player_hight/2))
    
    pygame.draw.circle(win, (0, 0, 255), (score_x - int(x - screen_width / 2 + player_width / 2), score_y - int(y - screen_hight / 2 + player_hight / 2)), score_radius)

    pygame.display.update() 
    pygame.time.delay(13)

pygame.quit()