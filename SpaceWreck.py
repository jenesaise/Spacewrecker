import pygame
import os
pygame.font.init()
pygame.mixer.init()

#defining window aspects
WIN_WIDTH = 900
WIN_HEIGHT = 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Spaceship Wrecker!")
BORDER = pygame.Rect(WIN_WIDTH//2 -5, 0, 10, WIN_HEIGHT)
FPS = 60

#sound effects
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets/Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets/Gun+Silencer.mp3'))

#fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#colors used 
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#speed of window closure and bullets
VEL = 5
BULLETS_VEL = 7

MAX_BULLETS = 3 #maximum number of bullets

#defining spaceship aspects
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

YELLOW_HIT = pygame.USEREVENT +1
RED_HIT =  pygame.USEREVENT +2


#IMPORTING ALL IMAGES USED 
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'spaceship_yellow.png')),90)
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'spaceship_red.png')), 270)
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'image.png')), (WIN_WIDTH, WIN_HEIGHT))


def yellow_handle_movements(keys_pressed, yellow):
    
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL +yellow.height < WIN_HEIGHT - 5: #down
        yellow.y += VEL


def red_handle_movements(keys_pressed, red):
    
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width  : #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIN_WIDTH: #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0 : #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < WIN_HEIGHT - 5: #down
        red.y += VEL


def handle_bullets(yellowbullets, redbullets, yellow, red):
    for bullet in yellowbullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowbullets.remove(bullet)
        elif bullet.x > WIN_WIDTH:
            yellowbullets.remove(bullet) 

    for bullet in redbullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):  
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redbullets.remove(bullet)
        elif bullet.x < 0:
            redbullets.remove(bullet)


def draw_window(red, yellow,redbullets, yellowbullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, WHITE)

    #reducing user health 
    WIN.blit(red_health_text, (WIN_WIDTH - red_health_text.get_width()-10 , 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))


    for bullet in redbullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellowbullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def draw_winner(text):
    #using // to avoid float num errors 
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIN_WIDTH//2 - draw_text.get_width()//2, WIN_HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    red = pygame.Rect(700, 300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellowbullets=[]
    redbullets=[]
    
    #initializing health
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowbullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellowbullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(redbullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    redbullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movements(keys_pressed, yellow)
        red_handle_movements(keys_pressed, red)

        handle_bullets(yellowbullets, redbullets, yellow, red)

        draw_window(red, yellow, redbullets, yellowbullets, red_health, yellow_health)
    main()


if __name__ == "__main__":
    main()
