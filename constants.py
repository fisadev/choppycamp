CLEAR = '\033[0m'
BOLD = '\033[1m'
REVERSE = '\033[7m'

RED = '\033[31m'
BLUE = '\033[34m'
YELLOW = '\033[93m'
GREEN = '\033[32m'
MAGENTA = '\033[35m'


EMPTY = ' '
WALL = '{0}#{1}'.format(MAGENTA, CLEAR)
CHOPP = '{0}{1}U{2}'.format(BOLD, YELLOW, CLEAR)
LAPTOP = '{0}{1}L{2}'.format(BOLD, BLUE, CLEAR)
PLAYER_X = '{0}{1}x{2}'.format(BOLD, RED, CLEAR)
PLAYER_Y = '{0}{1}y{2}'.format(BOLD, GREEN, CLEAR)
ROOM = '{0}@{1}'.format(MAGENTA, CLEAR)

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
