EMPTY = '.'
WALL = '#'
ROOM = '@'
CHOPP = 'U'
LAPTOP = 'L'
PLAYER_X = 'x'
PLAYER_Y = 'y'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
DANCE = 'dance'

ACTIONS = UP, DOWN, LEFT, RIGHT, DANCE

PLAYERS = PLAYER_X, PLAYER_Y

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
