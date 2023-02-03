import flappy_bird
import preview


if preview.choise(1) == 'new game':
    if flappy_bird.go() == 'win to menu':
        preview.choise(2)