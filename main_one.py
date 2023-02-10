import sys
import space_game
import room_with_en
import test_map
import flappy_bird
import preview



st = preview.start()
if st == 'new game' or st == 'continue':

    if st == 'new game':
        test_map.work_with_file(3)

    keys, final_boss, space, room, bird = test_map.work_with_file(1)


    running = True

    while running:



        if int(keys) >= 4:
            if preview.end_of_the_game() == 'finish':
                sys.exit()

        a = test_map.go()

        if a == 'space game':
            if space_game.go() == 'win':
                test_map.work_with_file(2, 'space')

        if a == 'flappy bird':
            if flappy_bird.go() == 'win to menu':
                test_map.work_with_file(2, 'bird')

        if a == 'room with enemies':
            if room_with_en.start_screen() == 'play':
                if room_with_en.go() == 'win':
                    test_map.work_with_file(2, 'room')

        if a == 'final boss':
            pass

        keys, final_boss, space, room, bird = test_map.work_with_file(1)