WALL = '#'
CHOPP = 'i'
LAPTOP = 'L'
PYTHONISTA1 = 'x'
PYTHONISTA2 = 'y'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
DANCE = 'dance'

ACTIONS = UP, DOWN, LEFT, RIGHT, DANCE

PLAYERS = PYTHONISTA1, PYTHONISTA2
SCORE_THINGS = {
    CHOPP: 1,
    LAPTOP: 5,
}

ACTION_DELTAS = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1),
    DANCE: (0, 0),
}

WON = 'won'
LOST  = 'lost'
TIE = 'tie'

RESULTS = WON, LOST, TIE
