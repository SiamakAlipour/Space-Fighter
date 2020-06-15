import pygame
from pygame import mixer
import random
from math import sqrt , pow
pygame.init()
pygame.mixer.init()
Background = pygame.image.load('images/BG1.png')
width , height = 750 , 750
Screen = pygame.display.set_mode((width  ,height))
pygame.display.set_caption("Space Fighter")
ICON = pygame.image.load('images/icon.png')
pygame.display.set_icon(ICON)

clock = pygame.time.Clock()

#Background Music
ExpSound = mixer.Sound("musics/hit.wav")
ExpSound.set_volume(0.1)
hitSound = mixer.Sound("musics/Rocket.wav")
hitSound.set_volume(0.05)

PlayerIMG = pygame.image.load('images/SpaceShip.png')
EnemyIMG = pygame.image.load('images/SpaceInvader.png')
FPS = 60
RocketIMG = pygame.image.load('images/Rocket.png')
class Player:
    def __init__(self,PlayerX,PlayerY):
        self . PlayerX = PlayerX
        self . PlayerY = PlayerY
        self . speed = 6
        self.hitbox = (self.PlayerX, self.PlayerY, 64, 64)
    def draw(self,Screen):
        Screen.blit(PlayerIMG, (self.PlayerX , self.PlayerY))
        self.hitbox = (self.PlayerX, self.PlayerY, 64, 64)

class Enemy:
    def __init__(self,EnemyX,EnemyY):
        self . EnemyX = EnemyX
        self . EnemyY = EnemyY
        self.speed = 1
        self.hitbox = (self.EnemyX-3, self.EnemyY, 64, 64)
    def draw(self,Screen):
        Screen.blit(EnemyIMG,(self.EnemyX,self.EnemyY))
        self.hitbox = (self.EnemyX-3, self.EnemyY, 64, 64)

    def move(self):
        self.EnemyY += self.speed


class RocketCL:
    def __init__(self,RocketX,RocketY):
        self . RocketX = RocketX
        self . RocketY = RocketY
        self . speed = 15
        self . ready = True
    def draw(self,Screen):
        Screen.blit(RocketIMG,(self.RocketX,self.RocketY))
def main():
    def DrawScreen():
        Screen.blit(Background, (0, 0))
        text = font.render('Score :' + str(score) , 1 , (255,255,0) )
        textlives = livesfont.render('Lives :' + str(lives) , 1 , (255,255,0) )
        leveltext = Levelfont.render('Level :' + str(Level) , 1 , (255,255,0) )
        Screen.blit(text,(630,10))
        Screen.blit(textlives,(0,10))
        Screen.blit(leveltext, (0, 30))
        man.draw(Screen)
        for enemy in enemies:
            enemy.draw(Screen)
        for Rocket in Rockets:
            Rocket.draw(Screen)
        pygame.display.update()
    #main loop
    man = Player(300,600)
    enemies = []
    Rockets = []
    wavelen = 5
    start = True
    score = 0
    lives = 5
    Level = 0
    Levelfont = pygame.font.SysFont("comicsans" , 30 , True)
    livesfont = pygame.font.SysFont("comicsans" , 30 , True)
    font = pygame.font.SysFont("comicsans",30,True)
    while start:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
        if lives == 0 :
            start = False
        if len(enemies) == 0:
            Level += 1
            wavelen += 5
            for i in range(wavelen):
                enemy = Enemy(random.randint(50, width - 150), random.randint(-1500, -100))
                enemies.append(enemy)
        for enemy in enemies[:]:
            enemy.move()
            if len(enemies) == 0:
                if Level != 0 :
                    enemy.speed += Level+2
            if man.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and man.hitbox[1] + man.hitbox[3] > enemy.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > enemy.hitbox[0] and man.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                    man.PlayerX, man.PlayerY = 300, 600
                    score -= 5
                    enemies.pop(enemies.index(enemy))
                    ExpSound.play()
                    lives -= 1
            if enemy.EnemyY > 750 :
                score -= 5
                enemies.pop(enemies.index(enemy))
                lives -= 1
        for Rocket  in Rockets:
            for enemy in enemies[:]:
                distance = sqrt(pow(Rocket.RocketX-enemy.EnemyX,2) + pow(Rocket.RocketY-enemy.EnemyY,2))
                if distance < 64 :
                    score += 1
                    Rockets.pop(Rockets.index(Rocket))
                    enemies.pop(enemies.index(enemy))
                    ExpSound.play()
                else:
                    continue
            if Rocket.RocketY <  750 and Rocket.RocketY > 0 :
                Rocket . RocketY -= Rocket.speed
            else:
                Rockets.pop(Rockets.index(Rocket))


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and man.PlayerX > man.speed:
            man.PlayerX -= man.speed
        if keys[pygame.K_d] and man.PlayerX < 680:
            man.PlayerX += man.speed
        if keys[pygame.K_w]  and man.PlayerY > 0:
            man.PlayerY -= man.speed
        if keys[pygame.K_s] and man.PlayerY < 680 :
            man.PlayerY += man.speed
        if keys[pygame.K_x]:
            X = man.PlayerX + 15
            Y = man.PlayerY + 10
            if len(Rockets) < 1:
                Rockets.append(RocketCL(X,Y))
            hitSound.play()


        DrawScreen()

        pygame.display.update()
def main_menu():
    Title = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        Screen.blit(Background, (0,0))
        title_render = Title.render("Press the mouse to begin...", 1, (255,255,0))
        Screen.blit(title_render, (79, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()