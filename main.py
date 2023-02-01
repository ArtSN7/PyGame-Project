import pygame
import sys
import os
from pygame.sprite import Group
from pygame import mixer

all_sprites = pygame.sprite.Group()
schr = 0
schu = 0
schl = 0
schd = 0


class ship():
    def __init__(self, sreen):
        self.screen = sreen
        self.image = load_image("jss.png")
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
        self.image = load_image('monster.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)

    def realise(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += 1


class bombs(pygame.sprite.Sprite):
    def __init__(self, screen, shipps):
        super(bombs, self).__init__()
        self.screen = screen
        self.image = load_image('bullit.png')
        self.rect = self.image.get_rect()
        self.speed = 1
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name, colorkey=None, transform=None):
    fullname = os.path.join("data/", name)
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


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('siv')
    size = width, height = 1200, 720
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
    kol = 20
    c = 0
    clock = pygame.time.Clock()
    playlist = list()
    playlist.append("data/music.mp3")
    playlist.append("data/music.mp3")

    pygame.mixer.music.load(playlist.pop())
    pygame.mixer.music.queue(playlist.pop())
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    hp = 3
    a = 0
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render(f'жизни:{hp}', True,
                      (180, 0, 0))

    for s in range(5):
        for i in range(22):
            m = mobs(screen)
            m.x = wd + wd * i
            m.y = ht + ht * s
            m.rect.x = m.x
            m.rect.y = m.y
            monsters.add(m)
    while a == 0:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if len(playlist) > 1:
                        pygame.mixer.music.queue(playlist.pop())

                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        schr = 1
                    if event.key == pygame.K_s:
                        schd = 1
                    if event.key == pygame.K_a:
                        schl = 1
                    if event.key == pygame.K_w:
                        schu = 1
                    if event.key == pygame.K_SPACE:
                        material = bombs(screen, shp)
                        many_bombs.add(material)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        schr = 0
                    if event.key == pygame.K_s:
                        schd = 0
                    if event.key == pygame.K_a:
                        schl = 0
                    if event.key == pygame.K_w:
                        schu = 0
            if schr == 1 and shp.rect.right <= 1220:
                shp.cc += 1
            if schd == 1 and shp.rect.bottom < 720:
                shp.cy += 1
            if schl == 1 and shp.rect.left > -20:
                shp.cc -= 1
            if schu == 1 and shp.rect.top > -20:
                shp.cy -= 1
            shp.rect.centerx = shp.cc
            shp.rect.centery = shp.cy

            shp.draw()
            many_bombs.update()
            for i in many_bombs.copy():
                if i.rect.top == 50:
                    i.image = load_image('explosion.png')
                    print("qw")
                if i.rect.top < 0:
                    many_bombs.remove(i)
            for i in many_bombs.sprites():
                i.realise()
            goto = pygame.sprite.groupcollide(many_bombs, monsters, True, True)
            print(monsters)

            if c % 20 == 0:
                monsters.update()
            if pygame.sprite.spritecollideany(shp, monsters):
                hp -= 1
                many_bombs.empty()
                monsters.empty()
                shp.relocation()
                for s in range(5):
                    for i in range(22):
                        m = mobs(screen)
                        m.x = wd + wd * i
                        m.y = ht + ht * s
                        m.rect.x = m.x
                        m.rect.y = m.y
                        monsters.add(m)

                if hp == 0:
                    exit()

            monsters.draw(screen)

            pygame.display.flip()
            screen.blit(bg, (0, 0))
            text1 = f1.render(f'жизни:{hp}', True,
                              (180, 0, 0))
            screen.blit(text1, (0, 0))
            c += 1
        pygame.quit()
