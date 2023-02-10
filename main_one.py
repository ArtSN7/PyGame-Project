import sys

import room_with_en




if room_with_en.start_screen() == 'play':
    if room_with_en.go() == 'win':
        print('win')
    elif room_with_en.go() == 'exit':
        print('exit')
else:
    sys.exit()
#if preview.choise(1) == 'new game':
#   if flappy_bird.go() == 'win to menu':
#       preview.choise(2)
