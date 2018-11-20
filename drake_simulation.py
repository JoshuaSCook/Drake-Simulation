# -*- coding: utf-8 -*-
import pygame
import random
import time

pi = 3.14159
e = 2.71828

image = pygame.image.load('galaxy.jpg')

def generateLifespan(L, sigma):
    '''
    assigns a random lifespan factor (0.0 - 1.0) based on the lifespan
    probability function.
    '''
    y = 1
    fx = 0
    while y > fx:
        x = random.uniform(0, L + (5 * sigma))
        y = random.uniform(0.0, 0.0016)
        fx = ((1 / ((2 * pi * sigma ** 2) ** -1)) * (e ** -(((x - L) ** 2) / (2 * (sigma ** 2)))))    # lifespan probablility function
    return(x)
    
def createCivilization(civilizations, t, L):
    '''
    creates virtual civilization represented by a list of values that provide
    the necessary information needed to run the simulation.
    
    example = [0, 1, 2, 3]
    where index,
        0 = x position of the civilization within the galaxy
        1 = y position of the civilization within the galazy
        2 = time (t) of emergence for the civilization
        3 = lifespan (years)
    '''
    civ = []
    
    x_pos = random.uniform(0.0, 1.0)
    y_pos = random.uniform(0.0, 1.0)
    
    sigma = 0.1 * L
    lifespan = generateLifespan(L, sigma)
    
    civ.append(x_pos)
    civ.append(y_pos)
    civ.append(t)
    civ.append(lifespan)
    
    return(civ)
    
def button(color=(0,0,0), width=0, height=0, x_pos=0, y_pos=0, quantity=0, multiplier=1):
    '''
    
    '''
    button_color = color
    if mouse[0] >= x_pos and mouse[0] <= x_pos + width and mouse[1] >= y_pos and mouse[1] <= y_pos + height:
        button_color = blue
        
        if click[0] == 1:
            button_color = (100, 100, 100)
            quantity += (0.01 * multiplier)
            
            if quantity < 0:
                quantity = 0
            if quantity >= 10:
               pass
            elif quantity < 10 and quantity > 2:
                quantity = 10
            elif quantity > 1:
                quantity = 1
                            
    pygame.draw.rect(screen, button_color, [x_pos, y_pos, width, height])
    return(round(quantity, 2))        

# initialize game engine.
pygame.init()
# set screen width/height and caption
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
title = 'Civilization Simulator'
pygame.display.set_caption(title + ' - 25.0 fps')
myfont = pygame.font.SysFont('monospace', 15)

# initialize clock. used later in the loop.
fps = 25
t = 0
years_per_second = 1000
years_per_frame = int(years_per_second / fps)
clock = pygame.time.Clock()
frame = 0

# Colors
white = (255,255,255)
black = (0,0,0)
grey = (50,50,50)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# constants (values taken from wikipedia)
R_star = 1.5    # star-formation rate (new stars per year)
f_p = 1.0    # fraction of stars that have planets (0.0 - 1.0)
n_e = 0.4    # average number of habitable planets per star

# variable
f_l = 0.5    # fraction of those planets that actually develop life (0.0 - 1.0)
f_i = 0.05    # fraction of those biomes that produce intelligent life (0.0 - 1.0)
f_c = 0.5    # fraction of those intelligent life that send signals into space (0.0 - 1.0)
L = 1000.0    # the lenght of time those civilizaitons exist (years)

N = R_star * f_p * n_e * f_l * f_i * f_c * L    # number of active civs at a given moment
R = N / years_per_frame    # number of emerging civs per frame
print('N = ' + str(N))
print('R = ' + str(R))

n_civs = 0
civilizations = []
ex_civs = []

