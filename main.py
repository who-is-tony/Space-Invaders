import pygame, time
from pygame import mixer

ghostwait = 0
newghost = False
startup = True

#screen
pygame.init()
screen = pygame.display.set_mode((800,600))
screen.fill((0, 0, 0))

#bg
bg = pygame.transform.scale(pygame.image.load("bg.jpg").convert_alpha(), (1200, 800))
bg.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)

#bg sound
mixer.music.load("bg.wav")
mixer.music.play(-1)

#title icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("rickastleyserum.png")
pygame.display.set_icon(icon)

#score
scoreval = 0
scorefont = pygame.font.Font("BaiJamjuree-Bold.ttf", 32)

def score():
    score = scorefont.render("Score: " + str(scoreval), True, (255, 255, 255))
    screen.blit(score, (10,3))

#title
def title():
    tfont = pygame.font.Font("BaiJamjuree-Bold.ttf", 90)
    ttext = tfont.render("Space Invaders", True, (255, 255, 255))
    screen.blit(ttext, (75, 50))
    playstart()

#game over
def gameover():
    gofont = pygame.font.Font("BaiJamjuree-Bold.ttf", 80)
    gotext = gofont.render("Game Over", True, (255, 255, 255))
    screen.blit(gotext, (175, 225))
    playstart()

def playstart():
    psfont = pygame.font.Font("BaiJamjuree-Bold.ttf", 40)
    pstext = psfont.render("Press any key to start", True, (255, 255, 255))
    screen.blit(pstext, (185, 500))

#player
playerimage = pygame.transform.scale(pygame.image.load("space-invaders.png"), (64, 64))
playerX = 370
playerY = 480
playerXmove = 0

def player(x, y):
    screen.blit(playerimage, (x, y))

#ghost
ghostimage = []
ghostX = []
ghostY = []
ghostXmove = []
ghostnum = 6

ghostimage.append(pygame.transform.scale(pygame.image.load("ghost.png"), (64, 64)))
ghostX.append(736)
ghostY.append(50)
ghostXmove.append(-0.2)


def ghost(x, y):
    screen.blit(ghostimage[0], (x, y))

#bullet
bulletimg = pygame.transform.scale(pygame.image.load("bullet.png"), (32, 32))
bulletX = 390
bulletY = 480
bulletYmove = 1
fire = False

def firebullet(x, y):
    global fire
    fire = True
    screen.blit(bulletimg, (x + 16, y + 10))



#exit code
quitexit = False
while quitexit == False:

    screen.fill((0, 0, 0))  #leave this line above all in the while loop
    screen.blit(bg, (-50, -100))

    if newghost:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quitexit = True
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT:
                    playerXmove = -0.3
                if i.key == pygame.K_RIGHT:
                    playerXmove = 0.3
                if i.key == pygame.K_SPACE:
                    if fire == False:
                        bulletX = playerX
                        laser = mixer.Sound("laser.wav")
                        laser.play()
                        fire = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RSHIFT] and keys[pygame.K_SLASH]:
                    newghost = False
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT:
                    playerXmove = 0

        #player boundaries
        playerX += playerXmove
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        #ghost movement
        for i in range(len(ghostX)):

            #Game Over
            if ghostimage[i].get_rect(x = ghostX[i], y = ghostY[i]).colliderect(playerimage.get_rect(x = playerX, y=playerY)) or not newghost:
                newghost = False
                for j in range(len(ghostX)):
                    ghostY[j] = -2000 - (j * 128)
                    ghostX[j] = 200
            else:
                ghostX[i] += ghostXmove[i]
                if ghostX[i] <= 0:
                    ghostX[i] = 10
                    ghostY[i] += 80
                    ghostXmove[i] = 0.2
                elif ghostX[i] >= 736:
                    ghostX[i] = 726
                    ghostY[i] += 80
                    ghostXmove[i] = -0.2
                if ghostY[i] >=600:
                    ghostY[i] = 50


        #bullet movement
        if bulletY <= -33:
            bulletY = 480
            fire = False

        for i in range(len(ghostX)):
            if ghostimage[i].get_rect(x = ghostX[i], y = ghostY[i]).colliderect(bulletimg.get_rect(x = bulletX, y=bulletY)):
                if not ghostY[i] >= 430:
                    scoreval += 1
                    ghostX[i] = 736
                    ghostY[i] = 50
                    bulletY = 480
                    fire = False
                    hit = mixer.Sound("explosion.wav")
                    hit.set_volume(0.5)
                    hit.play()
            for j in range(len(ghostX)):
                if i == j:
                    continue
                if ghostimage[i].get_rect(x = ghostX[i], y = ghostY[i]).colliderect(ghostimage[j].get_rect(x = ghostX[j], y=ghostY[j])):
                    if ((ghostY[i] / 80) - 50) % 2 <= 1:
                        ghostX[i] -= 128
                    else:
                        ghostX[i] += 128
            if newghost == False:
                ghostXmove[i] = 0
            elif ((ghostY[i]/80)-50)%2 <= 1:
                ghostXmove[i] = -0.2
            else:
                ghostXmove[i] = 0.2



        if fire == True:
            firebullet(bulletX, bulletY)
            bulletY -= bulletYmove

        if ghostwait == 500 and len(ghostX) < ghostnum or ghostwait >= 2000:
            if newghost == True:
                ghostimage.append(pygame.transform.scale(pygame.image.load("ghost.png"), (64, 64)))
                ghostX.append(736)
                ghostY.append(50)
                ghostXmove.append(-0.2)
                ghostwait = 0


        player(playerX, playerY)
        for i in range(len(ghostX)):
            ghost(ghostX[i], ghostY[i])
        ghostwait += 1
        score()
    else:
        if startup:
            title()
        else:
            gameover()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                quitexit = True
            if i.type == pygame.KEYDOWN:
                newghost = True
                startup = False
                #code being weird so this is reset function
                scoreval = 0
                playerX = 370
                playerY = 480
                playerXmove = 0
                ghostimage = []
                ghostX = []
                ghostY = []
                ghostXmove = []
                ghostimage.append(pygame.transform.scale(pygame.image.load("ghost.png"), (64, 64)))
                ghostX.append(736)
                ghostY.append(50)
                ghostXmove.append(-0.2)
                bulletX = 370
                bulletY = 480
                bulletYmove = 1
                fire = False

    pygame.display.update()