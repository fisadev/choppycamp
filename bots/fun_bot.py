import itertools
import functools
from copy import deepcopy

import constants
from bots.base_bot import BaseBot
import random
import utils

"""

FunBot is a bot written in functional style.

"""

QUICKY_RADIUS = 2
COOLPLACE_RADIOUS = 1
COOLPLACE_TIMER = 10
QUICKY_TIMER = 5
MAX_QUICKIES = 4

initial_state = {
    'method': None,
    'action': None,
    'quickies_targetted': set(),
    'quicky_timer': 0,
    'coolplace_timer': 0,
    'coolplace': None,
}

# Fun tools
# ---------

def assoc(_d, key, value):
    d = deepcopy(_d)
    d[key] = value
    return d

def assoc_multi(_d, d2):
    d = deepcopy(_d)
    d.update(d2)
    return d

def set_add(_set, obj):
    new_set = deepcopy(_set)
    new_set.add(obj)
    return new_set

def ireduce(func, iterable, init=None):
    if init is None:
        iterable = iter(iterable)
        curr = iterable.next()
    else:
        curr = init
    for x in iterable:
        curr = func(curr, x)
        yield curr

# Common functions
# ----------------

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_all_positions(map_):
    map_width = len(map_)
    map_height = len(map_[0])
    return itertools.product(range(map_width), range(map_height))

def get_around_positions(map_, position, radious):
    map_width = len(map_)
    map_height = len(map_[0])
    range_x = range(max(0, position[0]-radious), min(map_width, position[0]+radious+1))
    range_y = range(max(0, position[1]-radious), min(map_height, position[1]+radious+1))
    return itertools.product(range_x, range_y)

def weight(p, map_):
    thing = map_[p[0]][p[1]]
    return constants.SCORE_THINGS.get(thing, 0)

def around_weight(position, map_, radious):
    around_positions = get_around_positions(map_, position, radious)
    return sum(map(functools.partial(weight, map_=map_), around_positions))

# The quicky method
# -----------------

def get_quickything(map_, position, radious=QUICKY_RADIUS):
    around_positions = itertools.filterfalse(lambda p: p == position, get_around_positions(map_, position, radious))
    staffed_positions = filter(lambda t: map_[t[0]][t[1]] in constants.SCORE_THINGS, around_positions)
    staffed_a, staffed_b = itertools.tee(staffed_positions)
    if not any(staffed_a):
        return None
    else:
        closest = functools.partial(distance, b=position)
        return min(staffed_b, key=closest)

def quicky_act(map_, position, state):
    """If there is anything at hand, go grab it.

    There is a counter to avoid getting too much distracted with
    guickies, as grabbing one thing near after another can leave the
    bot far from the cool place.

    When the maximum of quickies is reached, a timer is set to go back
    to quicky mode.

    """
    if state['quicky_timer'] <= 0:
        return assoc_multi(state, {
            'method': 'quicky',
            'quickies_targetted': set(),
            'quicky_timer': QUICKY_TIMER,
            'action': constants.DANCE,
        })
    else:
        if len(state['quickies_targetted']) >= MAX_QUICKIES:
            return assoc_multi(state, {
                'method': 'quicky',
                'action': constants.DANCE,
                'quicky_timer': state['quicky_timer'] - 1,
            })
        else:
            quickything = get_quickything(map_, position)
            if quickything is None:
                return assoc_multi(state, {
                    'method': 'quicky',
                    'action': constants.DANCE,
                })
            else:
                return assoc_multi(state, {
                    'method': 'quicky',
                    'action': utils.a_star(map_, position, quickything),
                    'quickies_targetted': set_add(state['quickies_targetted'], quickything),
                })

# The coolplace method
# --------------------

def get_coolplace(map_, radious=COOLPLACE_RADIOUS):
    all_map = get_all_positions(map_)
    return max(all_map, key=functools.partial(around_weight, map_=map_, radious=radious))

def tick_coolplace_timer(state):
    return COOLPLACE_TIMER if state['coolplace_timer'] <= 0 else state['coolplace_timer'] - 1

def coolplace_needs_update(state):
    return state['coolplace'] is None or state['coolplace_timer'] <= 0

def coolplace_act(map_, position, state):
    """Go to a place in the map where most things are accumulated.

    There is a timer to avoid changing the target place in each step.
    Because there is a chance that more than one place are equally
    interesting.

    """
    coolplace = get_coolplace(map_) if coolplace_needs_update(state) else state['coolplace']
    action = utils.a_star(map_, position, coolplace)
    return assoc_multi(state, {
        'method': 'coolplace',
        'action': action,
        'coolplace': coolplace if action != constants.DANCE else None,
        'coolplace_timer': tick_coolplace_timer(state),
    })

# The random method
# -----------------

def random_step_act(map_, position, state):
    return assoc_multi(state, {
        'method': 'random_step',
        'action': random.choice([constants.UP, constants.DOWN,
                                 constants.RIGHT, constants.LEFT]),
    })

# The actual acting
# -----------------

def do_act(map_, position, state):
    all_methods = [
        quicky_act,       # If there is anything near, go pick it.
                          # But don't get too much distracted.
        coolplace_act,    # Otherwise go right where the bounty is.
        random_step_act,  # Otherwise make a random step,
                          # because... why not?
    ]
    applied_methods = map(lambda f: functools.partial(f, map_, position), all_methods)
    condition = lambda state: state['action'] != constants.DANCE
    return next(filter(condition, ireduce(lambda a, f: f(a), applied_methods, state)))


class FunBot(BaseBot):
    def __init__(self, *k, **w):
        super(FunBot, self).__init__(*k, **w)
        self.state = initial_state

    def act(self, map_):
        position = self._position(map_)
        self.state = do_act(map_, position, self.state)
        return self.state['action']

    def get_debug_lines(self):
        debug_lines = []
        debug_lines.append('method:   ' + self.state['method'])
        debug_lines.append('quikies:  ' + '*'*len(self.state['quickies_targetted']))
        debug_lines.append('quick t:  ' + '-'*self.state['quicky_timer'])
        debug_lines.append('cool t:   ' + '-'*self.state['coolplace_timer'])
        return debug_lines


def create_bot(id_, map_, other_player):
    return FunBot(id_, map_, other_player)
