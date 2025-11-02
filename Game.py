import pygame
import random
import json
import os
import os.path
import math
import time
import button

pygame.init()

#menu 
surface = pygame.display.set_mode((800, 600))
 
#Game Vars
global scroll
global score
global clockChange
global pl_x
global pl_vel
global pl_y
global keys_pressed
clockChange = pygame.USEREVENT + 1
gotHit = pygame.USEREVENT + 2
FPS = 60
width = 800
height = 400
pl_x = 10
pl_y = 10
obsVel = 8
pl_vel = 5
score = 0
item_data={}
highScore = 0
start_game = 0
keys_pressed = pygame.key.get_pressed()
scoreFont = pygame.font.Font("Assets/FFFFORWA.TTF", 30)
scoreShower = pygame.font.Font("Assets/FFFFORWA.TTF", 25)
x, y = 5, 8

#Menu Images
start_img = pygame.image.load(os.path.join('Assets', 'start_btn2.png')).convert_alpha()
exit_img = pygame.image.load(os.path.join('Assets', 'exit_btn2.png')).convert_alpha()
restart_img = pygame.image.load(os.path.join('Assets', 'restart_btn.png')).convert_alpha()
resume_img = pygame.image.load(os.path.join('Assets', 'resume_btn.png')).convert_alpha()

#Other Images
obstacleImg = pygame.image.load(os.path.join('Assets', 'Obstacle.png'))
obstacleImg1 = pygame.image.load(os.path.join('Assets', 'Obstacle.png'))
theObstacle = pygame.transform.rotate(pygame.transform.scale(obstacleImg1, (55, 40)), 270)
characterImg = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'character2.png')), 315)
theCharacter = pygame.transform.scale(characterImg, (150, 150))
bgImg = pygame.image.load(os.path.join('Assets', 'background1.png')).convert()
mnenuBg = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'menuBg.jfif')).convert(), (800, 400))
mnenuBg1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'MenuBG1.jfif')).convert(), (800, 400))


#obstacle Images
obstacleImg2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'obstacle1.png')), (150, 150))
obstacleImg3 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'obstacle2.png')), (150, 150))
obstacleImg4 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'obstacle3.png')), (150, 150))
obstacleImg5 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'obstacle4.png')), (150, 150))

#cars
car1Img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'car1.png')), (75, 150)), 270)
car2Img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'car2.png')), (75, 150)), 270)
car3Img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'car2.png')), (75, 150)), 90)
bgWidth = bgImg.get_width()
tiles = math.ceil(width/bgWidth) + 1

        
user_profile = os.environ['USERPROFILE']
if os.path.isfile(f'{user_profile}/score.json') == False:
    with open(f'{user_profile}/score.json', 'w') as newfile:
        newfile.write("[]")
    with open(f'{user_profile}/score.json', "r") as newfile:
        temp1 = json.load(newfile)
    item_data["Score"] = 0
    temp1.append(item_data)
    with open(f'{user_profile}/score.json','w') as newfile:
        json.dump(temp1, newfile, indent=4)


#Creating the game screen
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Road Rush")
def game_over():
    pass

#Main drawing function

def draw_window(pl, obstacles):
    #win.fill((255, 255, 255))
    win.blit(car3Img, (pl.x - 12, pl.y - 12))
    #pygame.draw.rect(win, (255, 165, 0), (pl.x, pl.y, 120, 50))
    for obstacle in obstacles:
        def img1():
            win.blit(obstacleImg2, (obstacle.x - 30, obstacle.y - 60))
            
        def img2():
            win.blit(obstacleImg3, (obstacle.x - 30, obstacle.y - 60))
        def img3():
            win.blit(obstacleImg4, (obstacle.x - 30, obstacle.y - 60))
        def img4():
            win.blit(obstacleImg5, (obstacle.x - 30, obstacle.y - 60))
        images = random.choice([obstacleImg2, obstacleImg3, obstacleImg4, obstacleImg5])
        
        obss = [img1, img2, img3, img4]
        #realObs = random.choice(obss)()
        pygame.draw.rect(win, (255,165,255), obstacle)
        win.blit(car1Img, (obstacle.x - 18, obstacle.y - 13))


    
    pygame.display.update()
def obstacle_movement(obstacles):
    for obstacle in obstacles:
        obstacle.x -= obsVel
    
def pl_movement(pl):
    if pygame.key.get_pressed()[pygame.K_w] and pl.y - pl_vel > 0:
        pl.y -= pl_vel
    if pygame.key.get_pressed()[pygame.K_s] and pl.y + pl_vel + pl.height < height:
        pl.y += pl_vel

def hit_obstacle(pl, obstacles):
    for obstacle in obstacles:
        if pl.colliderect(obstacle):
            pygame.event.post(pygame.event.Event(gotHit))

