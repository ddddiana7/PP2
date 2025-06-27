import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()

#main 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60 # сколько фпс в секунду
SPEED = 5 # начальная скорость
SCORE = 0 #нач скор
COINS_COLLECTED = 0  #amount of coins

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#fonts
font_large = pygame.font.SysFont("Verdana", 60)#текст и фон 
font_small = pygame.font.SysFont("Verdana", 20)#цвет текста
game_over = font_large.render("GAME OVER", True, BLACK)# надписб после проигрыша

#window and background
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
background = pygame.image.load("AnimatedStreet.png")
bg_y = 0

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()#прямоугольник который описывает положение и размеры игрока
        self.rect.center = (160, 520) #центр картинки

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:# проверяет нажата ли кнопка лево и находится ли игрок у левого края экрана 
            self.rect.move_ip(-5, 0) #движение влево 
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)#движение вправо

#enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load("Pygame_rects.png")
        self.image = pygame.transform.rotate(self.image_original, 180)
        self.rect = self.image.get_rect()  #прямоугольник который описывает положение и размеры врага
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50) #центр картинки

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED) #двигает врага вниз по экрану на speed пикселей 
        if self.rect.top > SCREEN_HEIGHT: # не вышел ли за нижнюю границу экрана 
            SCORE += 1 #засчитывается если враг зашел за границу
            self.rect.top = -50
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50) #враг перемещается обратно вверх

#coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30)) #меняет размер монеты
        self.rect = self.image.get_rect()#создает прямоугольник который описывает полоэение и размеры монеты на экране
        self.value = random.choice([1, 3, 5])  #разные значения монет
        self.respawn() #заново спавнятся

    def move(self):
        pass #для совместимости с другими классами

    def respawn(self):
        # Случайное положение и новая ценность
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40),
                            random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT - 50))
        self.value = random.choice([1, 3, 5])

#создаю объекты для классов
player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group() #создаю группу врагов
enemies.add(enemy) # в эту группу добавляю объект enemy из класса enemy

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)

#таймер для постепенного увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED:
            SPEED += 0.5  #постепенное ускорение

    #прокрутка фона
    bg_y += SPEED
    if bg_y >= SCREEN_HEIGHT:
        bg_y = 0

    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - SCREEN_HEIGHT))

    #обработка движения всех спрайтов
    for sprite in all_sprites:
        sprite.move()
        screen.blit(sprite.image, sprite.rect)

    #отображение счёта
    score_display = font_small.render(f"Score: {SCORE}", True, BLACK) #создает изображение с текстом
    coin_display = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK) #то же саоме
    screen.blit(score_display, (10, 10))  #отображает Score: ... в левом верхнем углу (координаты 10, 10)
    screen.blit(coin_display, (10, 30)) #отображает Coins: ... на 20 пикселей ниже

    #столкновение с монетой
    if pygame.sprite.spritecollideany(player, coins):
        SCORE += coin.value #увеличение score
        COINS_COLLECTED += 1 #считает сколько монет собрали
        coin.respawn() #спавнит новые монеты

        #увеличение скорости при сборе каждой 5-й монеты
        if COINS_COLLECTED % 5 == 0:
            SPEED += 1  #можно менять на 0.5 или другое значение

    #столкновение с врагом
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.Sound("crash.wav").play()#
        time.sleep(1) #пауза на одну секунда для звука
        screen.fill(RED)#экран смерти
        screen.blit(game_over, (30, 250))#
        pygame.display.update()#обновляю
        time.sleep(2)#пауза на две секунды для надписи
        pygame.quit()#модули выкл
        sys.exit()#выходит из циклов

    pygame.display.update()#j,yjdkz. 'rhfy
    clock.tick(FPS) #60 кадров в секунду