# Loop until the user clicks close button
done = False
while done == False:
    
    # Calculate the fps and display in the caption
    frame += 1.
    if frame == 1:
        start_time = time.clock()
    elif frame > 30:
        end_time = time.clock()
        fps = 30 / (end_time - start_time)
        pygame.display.set_caption(title + ' - ' + str(round(fps, 1)) + ' fps')
        frame = 0
      
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
            
    # write game logic here 
    N = R_star * f_p * n_e * f_l * f_i * f_c * L    # number of active civs at a given moment
    R = N / years_per_frame    # number of emerging civs per frame
          
    if R < 1:
        dice = random.uniform(0.0, 1.0)
        if dice <= R:
            civ = createCivilization(civilizations, t, L)
            civilizations.append(civ)
            n_civs += 1
    
    else:
        for i in range(int(R)):
            civ = createCivilization(civilizations, t, L)
            civilizations.append(civ)
            n_civs += 1
        
    # once civilization dies, move it to the ex_civs list
    for civ in civilizations:
        if t - civ[2] > civ[3]:
            ex_civs.append(civ)
            civilizations.remove(civ)    
    
    # once 10000 yrs have passed since the civs emergence, delete civ from ex_civs
    for civ in ex_civs:
        if t - civ[2] > 10000:
            ex_civs.remove(civ)
    
    t += years_per_frame
    
    contacts = 0
    # SETI for active civilizations
    for civ_1 in civilizations:
        for civ_2 in ex_civs:
            delta_x = abs(civ_1[0] - civ_2[0]) * 100000
            delta_y = abs(civ_1[1] - civ_2[1]) * 100000
            d = ((delta_x ** 2) + (delta_y ** 2)) ** (0.5)
            head = t - civ_2[2]
            tail = t - civ_2[2] - civ_2[3]
            if head > d and d > tail:
                contacts += 1
                     
                
 
    # clear the screen before drawing
    screen.fill(black) 
    
    # write draw code here
    screen.blit(image, (0, 0))
          
    for civ in ex_civs:
        strength = float((10000 - (t - civ[2]))) / 10000.0
        color = (int(strength * 155), 0, 0)
        x = int(civ[0] * width)
        y = int(civ[1] * height)
        r = int((t - civ[2]) / 200)
        ring_width = int(civ[3] / 200)
        # make imperceptible numerical changes if L < 200 --> ring_width = 0
        if ring_width == 0:
            ring_width = 1
            r += 1
        pygame.draw.circle(screen, color, [x, y], r, ring_width)
            
    for civ in civilizations:
        x = int(civ[0] * width)
        y = int(civ[1] * height)
        r = int((t - civ[2]) / 200)
        pygame.draw.circle(screen, green, [x, y], r)
        #pygame.draw.circle(screen, white, [x, y], 3)
    
    # draw buttons
    #pygame.draw.rect(screen, grey, [0, 0, 270, 90])
    
    f_l = button((0,0,200), 10, 10, 20, 10, f_l, 1)
    f_l = button((0,0,200), 10, 10, 20, 45, f_l, -1)
    f_l_value = myfont.render(str(f_l), 1, white)
    screen.blit(f_l_value, (20, 25))
    f_l_label = myfont.render('f_l', 1, white)
    screen.blit(f_l_label, (20, 60))
    
    f_i = button((0,0,200), 10, 10, 80, 10, f_i, 1)
    f_i = button((0,0,200), 10, 10, 80, 45, f_i, -1)
    f_i_value = myfont.render(str(f_i), 1, white)
    screen.blit(f_i_value, (80, 25))
    f_i_label = myfont.render('f_i', 1, white)
    screen.blit(f_i_label, (80, 60))
    
    f_c = button((0,0,200), 10, 10, 140, 10, f_c, 1)
    f_c = button((0,0,200), 10, 10, 140, 45, f_c, -1)
    f_c_value = myfont.render(str(f_c), 1, white)
    screen.blit(f_c_value, (140, 25))
    f_c_label = myfont.render('f_c', 1, white)
    screen.blit(f_c_label, (140, 60))
    
    L = button((0,0,200), 10, 10, 200, 10, L, 500)
    L = button((0,0,200), 10, 10, 200, 45, L, -500)
    L_value = myfont.render(str(L), 1, white)
    screen.blit(L_value, (200, 25))
    L_label = myfont.render('L', 1, white)
    screen.blit(L_label, (200, 60))
    
    pygame.draw.rect(screen, black, [0, 475, 500, 25])
    
    n = 0
    for i in range(contacts):
        pygame.draw.rect(screen, green, [485 - (10 * n), 482, 6, 12])
        n += 1
        if n >= 34:
            pygame.draw.rect(screen, red, [485 - (10 * n), 482, 6, 12])
            break
        
    label = myfont.render('t = ' + str(t) + ' yrs', 1, green)
    screen.blit(label, (8, 480))
    
    # Constants
    R_star_label = myfont.render('R_star = ' + str(R_star), 1, white)
    screen.blit(R_star_label, (373, 10))
    f_p_label = myfont.render('f_p = ' + str(f_p), 1, white)
    screen.blit(f_p_label, (400, 30))
    n_e_label = myfont.render('n_e = ' + str(n_e), 1, white)
    screen.blit(n_e_label, (400, 50))
    
    n_civs_label = myfont.render(str(n_civs), 1, white)
    screen.blit(n_civs_label, (465, 460))
        
    # display what’s drawn. this might change
    pygame.display.update()
    
    # run at defined fps
    clock.tick(fps)
 
# close the window and quit
pygame.quit()