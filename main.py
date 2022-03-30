#######################################################
#######################################################
#######################################################
### Course Info:
###   - bugfixing and debugging concept-process
###   - fixing hit-far-from-rocket issue
#######################################################
#######################################################
#######################################################


#######################################################
# Import of all required modules/libraries
#######################################################
import os
import random
import time
import pygame as pg
from pygame.locals import *


#######################################################
# Constants
#######################################################

# Screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_CAPTION = "Tennis"
SCREEN_FPS = 60
SCREEN_ICON = "screen_icon.png"
SCREEN_BGIMAGE = "god.png"
COLOR_BLANK = pg.Color("black")

# File System
DIR_ASSETS_IMAGES = os.path.join("assets", "images")
DIR_ASSETS_SOUNDS = os.path.join("assets", "sounds")
DIR_ASSETS_MUSIC = os.path.join("assets", "music")

# Assets File Names
FILE_IMG_Player1 = "player1.png"
FILE_IMG_Player2 = "player2.png"
FILE_IMG_Ball = "ball.png"

FILE_MUS_Background = "track1.mp3"
FILE_SFX_Stroke = "stroke.wav"
FILE_SFX_Lost = "lost.wav"


#######################################################
# Utility
#######################################################

# loads image file from assets folder
def LoadImage(fileName):
    return pg.image.load(os.path.join(DIR_ASSETS_IMAGES, fileName))

# loads music file from assets folder
def LoadMusic(fileName):
    pg.mixer.music.load(os.path.join(DIR_ASSETS_MUSIC, fileName))

# loads sound file from assets folder
def LoadSound(fileName):
    return pg.mixer.Sound(os.path.join(DIR_ASSETS_SOUNDS, fileName))

# draw a given text of given size to given surface on given position
def DrawText(surface, text, size, x, y):
    font_name = pg.font.match_font("arial")
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, pg.Color('white'))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# quits to system
def QuitGame():
    pg.quit()
    exit(0)


#######################################################
# PyGame Initialization
#######################################################

pg.init()
# module for fonts
pg.font.init()
# module for loading and playing sounds & music
pg.mixer.init()

pg.display.set_icon(LoadImage(SCREEN_ICON))
pg.display.set_caption(SCREEN_CAPTION)
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()


#######################################################
# Load assets
#######################################################

# load images
IMG_background = pg.transform.scale(LoadImage(SCREEN_BGIMAGE), (SCREEN_WIDTH, SCREEN_HEIGHT))
IMG_player1 = LoadImage(FILE_IMG_Player1)
IMG_player2 = LoadImage(FILE_IMG_Player2)
IMG_ball = LoadImage(FILE_IMG_Ball)

# load music
LoadMusic(FILE_MUS_Background)

# load sounds
SFX_Stroke = LoadSound(FILE_SFX_Stroke)
SFX_Lost = LoadSound(FILE_SFX_Lost)


#######################################################
# Define sprites
#######################################################

