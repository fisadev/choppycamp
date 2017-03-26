import constants
from bots.base_bot import BaseBot
import utils


class PartyBot(BaseBot):
    def act(self, map_):
        if self.id == constants.PLAYER_X:
            other = constants.PLAYER_Y
        else:
            other = constants.PLAYER_X

        my_position = utils.find_thing(map_, self.id)
        other_position = utils.find_thing(map_, other)

        def distance(a, b):
            return sum([abs(a[i]-b[i]) for i in [0, 1]])

        if distance(my_position, other_position) == 1:
            next_step = constants.DANCE
        else:
            # remove to make that position reachable by astar
            map_[other_position[0]][other_position[1]] = constants.EMPTY
            next_step = utils.a_star(map_, my_position, other_position)

        return next_step

def create_bot(id_, map_, other_player):
    return PartyBot(id_, map_, other_player)
