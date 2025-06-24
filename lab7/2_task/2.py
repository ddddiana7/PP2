import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))

current =0
is_playing = False
start = False

run = True
lst = ["BTS - So What.mp3", "Doja Cat - Agora Hills.mp3", "Lady Gaga - Judas.mp3", "Tommy February6 - Lonely In Gorgeous.mp3" ]
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_F7: #предыдущий
                current-=1

                if current < 0:
                    current = len(lst) - 1

                pygame.mixer.music.load(lst[current])
                pygame.mixer.music.play()
                is_playing =True
                start= True

            if i.key == pygame.K_F8: #включить остановить

                if not is_playing and not start:
                    pygame.mixer.music.load(lst[current])
                    pygame.mixer.music.play()
                    is_playing = True
                    start = True
                    
                elif is_playing:
                    pygame.mixer.music.pause()
                    is_playing=False

                else:
                    pygame.mixer.music.unpause()
                    is_playing=True

            if i.key == pygame.K_F9: #следующий
                current+=1
                if current < 0:
                    current = len(lst)-1

                pygame.mixer.music.load(lst[current])
                pygame.mixer.music.play()
                is_playing=True
                start = True

pygame.quit()