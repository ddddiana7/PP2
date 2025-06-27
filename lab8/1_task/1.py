import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
SPEED = 5
SCORE = 0

#COLORS
WHITE = (255, 255, 255) #текст и фон
BLACK = (0, 0, 0) #цвет текста
RED = (255, 0, 0) #экран смерти

#FONTS
font_large = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font_large.render("GAME OVER", True, BLACK)

#DISPLAY
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock() #для фпс

#BACKGROUND
background = pygame.image.load("AnimatedStreet.png")
bg_y = 0 #вертикальная позиция фона для эффекта движения дороги вниз

#PLAYER CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520) #центр картинки

    def move(self):#движение игрока
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

#Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load("Pygame_rects.png")
        self.image = pygame.transform.rotate(self.image_original, 180)  # Поворачиваем машину к игроку
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)  # Старт за верхом экрана

    def move(self):#движение врага
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = -50
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)


#Coin Class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30)) #уменьшаем картинку
        self.rect = self.image.get_rect()
        self.respawn() #cнова появляется в другом месте

    def move(self):
        pass  #Coin doesn't move, but method is needed for consistency

    def respawn(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40),
                            random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 50))


#объекты для классов
player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)

#увеличение скорости со временем
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#главный цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() #заканчивает модули пайгейма
            sys.exit() #заканчивает циклы
        if event.type == INC_SPEED:
            SPEED += 0.5 #увеличивает скорость 

    #движение фона
    bg_y += SPEED
    if bg_y >= SCREEN_HEIGHT:
        bg_y = 0
    #фон движется вниз, создавая эффект движения дороги
    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - SCREEN_HEIGHT))

    #все объекты двигаются и рисуются на экране
    for sprite in all_sprites:
        sprite.move()
        screen.blit(sprite.image, sprite.rect)

    #счет считается в углу экрана
    score_display = font_small.render(f"Score: {SCORE}", True, BLACK)
    screen.blit(score_display, (10, 10))

    #если игрок касается монетки то получает 5 очков 
    if pygame.sprite.spritecollideany(player, coins):
        SCORE += 5
        coin.respawn()

    #столкновение с врагом
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.Sound("crash.wav").play() #звук ааврии
        time.sleep(1) #пауза на одна сек чтобы звук проигрался
        screen.fill(RED) #кровавый экран
        screen.blit(game_over, (30, 250)) #GAME OVER
        pygame.display.update() #обновляем
        time.sleep(2)# пауза на две секунды чтобы было видно надпись
        pygame.quit()# выключает все модули 
        sys.exit() # выходит из всех циклов

    pygame.display.update()
    clock.tick(FPS) #фпс