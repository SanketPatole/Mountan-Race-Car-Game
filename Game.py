import pygame
import time
import random

pygame.init()

gameDisplay = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
displayWidth, displayHeight = gameDisplay.get_size()
pygame.display.set_caption("Race Car Game")
clock = pygame.time.Clock()

def draw_text(text, fontname,  fontsize, pos_x=None, pos_y=None, color=(0,0,0), center=False, yOffset=0, textRect=None):
    textSurface = pygame.font.SysFont(name=fontname, size=fontsize).render(text, True, color)
    textRect = textSurface.get_rect(center=(displayWidth/2, (displayHeight/2 + yOffset) )) if center else (pos_x, pos_y) if not textRect else textRect
    gameDisplay.blit(textSurface, textRect)

def get_image_obj(imagUrl, width, height):
    return pygame.transform.scale( pygame.image.load(imagUrl), (width, height))

def draw_image(imageObj, x_pos, y_pos):
    gameDisplay.blit(imageObj, (x_pos, y_pos))

def draw_button(inactive, active, text, x_pos, y_pos):

    mouse_x, mouse_y = pygame.mouse.get_pos()

    textRect = inactive.get_rect(center=(x_pos+inactive.get_width()/1.4, y_pos+inactive.get_height()/1.4))

    if mouse_x > x_pos and mouse_x < x_pos+300 and mouse_y > y_pos and mouse_y < y_pos+150:
        draw_image(active, x_pos, y_pos)
        draw_text(text=text, fontname="comicsansms", fontsize=40, textRect=textRect)
        if pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            False
    else:
        draw_image(inactive, x_pos, y_pos)
        draw_text(text=text, fontname="comicsansms", fontsize=40, textRect=textRect)
        return False

def game_intro():
    stop_game = False

    obsImgObj = get_image_obj("images/obs_png.png", 300, 225)
    redButtonImgObj = get_image_obj("images/red_button.png", 150, 150)
    greenButtonImgObj = get_image_obj("images/green_button.png", 150, 150)
    activeButtonImgObj = get_image_obj("images/active_button.png", 150, 150)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_game = True

        gameDisplay.fill((255, 255, 255))
        draw_text(text="Mountain", fontname="comicsansms", fontsize=175, color=(200, 0, 0), center=True, yOffset=-200)
        draw_text(text="Race Car", fontname="comicsansms", fontsize=100, color=(0, 0, 200), center=True, yOffset=0)
        draw_image(obsImgObj, 200, displayHeight/2 - 112)
        draw_image(obsImgObj, displayWidth-500, displayHeight/2 - 112)
        greenPressed = draw_button(inactive=greenButtonImgObj, active=activeButtonImgObj, text="Play", x_pos=550, y_pos=displayHeight*0.70)
        redPressed = draw_button(inactive=redButtonImgObj, active=activeButtonImgObj, text="Quit", x_pos=displayWidth-700, y_pos=displayHeight*0.70)

        if redPressed:
            stop_game = True
        elif greenPressed:
            stop_game = game_loop()

        pygame.display.update()
        if stop_game == True:
            return

def game_loop():
    stop_game = False
    pause_game = False
    score, level = 0, 1
    pause_x_carpos_change, pause_obs_speed = 0, 0

    car_speed, car_height, car_width = 10, 150, 150
    x_carpos, y_carpos, x_carpos_change = (displayWidth/2 - car_width/2), (displayHeight - 300), 0

    obs_speed, obs_height, obs_width = 10, 200, 225
    x_obspos, y_obspos = (random.randrange(175, displayWidth - obs_width - 325)), -600

    carImgObj = get_image_obj("images/car_png.png", car_width, car_height)
    obsImgObj = get_image_obj("images/obs_png.png", obs_width, obs_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_game = True
                    return stop_game
                if event.key == pygame.K_LEFT:
                    x_carpos_change = -car_speed
                if event.key == pygame.K_RIGHT:
                    x_carpos_change = car_speed
                if event.key == pygame.K_p:
                    if pause_game:
                        pause_game = False
                    else:
                        pause_game = True

        if pause_game and obs_speed != 0:
            pause_x_carpos_change = x_carpos_change
            pause_obs_speed = obs_speed
            x_carpos_change = 0
            obs_speed = 0
        elif pause_game == False and x_carpos_change == 0 and obs_speed == 0:
            x_carpos_change = pause_x_carpos_change
            obs_speed = pause_obs_speed

        x_carpos = x_carpos + x_carpos_change
        y_obspos = y_obspos + obs_speed

        gameDisplay.fill((255, 255, 255))
        draw_image(obsImgObj, x_obspos, y_obspos)
        draw_image(carImgObj, x_carpos, y_carpos)
        draw_text(text="Score: "+str(score), fontname="comicsansms", fontsize=50, pos_x=195, pos_y=150, color=(0,0,0), center=False)
        draw_text(text="Level: "+str(level), fontname="comicsansms", fontsize=50, pos_x=195, pos_y=250, color=(0,200,0), center=False)
        if pause_game:
            draw_text(text="Paused!!", fontname="comicsansms", fontsize=200, color=(200, 0, 0), center=True)

        if (x_carpos < 175 or x_carpos > displayWidth - 325)\
            or (
                (y_obspos+obs_height > y_carpos+15 and y_obspos+10 < y_carpos+car_height)
                and (
                     (x_carpos + 25 > x_obspos and x_carpos + 25 < x_obspos + obs_width)
                     or (x_carpos + car_width - 25 > x_obspos and x_carpos + car_width - 25 < x_obspos + obs_width)
                    )
                ):
            draw_text(text="Crashed!!", fontname="comicsansms", fontsize=200, color=(200, 0, 0), center=True)
            pygame.display.update()
            time.sleep(2)
            return stop_game

        if y_obspos > displayHeight:
            x_obspos = random.randrange(175, displayWidth - obs_width - 325)
            y_obspos = -obs_height
            score += 1
            if score>1 and (score-1)%5 == 0:
                level +=1
                obs_speed += 1

        clock.tick(100)
        pygame.display.update()

game_intro()

pygame.quit()
quit()