class Player(pg.sprite.Sprite):
    # defaults
    __PLAYER_Width__ = 80
    __PLAYER_Height__ = 80
    __PLAYER_Speed__ = 5

    def __init__(self, playerImage, positionX, positionY):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(playerImage, (Player.__PLAYER_Width__, Player.__PLAYER_Height__))
        #self.image.set_colorkey(COLOR_BLANK) # not needed for images with transparent background
        self.rect = self.image.get_rect()
        #self.radius = int((Player.__PLAYER_Width__ + Player.__PLAYER_Height__) / 2)
        #pg.draw.circle(self.image, pg.Color("red"), self.rect.center, self.radius) # for collision accuracy testing purposes
        #pg.draw.rect(self.image, (255, 0, 0), (self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)
        self.rect.centerx = positionX
        self.rect.centery = positionY
        self.speedx = 0
        self.speedy = 0

    def goLeft(self, proceed = False):
        if proceed:
            self.speedx -= Player.__PLAYER_Speed__
        else:
            self.speedx = 0

    def goRight(self, proceed = False):
        if proceed:
            self.speedx += Player.__PLAYER_Speed__
        else:
            self.speedx = 0

    def goUp(self, proceed = False):
        if proceed:
            self.speedy -= Player.__PLAYER_Speed__
        else:
            self.speedy = 0

    def goDown(self, proceed = False):
        if proceed:
            self.speedy += Player.__PLAYER_Speed__
        else:
            self.speedy = 0

    def update(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

        # don't let the sprite goes over the left/right/top/bottom screen borders
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        # don't let the sprite goes over the net
        #...


class Ball(pg.sprite.Sprite):
    def __init__(self, positionX, positionY, speed):
        pg.sprite.Sprite.__init__(self)
        
        self.image = IMG_ball
        self.rect = self.image.get_rect()
        #pg.draw.rect(self.image, (255, 0, 0), (self.rect.left, self.rect.top, self.rect.width, self.rect.height), 1)
        self.rect.centerx = positionX
        self.rect.centery = positionY
        #self.init.centerx = positionX
        #self.init.centery = positionY
        self.speed = speed
        self.speedx = 0
        self.speedy = 0

    def start(self):
        self.speedx += self.speed * random.randrange(-1, 1)
        self.speedy += self.speed * random.randrange(-1, 1)
    #def reset(self):
       # self.rect.centerx
       # self.rect.centery
    def hit(self):
        xold = 1
        yold = 1
        xnew = 1
        ynew = 1

        if self.speedx < 0:
            xold = -1

        if self.speedy < 0:
            yold = -1

        self.speedx = random.randrange(self.speed*-1, self.speed)
        self.speedy = random.randrange(self.speed*-1, self.speed)

        if self.speedx < 0:
            xnew = -1

        if self.speedy < 0:
            ynew = -1

        if xold == xnew:
            self.speedx *= -1

        if yold == ynew:
            self.speedy *= -1

    def update(self):        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # don't let the sprite goes over the left/right/top/bottom screen borders
        # change direction to random opposit
        if self.rect.right > SCREEN_WIDTH:
            self.speedx *= -1
            

        if self.rect.left < 0:
            self.speedx *= -1
            
        if self.rect.top < 0:
            self.speedy *= -1
               
        if self.rect.bottom > SCREEN_HEIGHT:
            self.speedy *= -1
           
#############################
# ##########################
# Game functions
#######################################################

def HandleKeyDownEvent(KeyDownEvent):
    # player1 controll
    if KeyDownEvent.key == pg.K_LEFT:
        player1.goLeft(True)

    if KeyDownEvent.key == pg.K_RIGHT:
        player1.goRight(True)

    if KeyDownEvent.key == pg.K_UP:
        player1.goUp(True)

    if KeyDownEvent.key == pg.K_DOWN:
        player1.goDown(True)
    
    # player2 controll
    if KeyDownEvent.key == pg.K_a:
        player2.goLeft(True)

    if KeyDownEvent.key == pg.K_d:
        player2.goRight(True)

    if KeyDownEvent.key == pg.K_w:
        player2.goUp(True)

    if KeyDownEvent.key == pg.K_s:
        player2.goDown(True)

    # ball controll
    if KeyDownEvent.key == pg.K_SPACE:
        ball.start()

def HandleKeyUpEvent(KeyUpEvent):
    # Player1 Controll
    if KeyUpEvent.key == pg.K_LEFT:
        player1.goLeft(False)

    if KeyUpEvent.key == pg.K_RIGHT:
        player1.goRight(False)

    if KeyUpEvent.key == pg.K_UP:
        player1.goUp(False)

    if KeyUpEvent.key == pg.K_DOWN:
        player1.goDown(False)

    # Player2 Controll
    if KeyUpEvent.key == pg.K_a:
        player2.goLeft(False)

    if KeyUpEvent.key == pg.K_d:
        player2.goRight(False)

    if KeyUpEvent.key == pg.K_w:
        player2.goUp(False)

    if KeyUpEvent.key == pg.K_s:
        player2.goDown(False)

#######################################################
# Main + Overall Event Loop
#######################################################

pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(loops=-1)

# sprite groups to easy update of all sprites
all_sprites = pg.sprite.Group()
player_sprites = pg.sprite.Group()
ball_sprites = pg.sprite.Group()

# creation of Player sprite
player1 = Player(IMG_player2, SCREEN_WIDTH-50, SCREEN_HEIGHT-50)
player2 = Player(IMG_player1, 50, 50)
all_sprites.add(player1)
all_sprites.add(player2)
player_sprites.add(player1)
player_sprites.add(player2)

# creation of Ball sprite
ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 10)
all_sprites.add(ball)

