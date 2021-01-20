# All constants are Capitals Variables
import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900, 500 # Width and Height of the window

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 255, 255)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # X, Y, Width, Height

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60 # frame the game is refreshing

VEL = 5 # Velocity of the ship

BULLET_VEL = 8 # velocity of the bullets less no means slow
MAX_BULLETS = 4  # number of max bullets that can be fired 

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

#if collide happen fire this event
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# loading the image 
# In this the path is soecified by the os module as some os have '/' seperator and some have '\' seperator
# so the respective seperator is added by the respective os module
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Battle_Stars', 'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Battle_Stars', 'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Battle_Stars', 'Assets', 'space.png')), (WIDTH, HEIGHT))

# Window of Width 900 and Height 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Window Title
pygame.display.set_caption("Battle Stars")

# Draw everything on window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        WIN.blit(SPACE, (0, 0))
        pygame.draw.rect(WIN, BLACK, BORDER) #another way of drawing the rect

        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10, 10))
        # we use blit when we want to draw the surface on the screen
        # 300 and 100 is the x and y coordinate respectively
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #moving ship acc to the rect
        WIN.blit(RED_SPACESHIP, (red.x, red.y))

        #Drawing bullets on the screen
        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update() 

def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left for left ship ie yellow and check that ship does not cross border
            yellow.x -= VEL  

        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # Right for left ship ie yellow
            yellow.x += VEL  

        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # Up for left ship ie yellow
            yellow.y -= VEL  

        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # Down for left ship ie yellow
            yellow.y += VEL  

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left for right ship ie red
        red.x -= VEL  

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # Right for right ship ie red
        red.x += VEL  

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up for left right ie red
        red.y -= VEL  

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # Down for right ship ie red
        red.y += VEL  


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets: 
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets: 
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2-draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000) 
# Main Function/ Driver Function
def main():

    # Making a rect in which image of ship is placed and instead of moving image we move the rect which is easy
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) 
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets =  [] 
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True # loop Until run is False
    while run:
        clock.tick(FPS) # This will control the speed of the while loop with FPS speed
        # This event loop check for all the events that are going to happen
        # This gives a list of all the events
        for event in pygame.event.get():

            # This will check for the window close button is click then it stops loop 
            # If window close event is clicked then stops
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN: # it tells we pressed a key downawrds to fire a bullet
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # for left player bullet emerges from the x position + the width of the body 
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.width//2-2, 10, 5) 
                    yellow_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.width//2-2, 10, 5) 
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1


            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        
        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        # this tells what keys are currently being pressed down and also it tells if we press multiple key 
        # toghter and also if we press down a key it will encounter multiple times
        keys_pressed = pygame.key.get_pressed() 
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red) # handling bullets collision

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main()
 

#As we have lots of file with their own main so it will call the main function only when this file is run 
if __name__ == "__main__":
    main()
