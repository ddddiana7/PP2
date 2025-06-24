import pygame
from datetime import datetime

pygame.init()

screen = pygame.display.set_mode((900, 900))

micky = pygame.image.load('micky.png')
minutes = pygame.image.load('minutes.png')
seconds = pygame.image.load('seconds.png')

rect = micky.get_rect(center = (400 ,309))


run = True

while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    screen.fill((255, 255, 255))


    time = datetime.now().time()

    seconds_angle = -(time.second * 6)
    minutes_angle = -(time.minute * 6)

    s_a = pygame.transform.rotate(seconds, seconds_angle)
    m_a = pygame.transform.rotate(minutes, minutes_angle)

    s_r = s_a.get_rect(center = (rect.centerx, rect.centery))
    m_r = m_a.get_rect(center = (rect.centerx, rect.centery))

    screen.blit(micky, rect.topleft)
    screen.blit(s_a, s_r.topleft)
    screen.blit(m_a, m_r.topleft)

    pygame.display.flip()

pygame.quit()