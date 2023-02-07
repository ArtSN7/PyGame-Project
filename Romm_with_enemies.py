import pygame
import sys
import os
import math
from random import randint

pygame.init()
pygame.display.set_caption('Game')
WIDTH = 1300
HEIGHT = 800
clock = pygame.time.Clock()


class Spritesheet:
    def __init__(self, file):
        self.sheet = load_image(file)

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey("BLACK")
        return sprite


def load_level(filename, dir="data"):
    filename = f"{dir}/{filename}"
    if not os.path.isfile(filename):
        print(f"Файл '{filename}' не найден")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level = load_level("level.txt")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30


def load_image(name, dir="data", colorkey=None, transform=None):
    fullname = os.path.join(f"{dir}/{name}")
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
    if transform is not None:
        image = pygame.transform.flip(image, True, False)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА"]

    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    intro_text = ["КОНЦОВКА"]
    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
all_bombs = pygame.sprite.Group()
all_booms = pygame.sprite.Group()
all_objects = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
all_monsters = pygame.sprite.Group()
all_mobs = pygame.sprite.Group()
player_attacks = pygame.sprite.Group()
coin = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    player_pos = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == "a":
                Tile('empty', x, y)
                Monster(x, y)
            elif level[y][x] == "b":
                Tile('empty', x, y)
                Bomb(x, y)
            elif level[y][x] == "c":
                Tile('empty', x, y)
                Coin(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                player_pos = x, y
                new_player = Player(x, y)
    return new_player, x, y, player_pos


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
tile_width = tile_height = 50
time_passed = 0


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, all_objects)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == "wall":
            walls_group.add(self)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coin)
        self.width = tile_width
        self.height = tile_height
        self.x = pos_x * tile_width
        self.y = pos_y * tile_height
        self.animation_loop = 0
        self.animations = [load_image(name) for name in
                           ("coin_01.png", "coin_02.png", "coin_03.png", "coin_04.png", "coin_05.png", "coin_06.png",
                            "coin_07.png", "coin_08.png")]
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 8:
            self.animation_loop = 0

    def collide(self):
        global win
        if pygame.sprite.spritecollideany(self, player_group) and not win:
            win = True
            self.kill()


class Bomb(pygame.sprite.Sprite):
    bomb = load_image("bomb.png")
    boom = load_image("boom.png")

    def __init__(self, pos_x, pos_y):
        super().__init__(all_bombs, all_mobs)
        self.image = Bomb.bomb
        self.boom = Bomb.boom
        self.rect = self.image.get_rect()
        width, height = self.rect.size
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y
        self.speed = 2
        self.stop = False
        self.HP = 1
        self.countdown = 0
        self.new_rect = self.rect

    def update(self):
        if self.HP <= 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, player_group):
            self.image = self.boom
            all_booms.add(self)
            all_bombs.remove(self)
            self.stop = True
        self.prev_rect = self.rect
        dx = self.rect.x - player.rect.x
        dy = self.rect.y - player.rect.y
        dist = math.sqrt(dx * dx + dy * dy)
        ox1 = ox = oy = oy1 = False
        if not self.stop and 0 <= dist <= 200:
            if self.rect.x <= player.rect.x:
                self.rect.x += self.speed
                ox1 = True
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed
                ox = True
            if self.rect.y > player.rect.y:
                self.rect.y -= self.speed
                oy1 = True
            elif self.rect.y <= player.rect.y:
                self.rect.y += self.speed
                oy = True
        if pygame.sprite.spritecollideany(self, walls_group) is not None:
            self.rect = self.prev_rect
            if ox1:
                self.rect.x -= self.speed
            if ox:
                self.rect.x += self.speed
            if oy:
                self.rect.y -= self.speed
            if oy1:
                self.rect.y += self.speed


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_monsters, all_mobs)
        self.animations_walking_right = [load_image(name, colorkey=-1) for name in
                                         ("monster_1.png", "monster_2.png", "monster_3.png",
                                          "monster_4.png")]
        self.animations_walking_left = [load_image(name, transform=True, colorkey=-1) for name in
                                        ("monster_1.png", "monster_2.png", "monster_3.png",
                                         "monster_4.png")]
        self.animation_w_loop = 0
        self.image = self.animations_walking_right[self.animation_w_loop]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = tile_width * pos_x + tile_width // 2
        self.rect.y = tile_height * pos_y + tile_height // 2
        self.speed = 1
        self.stop = False
        self.HP = 20
        self.prev_rect = self.rect
        self.velocity = 1
        self.direction = randint(0, 1)
        self.last_atk = 0

    def animate_walking(self):
        if self.direction:
            self.image = self.animations_walking_left[math.floor(self.animation_w_loop)]
            self.animation_w_loop += 0.5
            if self.animation_w_loop >= 4:
                self.animation_w_loop = 0
        if not self.direction:
            self.image = self.animations_walking_right[math.floor(self.animation_w_loop)]
            self.animation_w_loop += 0.5
            if self.animation_w_loop >= 4:
                self.animation_w_loop = 0

    def move(self):
        self.animate_walking()
        if pygame.sprite.spritecollideany(self, walls_group):
            if self.direction:
                self.direction = 0
            else:
                self.direction = 1
        if self.rect.x >= (WIDTH - self.rect.size[0]):
            self.direction = 1
        elif self.rect.x <= self.rect.size[0]:
            self.direction = 0
        if not self.direction:
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity

    def update(self):
        if self.HP <= 0:
            self.kill()
        else:
            dx = self.rect.x - player.rect.x
            dy = self.rect.y - player.rect.y
            dist = math.sqrt(dx * dx + dy * dy)
            self.prev_rect = self.rect
            ox1 = ox = oy = oy1 = False
            if not self.stop and 0 <= dist <= 200:
                if self.rect.x <= player.rect.x:
                    self.rect.x += self.speed
                    ox1 = True
                elif self.rect.x > player.rect.x:
                    self.rect.x -= self.speed
                    ox = True
                if self.rect.y >= player.rect.y:
                    self.rect.y -= self.speed
                    oy1 = True
                elif self.rect.y < player.rect.y:
                    self.rect.y += self.speed
                    oy = True
                if pygame.sprite.spritecollideany(self, walls_group) is not None:
                    self.rect = self.prev_rect
                    if ox1:
                        self.rect.x -= self.speed
                    if ox:
                        self.rect.x += self.speed
                    if oy:
                        self.rect.y -= self.speed
                    if oy1:
                        self.rect.y += self.speed
            else:
                self.velocity = 1
                self.move()