def score_show(x,y):
    scoretxt = scoreShower.render("SCORE : " +str(score),True,(255,255,255), None)
    win.blit(scoretxt,(x,y))


#create menu buttons
start_button = button.Button(width//2-120, height//2 - 80, start_img, 1.2)
exit_button = button.Button(width//2-105, height//2, exit_img, 1.2)

restart_button = button.Button(width//2-135, height//2 - 80, restart_img, 1.2)
resume_button = button.Button(width//2-135, height//2 - 80, resume_img, 1.2)

#start_game = 0 is the main menu of the game
#start_game = 1 is the game itself
#start_game = 2 is the restart menu
#start_game = 3 is the pause menu


def main():
    global timeMS
    global score
    global obstacle
    global timer
    global timeBeforeTheLastObs
    global start_game
    global obsVel
    scroll = 0
    pl = pygame.Rect(70, height/2, 120, 50)
    obstacles = []
    food = []
    clock = pygame.time.Clock()
    run = True

    #Getting the Highest Score
    with open(f'{user_profile}/score.json', "r") as newfile:
        temp1 = json.load(newfile)
    highest_score = max(score['Score'] for score in temp1)

    #To show the new highscore without reopening the game
    if score > highest_score:
        highest_score = score

    while run:
        clock.tick(FPS)
        if start_game == 0:
            #mainMenu
            win.fill((50, 205, 50))
            win.blit(mnenuBg1, (0, 0))
            
            pygame.display.set_caption("menu")
            highScoreTxt = scoreFont.render("HIGHEST SCORE : " +str(highest_score),True,((0, 0, 0)), None)
            win.blit(highScoreTxt,(width // 2 - 200, 5))
            
            #Add Buttons
            if start_button.draw(win):
                start_game = 1
                buttonPressingTime = pygame.time.get_ticks()
                pygame.display.set_caption("Road Rush")
                score = 0

            if exit_button.draw(win):
                run = False

        elif start_game == 2:
            win.fill((50, 205, 50))
            win.blit(mnenuBg1, (0, 0))
            scoretxt = scoreFont.render("SCORE : " +str(score),True,((0, 0, 0)), None)
            win.blit(scoretxt,(width // 2 - 100, 50))
            highScoreTxt = scoreFont.render("HIGHEST SCORE : " +str(highest_score),True,((0, 0, 0)), None)
            win.blit(highScoreTxt,(width // 2 - 200, 5))
            pygame.display.set_caption("menu")

            if restart_button.draw(win):
                start_game = 1
                buttonPressingTime = pygame.time.get_ticks()
                pygame.display.set_caption("Road Rush")
                score = 0

            if exit_button.draw(win):
                run = False

        elif start_game == 3:
            win.blit(mnenuBg1, (0, 0))
            if resume_button.draw(win):
                start_game = 1



        elif start_game == 1:
            timeMS = pygame.time.get_ticks()
            timer = timeMS/1000 - buttonPressingTime/1000
            timeBeforeTheLastObs = timeMS/1000 - buttonPressingTime/1000
            obstacle_x = 750
            obstacleYs = [240, 320, 140, 50]
            obstacle_y = random.choice(obstacleYs)


            if len(obstacles) < timeBeforeTheLastObs-2 and len(obstacles) < 4:
                obstacle = pygame.Rect(obstacle_x, obstacle_y, 120, 50)
                obstacles.append(obstacle)
                win.blit(car1Img, (obstacle.x, obstacle.y))
                timeBeforeTheLastObs = 0
                pygame.display.update()
            
            for obstacle in obstacles:
                if obstacle.x < -1:
                    score += 1
                    obstacles.remove(obstacle)
                    
            for i in range(0, tiles):
                win.blit(bgImg, (i * bgWidth + scroll, -93))
            scroll -= 5
            if abs(scroll) > bgWidth:
                scroll = 0

            


                 
            score_show(x,y)
            draw_window(pl, obstacles)
            obstacle_movement(obstacles)
            pl_movement(pl)
            hit_obstacle(pl, obstacles)
            pygame.display.update()
            print(timer, buttonPressingTime, timeBeforeTheLastObs, score)
            
            for event in pygame.event.get():
                if event.type == gotHit:
                    lost = False
                    if event.type == gotHit:
                        lost = True
                        start_game = 2
                    if lost == True:
                        item_data={}

                        with open(f'{user_profile}/score.json', "r") as newfile:
                            temp1 = json.load(newfile)
                        item_data["Score"] = score
                        temp1.append(item_data)
                        with open(f'{user_profile}/score.json','w') as newfile:
                            json.dump(temp1, newfile, indent=4)

                        start_game = 2
                        timeMS = 0
                        main()
                        timeMS = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        start_game = 3


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()