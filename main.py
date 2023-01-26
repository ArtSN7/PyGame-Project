import pygame


pygame.init()


display_width = 1200
display_height = 720

screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()



run = True
was_played = False

while run:
    clock.tick(60)

    # handle the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    sound = pygame.mixer.Sound('data_artem\\sound_of_bird.mp3')


    if not was_played:
        sound.play()
        for i in range(14):
            prev = pygame.image.load(f'data_artem\\photo{i + 1}.jpg')
            prev_rect = prev.get_rect(center=(1200 // 2, 720 // 2))
            screen.blit(prev, prev_rect)
            pygame.display.update()
            pygame.time.Clock().tick(10)
        was_played = True

        prev = pygame.image.load(f'data_artem\\photo{15}.jpg')
        prev_rect = prev.get_rect(center=(1200 // 2, 720 // 2))
        screen.blit(prev, prev_rect)
    pygame.display.flip()



pygame.quit()