class PlayerAttack(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, d):
        super().__init__(player_attacks)
        self.width = tile_width
        self.height = tile_height
        self.x = pos_x - self.width // 4
        self.y = pos_y - self.height // 4
        self.animation_loop = 0
        self.animations = [load_image(name, colorkey=-1) for name in
                           ("a1 (1).png", "a1 (2).png", "a1 (3).png", "a1 (4).png", "a1 (5).png", "a1 (6).png")]
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.d = d
        self.last_atk = 0

    def update(self):
        self.animate()
        self.collide()

    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.animation_loop += 1
        if self.animation_loop >= 6:
            self.kill()

    def collide(self):
        global attack, atk_timer
        if attack:
            hits = pygame.sprite.spritecollide(self, all_mobs, False)
            if time_passed - self.last_atk >= 1000:
                for enemy in hits:
                    enemy.HP -= player.ATK
                    self.last_atk = time_passed
                    attack = False


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.HP = 10
        self.ATK = 3

        self.animations_walking_right = [load_image(name, dir="Fire_Warrior/Walk") for name in
                                         ("Fire_Warrior_Walk1.png", "Fire_Warrior_Walk2.png", "Fire_Warrior_Walk3.png",
                                          "Fire_Warrior_Walk4.png", "Fire_Warrior_Walk5.png", "Fire_Warrior_Walk6.png",
                                          "Fire_Warrior_Walk7.png", "Fire_Warrior_Walk8.png")]
        self.animations_walking_left = [load_image(name, dir="Fire_Warrior/Walk", transform=True) for name
                                        in
                                        ("Fire_Warrior_Walk1.png", "Fire_Warrior_Walk2.png", "Fire_Warrior_Walk3.png",
                                         "Fire_Warrior_Walk4.png", "Fire_Warrior_Walk5.png", "Fire_Warrior_Walk6.png",
                                         "Fire_Warrior_Walk7.png", "Fire_Warrior_Walk8.png")]
        self.animation_w_loop = 0
        self.image = self.animations_walking_right[self.animation_w_loop]

        self.animations_atk_right = [load_image(name, dir="Fire_Warrior/Attack_3") for name in
                                     ("Fire_Warrior_Attack3_1.png", "Fire_Warrior_Attack3_2.png",
                                      "Fire_Warrior_Attack3_3.png",
                                      "Fire_Warrior_Attack3_4.png", "Fire_Warrior_Attack3_5.png")]
        self.animations_atk_left = [load_image(name, dir="Fire_Warrior/Attack_3", transform=True) for name
                                    in
                                    ("Fire_Warrior_Attack3_1.png", "Fire_Warrior_Attack3_2.png",
                                     "Fire_Warrior_Attack3_3.png",
                                     "Fire_Warrior_Attack3_4.png", "Fire_Warrior_Attack3_5.png")]
        self.animation_h_loop = 0
        self.animations_hit_right = [load_image(name, dir="Fire_Warrior/Hit") for name in
                                     ("Fire_Warrior_Hit1.png", "Fire_Warrior_Hit2.png",
                                      "Fire_Warrior_Hit3.png",
                                      "Fire_Warrior_Hit4.png")]
        self.animations_hit_left = [load_image(name, dir="Fire_Warrior/Hit", transform=True) for name
                                    in ("Fire_Warrior_Hit1.png", "Fire_Warrior_Hit2.png",
                                        "Fire_Warrior_Hit3.png",
                                        "Fire_Warrior_Hit4.png")]
        self.animation_a_loop = 0
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.prev_rect = self.rect
        self.orientation = "no"

    def animate_walking(self):
        if self.orientation == "left" or self.orientation == "top":
            self.image = self.animations_walking_left[math.floor(self.animation_w_loop)]
            self.animation_w_loop += 1
            if self.animation_w_loop >= 8:
                self.animation_w_loop = 0
        if self.orientation == "right" or self.orientation == "bot":
            self.image = self.animations_walking_right[math.floor(self.animation_w_loop)]
            self.animation_w_loop += 1
            if self.animation_w_loop >= 8:
                self.animation_w_loop = 0

    def animate_attacking(self):
        if self.orientation == "left" or self.orientation == "top":
            self.image = self.animations_atk_left[math.floor(self.animation_a_loop)]
            for i in range(5):
                self.animation_a_loop += 1
                if self.animation_a_loop >= 5:
                    self.animation_a_loop = 0
        if self.orientation == "right" or self.orientation == "bot":
            self.image = self.animations_atk_right[math.floor(self.animation_a_loop)]
            for i in range(5):
                self.animation_a_loop += 1
                if self.animation_a_loop >= 5:
                    self.animation_a_loop = 0

    def update(self):
        if self.HP <= 0:
            global game_over
            game_over = True
        global x, y, speed
        self.prev_rect = self.rect
        self.rect.x, self.rect.y = x, y
        if pygame.sprite.spritecollideany(self, walls_group) is not None:
            self.rect = self.prev_rect
            if ox1:
                x -= speed
            if ox:
                x += speed
            if oy1:
                y -= speed
            if oy:
                y += speed
            self.orientation = "no"
        else:
            if moved_once and not attack:
                self.animate_walking()
        hit_list = pygame.sprite.spritecollide(self, all_mobs, False)
        for enemy in hit_list:
            if enemy in all_bombs:
                self.HP -= 10
            elif enemy in all_monsters:
                if time_passed - enemy.last_atk >= 500:
                    self.image = self.animations_hit_right[math.floor(self.animation_h_loop)]
                    for i in range(40):
                        self.animation_h_loop += 0.1
                        if self.animation_h_loop >= 4:
                            self.animation_h_loop = 0
                    self.HP -= 4
                    enemy.last_atk = time_passed


