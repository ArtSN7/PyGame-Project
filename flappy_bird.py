from random import randint
from sys import exit
import pygame
import os
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Game')
WIDTH = 1920
HEIGHT = 1080
clock = pygame.time.Clock()
FPS = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(name, colorkey=None, transform=None):
    fullname = os.path.join("data_flappy/" + name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if transform is not None:
        image = pygame.transform.rotate(image, transform)
    return image


between = 150
winning_coin = 0

fon = load_image("fon.png")
fon = pygame.transform.scale(fon, (WIDTH, HEIGHT))
starting_fon = load_image("starting_fon.jpg")
starting_fon = pygame.transform.scale(starting_fon, (WIDTH, HEIGHT))
pause_fon =  load_image("pause.png")
ending_fon = load_image("ending_fon.jpg")


player_image = load_image('player.png')
player_image = pygame.transform.scale(player_image, (35, 25))
pipe = load_image("pipe.png")
pipe_top = load_image("pipe.png", transform=180)


def terminate():
    pygame.quit()
    exit()


pipe_h_min = WIDTH // 8
pipe_h_max = WIDTH // 2
all_sprites = pygame.sprite.Group()
pipes_group = pygame.sprite.Group()
top_pipes = pygame.sprite.Group()
bottom_pipes = pygame.sprite.Group()
player_group = pygame.sprite.Group()

flight = False
game_over = False


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, loc="top"):
        super().__init__()
        self.image = pipe
        self.rect = self.image.get_rect()
        if loc == "top":
            top_pipes.add(self)
            self.image = pipe_top
            self.rect.bottomleft = [x, y - int(between / 2)]
        else:
            bottom_pipes.add(self)
            self.rect.topleft = [x, y + int(between / 2)]

    def update(self):
        self.rect.x -= offset
        if self.rect.right <= 0:
            self.kill()

    def pipes_coords(self):
        return self.rect


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.index_anim = 0

        self.mouse_clicked = False
        self.v = 0
        self.bet_animation = [load_image('player.png'), load_image('player1.png'),
                              load_image('player3.png'), load_image('player4.png')]

    def update(self):
        global score
        if flight:
            self.v += 0.2
            if self.v > 20:
                self.v = 0
            if self.rect.bottom < HEIGHT - 20:
                self.rect.y += int(self.v)

        if not game_over:
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.mouse_clicked = True
                self.v = -3

            if pygame.mouse.get_pressed()[0]:
                self.mouse_clicked = False
            self.rect.y += self.v
            if self.index_anim == 4:
                self.index_anim = 0
            self.image = self.bet_animation[self.index_anim]
            self.index_anim += 1


player = Player(WIDTH // 2, HEIGHT // 2)
ground_x = 0
offset = 2
score = 0
one_pipe_passed = False


def start_screen():
    screen.blit(starting_fon, (0, 0))

    global score, one_pipe_passed
    score = 0
    one_pipe_passed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x >= 650 and x <= 1250 and y >= 600 and y <= 800:
                    return 'next'
                if x >= 650 and x <= 1250 and y >= 820 and y <= 1020:
                    return 'back'
        pygame.display.flip()
        clock.tick(FPS)


def game():
    global ground, ground_x, screen, flight, game_over, score, one_pipe_passed, between, winning_coin
    pygame.display.flip()
    ticks = 1800
    last_pipe = pygame.time.get_ticks() - ticks

    pause = 1


    while True:


        if game_over:
            player.kill()
            return

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = pause * -1


            if not flight and not game_over:
                flight = True

        if pause == -1:
            screen.blit(pause_fon, (0, 0))
            pygame.display.flip()
        else:
            if pygame.sprite.groupcollide(player_group, pipes_group, False,
                                          False) or player.rect.y < 10 or player.rect.y > HEIGHT - 10:
                game_over = True

            if not game_over and flight:
                ground_x -= offset
                if abs(ground_x) > 20:
                    ground_x = 0
                time_passed = pygame.time.get_ticks()
                if time_passed == ticks or time_passed - last_pipe > ticks:
                    h = randint(0, 150)
                    bot_pipe = Pipe(WIDTH, int(HEIGHT // 2) - h, loc="bot")
                    top_pipe = Pipe(WIDTH, int(HEIGHT // 2) - h, loc="top")
                    pipes_group.add(bot_pipe)
                    pipes_group.add(top_pipe)
                    last_pipe = time_passed
                    score += 1
                if pipes_group:
                    if pipes_group.sprites()[0].rect.left < player.rect.x < pipes_group.sprites()[0].rect.right \
                            and not one_pipe_passed:
                        one_pipe_passed = True
                    if one_pipe_passed:
                        if player.rect.x > pipes_group.sprites()[0].rect.right:
                            one_pipe_passed = False
                pipes_group.update()
                player_group.update()
                screen.blit(fon, (0, 0))
                pipes_group.draw(screen)
                player_group.draw(screen)

                font2 = pygame.font.Font('fonts\\DungeonFont.ttf', 40)
                text1 = font2.render(f'Life-time: {score} blinks', True, (128, 0, 0))
                screen.blit(text1, (0, 0))

                if score >= 15:
                    font1 = pygame.font.Font('fonts\\DungeonFont.ttf', 40)
                    text2 = font1.render(f'W-Coins: 1', True, (128, 0, 0))
                    screen.blit(text2, (0, 45))

                    winning_coin = 1
                else:
                    font1 = pygame.font.Font('fonts\\DungeonFont.ttf', 40)
                    text2 = font1.render(f'W-Coins: 0', True, (128, 0, 0))
                    screen.blit(text2, (0, 45))

                pygame.display.flip()
                clock.tick(FPS)
                if score > 3:
                    between = 130
                if score > 6:
                    between = 110
                if score > 9:
                    between = 90


def end_screen():
    screen.blit(ending_fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x >= 650 and x <= 1250 and y >= 600 and y <= 800:
                    return 'next'
                if x >= 650 and x <= 1250 and y >= 820 and y <= 1020:
                    return 'back'

        pygame.display.flip()
        clock.tick(FPS)


def go():
    global winning_coin, score, game_over, flight, player, ground_x, offset, one_pipe_passed
    sound = pygame.mixer.Sound('data_artem\\mp3\\Ambient 5.mp3')
    sound.play(loops=-1)
    if start_screen() == 'next':
        while winning_coin != 1:

            game()

            flight = False
            game_over = False
            player = Player(WIDTH // 2, HEIGHT // 2)
            ground_x = 0
            offset = 2
            score = 0
            one_pipe_passed = True
            for i in pipes_group.sprites():
                i.kill()

            if winning_coin == 0:
                score = 0
                a = end_screen()
                if a == 'back':
                    return 'menu'
            else:
                return 'win to menu'
    else:
        return 'menu'