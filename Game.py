import pygame
import time
import random

pygame.init()

gameDisplay = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
displayWidth, displayHeight = gameDisplay.get_size()
pygame.display.set_caption("Race Car Game")
clock = pygame.time.Clock()

def draw_level_text(level):
    levelFontObj = pygame.font.Font("freesansbold.ttf", 50)
    levelTextSurface = levelFontObj.render("Level: " + str(level), True, (0, 200, 0))
    gameDisplay.blit(levelTextSurface, (195, 250))

def draw_scoreboard(score):
    scoreFontObj = pygame.font.Font("freesansbold.ttf", 50)
    scoreTextSurface = scoreFontObj.render("Score: "+str(score),True,(0,  0, 0))
    gameDisplay.blit(scoreTextSurface, (195, 150))

def draw_obstacle(obsImage, x_pos, y_pos):
    gameDisplay.blit(obsImage, (x_pos, y_pos))

def draw_car(carImage, x_pos, y_pos):
    gameDisplay.blit(carImage, (x_pos, y_pos))

def draw_crash_text():
    crashFontObj = pygame.font.Font("freesansbold.ttf", 300)
    crashTextSurface = crashFontObj.render("Boom", True, (255, 0, 0))
    crashTextRect = crashTextSurface.get_rect()
    crashTextRect.center = (displayWidth/2, displayHeight/2)
    gameDisplay.blit(crashTextSurface, crashTextRect)
    pygame.display.update()
    time.sleep(2)

def game_loop():
    stop_game = False
    score = 0
    level = 1
    car_speed = 10
    car_height = 150
    car_width = 150
    x_carpos = (displayWidth/2 - car_width/2)
    y_carpos = displayHeight - 300
    x_carpos_change = 0

    obs_speed = 10
    obs_width = 225
    obs_height = 200
    x_obspos = random.randrange(175, displayWidth - obs_width - 325)
    y_obspos = -600

    carImage = pygame.image.load("images/car_png.png")
    carImage = pygame.transform.scale(carImage, (car_width, car_height))
    obsImage = pygame.image.load("images/obs_png.png")
    obsImage = pygame.transform.scale(obsImage, (obs_width, obs_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_game = True
                if event.key == pygame.K_LEFT:
                    x_carpos_change = -car_speed
                if event.key == pygame.K_RIGHT:
                    x_carpos_change = car_speed

        gameDisplay.fill((255,255,255))

        x_carpos = x_carpos + x_carpos_change
        y_obspos = y_obspos + obs_speed

        draw_scoreboard(score)
        draw_level_text(level)
        draw_obstacle(obsImage, x_obspos, y_obspos)
        draw_car(carImage, x_carpos, y_carpos)

        clock.tick(100)
        pygame.display.update()

        if stop_game == True:
            return False
        if x_carpos < 175 or x_carpos > displayWidth - 325:
            time.sleep(1)
            draw_crash_text()
            return True
        if y_obspos > displayHeight:
            x_obspos = random.randrange(175, displayWidth - obs_width - 325)
            y_obspos = -obs_height
            score += 1
            if score>1 and (score-1)%5 == 0:
                level +=1
                obs_speed += 1
        if y_obspos+obs_height > y_carpos+15 and y_obspos+10 < y_carpos+car_height:
            if (x_carpos+25 > x_obspos and x_carpos+25 < x_obspos+obs_width) or (x_carpos+car_width-25 > x_obspos and x_carpos+car_width-25 < x_obspos+obs_width):
                time.sleep(1)
                draw_crash_text()
                return True

game_count = 1
while(game_loop()):
    print("Game ", str(game_count), " Started")
    game_count += 1

pygame.quit()
quit()
