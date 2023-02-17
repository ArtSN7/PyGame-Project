import os
import sys
import pygame
from pygame.sprite import Group
import random

all_sprites = pygame.sprite.Group()
schr = 0
schu = 0
schl = 0
schd = 0


class ship():
    def __init__(self, sreen):
        self.screen = sreen
        self.image = load_image('jss.png')
        self.rect = self.image.get_rect()

        self.rect.centerx = sreen.get_rect().centerx
        self.rect.centery = sreen.get_rect().centery
        self.rect.bottom = self.screen.get_rect().bottom

        self.cc = float(self.rect.centerx)
        self.cy = float(self.rect.centery)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def relocation(self):
        self.cc = self.screen.get_rect().centerx
        self.cy = 680


class mobs(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(mobs, self).__init__()
        self.screen = screen
        ls = ['monster.png', 'octo.png']

        self.image = load_image(random.choice(ls))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)

    def realise(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += 7


class bombs(pygame.sprite.Sprite):
    def __init__(self, screen, shipps):
        super(bombs, self).__init__()
        self.screen = screen
        self.image = load_image('bullit.png')
        self.rect = self.image.get_rect()
        self.speed = 7
        self.shipps = shp.rect

        self.rect.centerx = shp.rect.centerx
        self.rect.top = shp.rect.top
        self.y_pos = self.rect.y
        self.x_pos = self.rect.x

    def update(self):
        self.y_pos -= self.speed
        self.rect.y = self.y_pos

    def realise(self):
        self.screen.blit(self.image, self.rect)


class health:
    def __init__(self, screen, eall):
        self.number = hp
        self.screen = screen
        self.images = ['3hearts.png', '2hearts.png', '1heart.png']

        if self.number == 3:
            self.image = load_image(self.images[0])
            self.rect = self.image.get_rect()

        elif self.number == 2:
            self.image = load_image(self.images[1])
            self.rect = self.image.get_rect()

        else:
            self.image = load_image(self.images[2])
            self.rect = self.image.get_rect()

        self.rect.top = self.screen.get_rect().top
        self.rect.left = self.screen.get_rect().left + 120

    def realise(self):
        self.screen.blit(self.image, self.rect)


def load_image(name, colorkey=None, transform=None):
    fullname = os.path.join("data_max/", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def end_screen():
    playlist.append("data_max/ehh.mp3")
    playlist.append("data_max/ehh.mp3")

    pygame.mixer.music.load(playlist.pop())
    pygame.mixer.music.queue(playlist.pop())
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()

    fon = pygame.transform.scale(load_image('game over.jpg'), (1920, 1080))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    playlist.clear()
                    playlist.append("data_max/music.mp3")
                    playlist.append("data_max/music.mp3")
                    pygame.mixer.music.load(playlist.pop())
                    pygame.mixer.music.queue(playlist.pop())
                    pygame.mixer.music.set_endevent(pygame.USEREVENT)
                    pygame.mixer.music.play()
                    return


def start_screen():
    fon = load_image('starting_screen.png')
    screen.blit(fon, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return


def go():
    playlist.append("data_max/music.mp3")
    playlist.append("data_max/music.mp3")
    # pygame.mixer.music.load(playlist.pop())
    # pygame.mixer.music.queue(playlist.pop())
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(100)

    global screen, rows, running, shooter, schd, schr, schu, schl, c, shp, hp, cr

    start_screen()

    znach = ''

    for s in range(rows):
        for i in range(32):
            m = mobs(screen)
            m.x = wd + wd * i + 100
            m.y = ht + ht * s
            m.rect.x = m.x
            m.rect.y = m.y
            monsters.add(m)

    rows += 1

    pause = 1
    pause_fon = load_image('pause.png')
    winning_of_space = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if len(playlist) > 1:
                    pygame.mixer.music.queue(playlist.pop())

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = pause * -1
                pygame.mouse.set_visible(False)

            if event.type == pygame.MOUSEBUTTONUP and pause == -1:
                x, y = pygame.mouse.get_pos()
                if 630 <= x <= 1930 and 870 <= y <= 1070:
                    znach = 'exit'
                    running = False

            if pause == -1:
                pygame.mouse.set_visible(True)
                screen.blit(pause_fon, (0, 0))
                pygame.display.flip()
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(100)

                if shooter == True:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        material = bombs(screen, shp)
                        many_bombs.add(material)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        schr = 1
                    if event.key == pygame.K_s:
                        schd = 1
                    if event.key == pygame.K_a:
                        schl = 1
                    if event.key == pygame.K_w:
                        schu = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        schr = 0
                    if event.key == pygame.K_s:
                        schd = 0
                    if event.key == pygame.K_a:
                        schl = 0
                    if event.key == pygame.K_w:
                        schu = 0

        if schr == 1 and shp.rect.right <= 1830:
            shp.cc += 2
        if schd == 1 and shp.rect.bottom < height:
            shp.cy += 2
        if schl == 1 and shp.rect.left > 80:
            shp.cc -= 2
        if schu == 1 and shp.rect.top > -20:
            shp.cy -= 2

        shp.rect.centerx = shp.cc
        shp.rect.centery = shp.cy
        shp.draw()
        many_bombs.update()

        for i in many_bombs.copy():
            if i.rect.top == 50:
                i.image = load_image('explosion.png')
            if i.rect.top < 0:
                many_bombs.remove(i)

        for i in many_bombs.sprites():
            i.realise()

        goto = pygame.sprite.groupcollide(many_bombs, monsters, True, True)

        if c % 20 == 0:
            monsters.update()

        if pygame.sprite.spritecollideany(shp, monsters):
            hp -= 1
            many_bombs.empty()
            monsters.empty()
            shp.relocation()
            for s in range(rows - 1):
                for i in range(32):
                    m = mobs(screen)
                    m.x = wd + wd * i + 100
                    m.y = ht + ht * s
                    m.rect.x = m.x
                    m.rect.y = m.y
                    monsters.add(m)
            if hp <= 0:
                if rows >= 6:
                    monsters.empty()
                    winning_of_space = True
                else:
                    end_screen()
                    monsters.empty()
                rows = 1
                hp = 3
        cr += 1

        font2 = pygame.font.Font('fonts\\DungeonFont.ttf', 40)
        text1 = font2.render(f'Attacks passed: {rows - 2}', True, (128, 0, 0))
        screen.blit(text1, (1400, 0))

        if rows >= 6:
            text2 = font2.render(f'W-KEY: 1', True, (128, 0, 0))
            screen.blit(text2, (1700, 0))
            winning_of_space = True
        else:
            text2 = font2.render(f'W-KEY: 0', True, (128, 0, 0))
            screen.blit(text2, (1700, 0))

        if len(monsters) == 0:
            shooter = False
            if cr % 2000 == 0:
                shooter = True
                for s in range(rows):
                    for i in range(32):
                        m = mobs(screen)
                        m.x = wd + wd * i + 100
                        m.y = ht + ht * s
                        m.rect.x = m.x
                        m.rect.y = m.y
                        monsters.add(m)
                r1 = rows

                rows += 1

        monsters.draw(screen)
        for i in monsters.sprites():
            if i.rect.bottom == screen.get_rect().bottom:
                hp = 3
                end_screen()
        hl = health(screen, hp)
        hl.realise()

        if pause != -1:
            pygame.display.flip()
            screen.blit(bg, (0, 0))
            c += 1

        if winning_of_space:
            znach = 'win'
            running = False

    return znach


pygame.init()
pygame.display.set_caption('siv')
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
shp = ship(screen)
bg = load_image('bgr.jpg')
bmb = bombs(screen, shp)
monsters = Group()
pygame.display.flip()
many_bombs = Group()
running = True
m = mobs(screen)
wd = m.rect.width
ht = m.rect.height
c = 0
rows = 1

new = False
clock = pygame.time.Clock()

playlist = list()
playlist.append("data_max/music.mp3")
playlist.append("data_max/music.mp3")
shooter = True

pygame.mixer.music.load(playlist.pop())
pygame.mixer.music.queue(playlist.pop())
pygame.mixer.music.set_endevent(pygame.USEREVENT)
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0)

hp = 3
b = False
f1 = pygame.font.Font(None, 36)
cr = 0

wave = 0
schu = 0
hl = health(screen, hp)
