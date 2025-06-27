import pygame
import random

pygame.init()

#настройки экрана и блока
WIDTH, HEIGHT, BLOCK = 700, 700, 50
SCREEN = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#шрифт для очков и уровня 
all_font = pygame.font.SysFont("Verdana", 30)

#цвет фона для линии сетки 
def drawlines(screen, HEIGHT, WIDTH, block):
    for i in range(0, HEIGHT + block, block): #рисует вертикальные линии 
        pygame.draw.line(screen, (40, 40, 40), (i, 0), (i, WIDTH), 1)
    for i in range(0, WIDTH + block, block): #рисует горизонтальные линии
        pygame.draw.line(screen, (40, 40, 40), (0, i), (HEIGHT, i), 1)

#Класс точки (координаты x, y)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Класс Змейки 
class Snake:
    def __init__(self):
        self.snakebody = [Point(x=HEIGHT // 2 // BLOCK, y=WIDTH // 2 // BLOCK)]

    def draw(self):
        #Голова змейки — зеленая
        head = self.snakebody[0] #содержит все части змейки (0 это голова)
        pygame.draw.rect(SCREEN, (0, 255, 0), pygame.Rect(head.x * BLOCK, head.y * BLOCK, BLOCK, BLOCK)) #рисует блоки змейки
        #Тело змейки — темно-зеленое
        for body in self.snakebody[1:]:
            pygame.draw.rect(SCREEN, (0, 200, 100), pygame.Rect(body.x * BLOCK, body.y * BLOCK, BLOCK, BLOCK))

    def move(self, dx, dy):
        #Двигаем тело змейки за головой
        for inx in range(len(self.snakebody) - 1, 0, -1):
            self.snakebody[inx].x = self.snakebody[inx - 1].x
            self.snakebody[inx].y = self.snakebody[inx - 1].y
        self.snakebody[0].x += dx
        self.snakebody[0].y += dy
        #границы, чтобы змейка уходила на другую сторону
        if self.snakebody[0].x >= HEIGHT // BLOCK:
            self.snakebody[0].x = 0
        elif self.snakebody[0].x < 0:
            self.snakebody[0].x = HEIGHT // BLOCK - 1
        if self.snakebody[0].y >= WIDTH // BLOCK:
            self.snakebody[0].y = 0
        elif self.snakebody[0].y < 0:
            self.snakebody[0].y = WIDTH // BLOCK - 1

    def collision(self, foodx, foody): #проверяет съела ли змейка еду 
        return self.snakebody[0].x == foodx and self.snakebody[0].y == foody
        #возвращает истинность есои коородинаты головы совпадают с координатами еды


#Класс еды
class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):

        #случайные координаты еды
        self.x = random.randint(0, HEIGHT // BLOCK - 1) 
        self.y = random.randint(0, WIDTH // BLOCK - 1)

        self.weight = random.choice([1, 3, 5])  # Случайный вес еды
        self.spawn_time = pygame.time.get_ticks() #сохраняет время создания еды, чтобы удалить если еда слишком долго на экране

    def draw(self):
        #Цвет зависит от веса
        if self.weight == 1:
            color = (255, 255, 0)     #желтая
        elif self.weight == 3:
            color = (255, 165, 0)     #оранжевая
        else:
            color = (255, 0, 0)       #красная

        #рисую саму еду с выбранным цветом 
        pygame.draw.circle(SCREEN, color,
                           (self.x * BLOCK + BLOCK // 2, self.y * BLOCK + BLOCK // 2), BLOCK // 2)

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 5000  #5 секунд

#Класс Стен
class Walls:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.wall_list = [Point(x=0, y=0)]

    def draw(self):
        for i in range(0, WIDTH, BLOCK):
            pygame.draw.rect(SCREEN, (150, 150, 150), pygame.Rect(self.x, i, BLOCK - 5, BLOCK - 5))
            self.wall_list.append(Point(self.x // BLOCK, i // BLOCK))

#объекты для классов
snake = Snake()
food = Food()
walls = Walls()

# переменные
runned = True
dx, dy = 0, 0
speed = 5  #начальная скорость 
level = 1
saved_length = 0

# главный цикл
while runned:
    SCREEN.fill((0, 0, 0))
    drawlines(SCREEN, HEIGHT, WIDTH, BLOCK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runned = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy != 1:
                dx, dy = 0, -1
            elif event.key == pygame.K_DOWN and dy != -1:
                dx, dy = 0, 1
            elif event.key == pygame.K_LEFT and dx != 1:
                dx, dy = -1, 0
            elif event.key == pygame.K_RIGHT and dx != -1:
                dx, dy = 1, 0

    #движение и отрисовка объектов
    snake.move(dx, dy)
    snake.draw()
    food.draw()
    walls.draw()

    #отображение уровня и очков
    level_text = all_font.render(f"Level: {level}", True, (255, 255, 255))
    score_text = all_font.render(f"Score: {len(snake.snakebody)}", True, (255, 255, 255))
    SCREEN.blit(level_text, (10, 10))
    SCREEN.blit(score_text, (HEIGHT - 200, 10))

    # Проверка столкновения головы с телом
    for i in range(1, len(snake.snakebody)):
        if snake.collision(snake.snakebody[i].x, snake.snakebody[i].y):
            runned = False

    # Проверка столкновения со стенами
    for wall in walls.wall_list:
        if snake.collision(wall.x, wall.y):
            runned = False

    # Проверка съедания еды
    if snake.collision(food.x, food.y):
        for _ in range(food.weight):
            snake.snakebody.append(Point(food.x, food.y))
        food.respawn()
        # Проверка, не появилась ли еда на змейке или стенах
        while any(p.x == food.x and p.y == food.y for p in snake.snakebody) or \
              any(w.x == food.x and w.y == food.y for w in walls.wall_list):
            food.respawn()

    #еда исчезает через 5 секунд
    if food.expired():
        food.respawn()

    #повышение уровня
    if len(snake.snakebody) % 5 == 0 and saved_length != len(snake.snakebody):
        speed += 1
        saved_length = len(snake.snakebody)
        level += 1

    pygame.display.flip()
    clock.tick(speed)
