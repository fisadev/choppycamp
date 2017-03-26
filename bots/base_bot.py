import constants
from utils import find_thing, position_in_map

class BaseBot(object):
    def __init__(self, id_, map_=None, enemy=None):
        self.id = id_
        self.map = map_
        self.enemy = enemy

    def act(self, map_):
        return constants.DANCE

    def game_over(self, result, map_, scores):
        pass

    def _position(self, map_):
        return find_thing(map_, self.id)

    def _enemy_id(self):
        if self.id == constants.PLAYER_X:
            return constants.PLAYER_Y
        return constants.PLAYER_X
