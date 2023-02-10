import pygame
import sys
import os


pygame.init()
pygame.display.set_caption('Game')


def load_image(name, dir="data_artem", colorkey=None, transform=None):
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


WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
image_of_cursor = pygame.transform.scale(load_image("cursor.png"), (80, 50))
fon = pygame.transform.scale(load_image('starting_map.png'), (WIDTH, HEIGHT))



def work_with_file(do, *args):
    with open('results.txt', 'r+', encoding='UTF-8') as file:
        # reading
        final_boss = False
        space = False
        room = False
        bird = False

        if do == 1:
            file = [i.strip() for i in file.readlines()]
            if "final boss" in file:
                final_boss = True
            if "space" in file:
                space = True
            if "room" in file:
                room = True
            if "bird" in file:
                bird = True

            if len(file) != 0:
                return list(file[0])[-1], final_boss, space, room, bird
            else:
                return '0', final_boss, space, room, bird

        #writing
        if do == 2:
            past_info = [i.strip() for i in file.readlines()]
            file.truncate(0)

            if len(past_info) != 1:
                new_info = [str(int(list(past_info[0])[-1]) + 1)] + past_info[1:] + [args[0]]
            else:
                new_info = [str(int(list(past_info[0])[-1]))]

            for i in new_info:
                file.write(i)
                file.write('\n')



def go():
    global running, clock, screen, fon, image_of_cursor, final_boss, space, room, bird, keys

    position = (960, 640)
    was = False
    was1 = False

    while running:
        screen.blit(fon, (0, 0))
        screen.blit(image_of_cursor, position)

        font1 = pygame.font.Font('fonts\\DungeonFont.ttf', 40)
        text2 = font1.render(f'Keys: {keys}', True, (255, 255, 255))
        screen.blit(text2, (0, 0))

        if was:
            font1 = pygame.font.Font('fonts\\DungeonFont.ttf', 40)
            text2 = font1.render(f'It is completed! Try another', True, (255, 255, 255))
            screen.blit(text2, (650, 300))
        if was1:
            font1 = pygame.font.Font('fonts\\DungeonFont.ttf', 40)
            text2 = font1.render(f'Need more keys', True, (255, 255, 255))
            screen.blit(text2, (650, 300))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused():
                    pygame.mouse.set_visible(False)
                    position = pygame.mouse.get_pos()

                else:
                    pygame.mouse.set_visible(True)

            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = pygame.mouse.get_pos()
                was = False
                was1 = False

                if 640 <= x <= 820 and 0 <= y <= 210:
                    if int(keys) != 3:
                        was1 = True
                    elif final_boss:
                        was = True
                    else:
                        return 'final boss'

                if 70 <= x <= 230 and 90 <= y <= 240:
                    if space:
                        was = True

                    else:
                        return 'space game'

                if 520 <= x <= 670 and 470 <= y <= 620:
                    if room:
                        was = True
                    else:
                        return 'room with enemies'

                if 1130 <= x <= 1280 and 470 <= y <= 620:
                    if bird:
                        was = True

                    else:
                        return 'flappy bird'

        pygame.display.flip()


keys, final_boss, space, room, bird = work_with_file(1)