# не работает:w
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - WIDTH // 2)


game_over = False
player, level_x, level_y, player_pos = generate_level(level)
x, y = player_pos
x *= tile_width
x += 15
y *= tile_height
y += 5
start_screen()
mon_change_dir = False
running = True
pygame.mouse.set_visible(False)
surf = pygame.Surface((WIDTH, HEIGHT))
tiles_group.draw(surf)
camera = Camera()
speed = 2
atk_timer = 0
attack = True
win = False
moved_once = False
while running:
    if not game_over:
        attack = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and time_passed - atk_timer >= 400:
                if player.orientation == "bot":
                    PlayerAttack(player.rect.x, player.rect.y + tile_height // 2, player.orientation)
                elif player.orientation == "top":
                    PlayerAttack(player.rect.x, player.rect.y - tile_height // 2, player.orientation)
                elif player.orientation == "right":
                    PlayerAttack(player.rect.centerx, player.rect.y, player.orientation)
                elif player.orientation == "left":
                    PlayerAttack(player.rect.x - tile_width // 4, player.rect.y, player.orientation)
                player.animate_attacking()
                attack = True
                atk_timer = time_passed
        keys = pygame.key.get_pressed()
        ox = oy = ox1 = oy1 = False
        time_passed = pygame.time.get_ticks()
        font = pygame.font.Font(None, 30)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x -= speed
            ox = True
            player.orientation = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x += speed
            ox1 = True
            player.orientation = "right"
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y -= speed
            oy = True
            player.orientation = "top"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y += speed
            oy1 = True
            player.orientation = "bot"
        if not ox and not ox1 and not oy and not oy1:
            moved_once = False
        else:
            moved_once = True
        all_sprites.draw(surf)
        screen.blit(surf, (0, 0))
        player.update()
        all_bombs.update()
        for boom in all_booms.sprites():
            boom.countdown += 1
            if boom.countdown >= 20:
                boom.kill()
        all_bombs.draw(screen)
        all_booms.draw(screen)
        all_monsters.update()
        coin.update()
        player_attacks.update()
        all_monsters.draw(screen)
        player_attacks.draw(screen)
        player_group.draw(screen)
        coin.draw(screen)
        text_coord = 30
        for line in ["Player HP: " + str(player.HP)]:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        clock.tick(FPS)
        pygame.display.flip()
        attack = True
        screen.fill((255, 255, 255))
    else:
        end_screen()
