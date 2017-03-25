import constants
from bots.base_bot import BaseBot
import random


class RandomBot(BaseBot):
    def _move(self):
        return RandomBot([constants.UP,
                          contstants.DOWN,
                          constants.RIGHT,
                          constants.LEFT,
                          constants.DANCE,
                          ])