# stores both players score
score_player1 = 0
score_player2 = 0

running = True
while running:
    # loop through all events
    for event in pg.event.get():
        # print all events in console for debug purposes
        #print(event)

        # check for closing window event
        if event.type == pg.QUIT:
            running = False
            QuitGame()
        # handle KeyDown event
        elif event.type == pg.KEYDOWN:
            HandleKeyDownEvent(event)
        # handle KeyUp event
        elif event.type == pg.KEYUP:
            HandleKeyUpEvent(event)

    # update all sprites
    all_sprites.update()

    # check for collisions between Ball and both Players sprites
    collisions = pg.sprite.spritecollide(ball, player_sprites, False, pg.sprite.collide_circle)

    if collisions:
        SFX_Stroke.play()
        #time.sleep(1)
        ball.hit()

    # clear screen to blank color OR blit a background image before drawing a sceen again
    #screen.fill(COLOR_BLANK)
    screen.blit(IMG_background, IMG_background.get_rect())

    # TODO: draw a pitch
    CenterX = SCREEN_WIDTH / 2
    CenterY = SCREEN_HEIGHT / 2
    # 10% of screen height
    OffsetX = 0.1 * SCREEN_WIDTH
    # 10% of screen width
    OffsetY = 0.1 * SCREEN_HEIGHT

    # outer rectangle
    pg.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 10)
    # net - from left bottom to top right
    pg.draw.line(screen, (255, 255, 255), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, 0), 10)
    
    # intra-top line
    pg.draw.line(screen, (255, 255, 255), (3*OffsetX, OffsetY), (SCREEN_WIDTH-OffsetX, OffsetY), 5)
    # intra-bottom line
    pg.draw.line(screen, (255, 255, 255), (OffsetX, SCREEN_HEIGHT-OffsetY), (SCREEN_WIDTH-3*OffsetX, SCREEN_HEIGHT-OffsetY), 5)

    # intra-left line
    pg.draw.line(screen, (255, 255, 255), (OffsetX, 4*OffsetY), (OffsetX, SCREEN_HEIGHT-OffsetY), 5)
    # intra-right line
    pg.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH-OffsetX, OffsetY), (SCREEN_WIDTH-OffsetX, SCREEN_HEIGHT-4*OffsetY), 5)

    # intra-top-left line
    pg.draw.line(screen, (255, 255, 255), (OffsetX, 4*OffsetY), (3*OffsetX, OffsetY), 5)
    # intra-bottom-right line
    pg.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH-3*OffsetX, SCREEN_HEIGHT-OffsetY), (SCREEN_WIDTH-OffsetX, SCREEN_HEIGHT-4*OffsetY), 5)

    # draw / render the sceen
    all_sprites.draw(screen)
    DrawText(screen, str(score_player1), 30, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 3)
    DrawText(screen, str(score_player2), 30, SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 3)

    # *after* drawing everything, flip/update the screen with what we've drawn
    pg.display.flip()
    #pg.display.update()

    # control the draw update speed
    clock.tick(SCREEN_FPS)


#######################################################
# Quit
#######################################################
QuitGame()
