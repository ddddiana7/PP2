import pygame
import random
import time
import psycopg2
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.font.init()

# Database connection
def create_connection():
    try:
        conn = psycopg2.connect(
            database="snakedb",  
            user="postgres", 
            password="Aidosmaidos",  
            host="localhost", 
            port="5432")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
        return None

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS "User" (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS user_score (
        score_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES "User"(user_id),
        level INT NOT NULL,
        score INT NOT NULL,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()

def get_user_id(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM \"User\" WHERE username = %s", (username,))
    result = cur.fetchone()
    
    if result:
        return result[0]
    else:
        cur.execute("INSERT INTO \"User\" (username) VALUES (%s) RETURNING user_id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id

def get_last_score(conn, user_id):
    cur = conn.cursor()
    cur.execute("""
        SELECT level, score FROM user_score 
        WHERE user_id = %s 
        ORDER BY saved_at DESC 
        LIMIT 1
    """, (user_id,))
    return cur.fetchone()

def save_score(conn, user_id, level, score):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_score (user_id, level, score)
        VALUES (%s, %s, %s)
    """, (user_id, level, score))
    conn.commit()

# Game settings
WIDTH, HEIGHT, BLOCK = 700, 700, 50
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
GRID_COLOR = (40, 40, 40)
WALL_COLOR = (150, 150, 150)

# Font
all_font = pygame.font.SysFont("Verdana", 30)

# Draw grid lines
def draw_grid(screen, width, height, block):
    for i in range(0, width + block, block):
        pygame.draw.line(screen, GRID_COLOR, (i, 0), (i, height), 1)
    for i in range(0, height + block, block):
        pygame.draw.line(screen, GRID_COLOR, (0, i), (width, i), 1)

# Point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Snake class
class Snake:
    def __init__(self):
        self.snakebody = [Point(x=WIDTH // 2 // BLOCK, y=HEIGHT // 2 // BLOCK)]
        self.direction = (0, 0)  # Начинаем без движения
        self.next_direction = (0, 0)

    def draw(self):
        # Draw head
        head = self.snakebody[0]
        pygame.draw.rect(SCREEN, GREEN, pygame.Rect(head.x * BLOCK, head.y * BLOCK, BLOCK, BLOCK))
        # Draw body
        for body in self.snakebody[1:]:
            pygame.draw.rect(SCREEN, DARK_GREEN, pygame.Rect(body.x * BLOCK, body.y * BLOCK, BLOCK, BLOCK))

    def update_direction(self, dx, dy):
        # Запрещаем разворот на 180 градусов
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)

    def move(self):
        # Обновляем направление только если змейка двигалась
        if self.direction != (0, 0) or self.next_direction != (0, 0):
            self.direction = self.next_direction
            
        # Если нет направления - не двигаемся
        if self.direction == (0, 0):
            return
            
        # Move body parts
        for idx in range(len(self.snakebody) - 1, 0, -1):
            self.snakebody[idx].x = self.snakebody[idx - 1].x
            self.snakebody[idx].y = self.snakebody[idx - 1].y
            
        # Move head
        self.snakebody[0].x += self.direction[0]
        self.snakebody[0].y += self.direction[1]
        
        # Wrap around screen edges
        if self.snakebody[0].x >= WIDTH // BLOCK:
            self.snakebody[0].x = 0
        elif self.snakebody[0].x < 0:
            self.snakebody[0].x = WIDTH // BLOCK - 1
        if self.snakebody[0].y >= HEIGHT // BLOCK:
            self.snakebody[0].y = 0
        elif self.snakebody[0].y < 0:
            self.snakebody[0].y = HEIGHT // BLOCK - 1

    def collision(self, x, y):
        return self.snakebody[0].x == x and self.snakebody[0].y == y

    def check_self_collision(self):
        head = self.snakebody[0]
        for segment in self.snakebody[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

# Food class
class Food:
    def __init__(self, walls):
        self.x = 0
        self.y = 0
        self.weight = 1
        self.spawn_time = pygame.time.get_ticks()
        self.walls = walls
        self.respawn()

    def respawn(self):
        while True:
            self.x = random.randint(0, WIDTH // BLOCK - 1)
            self.y = random.randint(0, HEIGHT // BLOCK - 1)
            
            # Проверяем, чтобы еда не появлялась на стенах
            valid_position = True
            for wall in self.walls.wall_list:
                if wall.x == self.x and wall.y == self.y:
                    valid_position = False
                    break
                    
            if valid_position:
                break
                
        self.weight = random.choice([1, 3, 5])
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
        if self.weight == 1:
            color = YELLOW
        elif self.weight == 3:
            color = ORANGE
        else:
            color = RED

        # Квадратная еда вместо круглой
        pygame.draw.rect(SCREEN, color, 
                        (self.x * BLOCK, self.y * BLOCK, BLOCK, BLOCK))

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 5000  # 5 seconds

# Walls class
class Walls:
    def __init__(self, level=1):
        self.wall_list = []
        self.level = level
        self.create_walls()

    def create_walls(self):
        # Clear existing walls
        self.wall_list = []
        
        # Border walls
        for x in range(0, WIDTH, BLOCK):
            self.wall_list.append(Point(x // BLOCK, 0))
            self.wall_list.append(Point(x // BLOCK, (HEIGHT - BLOCK) // BLOCK))
        for y in range(0, HEIGHT, BLOCK):
            self.wall_list.append(Point(0, y // BLOCK))
            self.wall_list.append(Point((WIDTH - BLOCK) // BLOCK, y // BLOCK))
        
        # Level-specific walls
        if self.level >= 2:
            for x in range(5, 10):
                self.wall_list.append(Point(x, 10))
        
        if self.level >= 3:
            for y in range(5, 15):
                self.wall_list.append(Point(15, y))

    def draw(self):
        for wall in self.wall_list:
            pygame.draw.rect(SCREEN, WALL_COLOR, 
                           (wall.x * BLOCK, wall.y * BLOCK, BLOCK - 5, BLOCK - 5))

    def check_collision(self, x, y):
        for wall in self.wall_list:
            if wall.x == x and wall.y == y:
                return True
        return False

# Show message on screen
def show_message(surface, msg, color, size=48, y_offset=0):
    font = pygame.font.SysFont("Verdana", size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    surface.blit(text, text_rect)

# Pause game
def pause_game(conn, user_id, level, score):
    save_score(conn, user_id, level, score)
    paused = True
    
    while paused:
        SCREEN.fill(BLACK)
        show_message(SCREEN, "PAUSED", YELLOW)
        show_message(SCREEN, "Press P to continue", WHITE, 24, 50)
        show_message(SCREEN, "Press Q to quit", WHITE, 24, 80)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    paused = False
                elif event.key == K_q:
                    return False
    
    return True

# Welcome screen
def show_welcome_screen(username, last_level, last_score):
    SCREEN.fill(BLACK)
    show_message(SCREEN, f"Welcome, {username}!", GREEN)
    
    if last_level:
        show_message(SCREEN, f"Last level: {last_level}", WHITE, 24, 50)
        show_message(SCREEN, f"Last score: {last_score}", WHITE, 24, 80)
    else:
        show_message(SCREEN, "New player! Starting from level 1", WHITE, 24, 50)
    
    show_message(SCREEN, "Press any key to start", WHITE, 24, 120)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            if event.type == KEYDOWN:
                waiting = False
    return True

# Game over screen
def show_game_over_screen(score, level):
    SCREEN.fill(BLACK)
    show_message(SCREEN, "GAME OVER", RED)
    show_message(SCREEN, f"Final Score: {score}", WHITE, 24, 50)
    show_message(SCREEN, f"Level: {level}", WHITE, 24, 80)
    show_message(SCREEN, "Press R to restart", WHITE, 24, 120)
    show_message(SCREEN, "Press Q to quit", WHITE, 24, 150)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return True
                elif event.key == K_q:
                    return False

# Main game loop
def game_loop(conn, username):
    user_id = get_user_id(conn, username)
    last_score = get_last_score(conn, user_id)
    
    if last_score:
        last_level, last_score = last_score
    else:
        last_level, last_score = None, None
    
    if not show_welcome_screen(username, last_level, last_score):
        return False
    
    # Initialize game objects
    level = 1
    walls = Walls(level)
    snake = Snake()
    food = Food(walls)  # Передаем стены для проверки позиции еды
    speed = 5
    score = 0
    saved_length = 0
    
    running = True
    while running:
        SCREEN.fill(BLACK)
        draw_grid(SCREEN, WIDTH, HEIGHT, BLOCK)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                return False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.update_direction(0, -1)
                elif event.key == K_DOWN:
                    snake.update_direction(0, 1)
                elif event.key == K_LEFT:
                    snake.update_direction(-1, 0)
                elif event.key == K_RIGHT:
                    snake.update_direction(1, 0)
                elif event.key == K_p:
                    if not pause_game(conn, user_id, level, score):
                        return False
        
        # Move snake
        snake.move()
        
        # Check collisions with walls
        if walls.check_collision(snake.snakebody[0].x, snake.snakebody[0].y):
            save_score(conn, user_id, level, score)
            return show_game_over_screen(score, level)
        
        # Check self-collision
        if snake.check_self_collision():
            save_score(conn, user_id, level, score)
            return show_game_over_screen(score, level)
        
        # Check food collision
        if snake.collision(food.x, food.y):
            # Add segments based on food weight
            for _ in range(food.weight):
                snake.snakebody.append(Point(food.x, food.y))
            score += food.weight
            food.respawn()
            
            # Ensure food doesn't spawn on snake or walls
            while any(p.x == food.x and p.y == food.y for p in snake.snakebody) or \
                  walls.check_collision(food.x, food.y):
                food.respawn()
            
            # Level up every 5 points
            if score // 5 > (score - food.weight) // 5:
                level += 1
                speed += 1
                walls = Walls(level)
                food.walls = walls  # Обновляем ссылку на стены для еды
        
        # Check food expiration
        if food.expired():
            food.respawn()
        
        # Draw everything
        walls.draw()
        food.draw()
        snake.draw()
        
        # Display score and level
        level_text = all_font.render(f"Level: {level}", True, WHITE)
        score_text = all_font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(level_text, (10, 10))
        SCREEN.blit(score_text, (WIDTH - 150, 10))
        
        pygame.display.flip()
        clock.tick(speed)
    
    return False

def main():
    conn = create_connection()
    if conn is None:
        print("Failed to connect to database. Exiting.")
        return
    
    create_tables(conn)
    
    username = input("Enter your username: ")
    
    restart = True
    while restart:
        restart = game_loop(conn, username)
    
    conn.close()
    pygame.quit()

if __name__ == "__main__":
    main()