import pygame


pygame.init()

class DifferentScreens:
    def __init__(self, a, b, screen):
        self.display_width = a
        self.display_height = b
        self.screen = screen

        self.clock = pygame.time.Clock()
        self.run = True
        self.was_played = False

        self.start()

    def defeat(self):
        pass

    def end_of_the_game(self):
        sound = pygame.mixer.Sound('data_artem\\mp3\\Ambient 7.mp3')
        sound.play(loops=-1)

        prev = pygame.image.load(f'data_artem\\screens\\final.jpg')
        prev_rect = prev.get_rect(center=(self.display_width // 2, self.display_height // 2))
        self.screen.blit(prev, prev_rect)
        pygame.display.update()

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x >= 660 and x <= 1260 and y >= 680 and y <= 880:
                        self.run = False
                        pygame.quit()

    def start(self):

        while self.run:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN and self.was_played:
                    self.run = False

            sound = pygame.mixer.Sound('data_artem\\bird\\sound_of_bird.mp3')

            if not self.was_played:
                sound.play()

                for i in range(14):
                    prev = pygame.image.load(f'data_artem\\bird\\photo{i + 1}.jpg')
                    prev_rect = prev.get_rect(center=(self.display_width // 2, self.display_height // 2))
                    self.screen.blit(prev, prev_rect)
                    pygame.display.update()
                    pygame.time.Clock().tick(10)

                pygame.time.Clock().tick(40)
                prev = pygame.image.load(f'data_artem\\bird\\photo{15}.jpg')
                prev_rect = prev.get_rect(center=(self.display_width // 2, self.display_height // 2))
                self.screen.blit(prev, prev_rect)

                self.was_played = True
                pygame.display.update()

        self.run = True
        self.menu()

    def menu(self):
        what_return = ''
        quit_game = False

        sound = pygame.mixer.Sound('data_artem\\mp3\\Ambient 1.mp3')
        sound.play(loops=-1)

        prev = pygame.image.load(f'data_artem\\screens\\menu.jpg')
        prev_rect = prev.get_rect(center=(self.display_width // 2, self.display_height // 2))
        self.screen.blit(prev, prev_rect)
        pygame.display.update()

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()

                    if x >= 640 and x <= 1240 and y >= 220 and y <= 420:
                        what_return = 'new game'
                        self.run = False

                    elif x >= 640 and x <= 1240 and y >= 470 and y <= 670:
                        what_return = 'countinue'
                        self.run = False

                    elif x >= 640 and x <= 1240 and y >= 710 and y <= 910:
                        self.run = False
                        quit_game = True

        if not quit_game:
            sound.stop()
            self.run = True

            return what_return
        else:
            pygame.quit()



display_width = 1920
display_height = 1080

screen = pygame.display.set_mode((display_width, display_height))

DifferentScreens(display_width, display_height, screen)
