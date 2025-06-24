import pygame

pygame.init()

screen  = pygame.display.set_mode((800, 800))

run = True

speed = 5
x = 400
y = 400

while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_UP:
                y -= speed
            if i.key == pygame.K_DOWN:
                y+=speed
            if i.key == pygame.K_LEFT:
                x-=speed
            if i.key == pygame.K_RIGHT:
                x+=speed
           
            x = max(25, min(x, 800 - 25))
            y = max(25, min(y, 800 - 25))

    screen.fill((255, 0, 0))
    cir = pygame.draw.circle(screen, (255, 255, 255), (x, y), 25)
    pygame.display.flip()



pygame.quit()