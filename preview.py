import pygame


pygame.init()


display_width, display_height = 1920, 1080
screen = pygame.display.set_mode((display_width, display_height))


clock = pygame.time.Clock()
run = True
was_played = False
n = 1




def end_of_the_game():
    global run, display_height, display_width, was_played
    sound = pygame.mixer.Sound('data_artem\\mp3\\Ambient 7.mp3')
    sound.play(loops=-1)

    prev = pygame.image.load(f'data_artem\\screens\\final.jpg')
    prev_rect = prev.get_rect(center=(display_width // 2, display_height // 2))
    screen.blit(prev, prev_rect)
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x >= 660 and x <= 1260 and y >= 680 and y <= 880:
                    run = False
    return 'finish'

def start():
    global run, display_height, display_width, was_played

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and was_played:
                run = False

        sound = pygame.mixer.Sound('data_artem\\bird\\sound_of_bird.mp3')

        if not was_played:
            sound.play()

            for i in range(14):
                prev = pygame.image.load(f'data_artem\\bird\\photo{i + 1}.jpg')
                prev_rect = prev.get_rect(center=(display_width // 2, display_height // 2))
                screen.blit(prev, prev_rect)
                pygame.display.update()
                pygame.time.Clock().tick(10)

            pygame.time.Clock().tick(40)
            prev = pygame.image.load(f'data_artem\\bird\\photo{15}.jpg')
            prev_rect = prev.get_rect(center=(display_width // 2, display_height // 2))
            screen.blit(prev, prev_rect)

            was_played = True
            pygame.display.update()

    run = True
    return menu()

def menu():
    global run, display_height, display_width, was_played
    what_return = ''
    quit_game = False
    pygame.mouse.set_visible(True)

    sound = pygame.mixer.Sound('data_artem\\mp3\\Ambient 1.mp3')
    sound.play(loops=-1)

    prev = pygame.image.load(f'data_artem\\screens\\menu.jpg')
    prev_rect = prev.get_rect(center=(display_width // 2, display_height // 2))
    screen.blit(prev, prev_rect)
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                if x >= 640 and x <= 1240 and y >= 220 and y <= 420:
                    what_return = 'new game'
                    run = False

                elif x >= 640 and x <= 1240 and y >= 470 and y <= 670:
                    what_return = 'countinue'
                    run = False

                elif x >= 640 and x <= 1240 and y >= 710 and y <= 910:
                    run = False
                    quit_game = True

    if not quit_game:
        sound.stop()
        run = True
        return what_return
    else:
        pygame.quit()

def choise(a):
    global n
    n = a
    return main_thing()


def main_thing():
    global n
    if n == 1:
        return start()
    else:
        return end_of_the_game()
