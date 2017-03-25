WALL = '#'
CHOPP = 'i'
LAPTOP = 'L'
PYTHONISTA1 = 'x'
PYTHONISTA2 = 'y'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

ACTIONS = UP, DOWN, LEFT, RIGHT
PLAYERS = PYTHONISTA1, PYTHONISTA2

ACTION_DELTAS = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1),
}
