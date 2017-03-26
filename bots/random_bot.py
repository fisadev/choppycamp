import constants
from bots.base_bot import BaseBot
import random


class RandomBot(BaseBot):
    def act(self, map_):
        return random.choice([
            constants.UP, constants.DOWN, constants.RIGHT, constants.LEFT, constants.DANCE
        ])


def create_bot(id_, map_, other_player):
    return RandomBot(id_, map_, other_player)
