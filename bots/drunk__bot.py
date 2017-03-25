import constants
from bots.base_bot import BaseBot
import random
import utils

class DrunkBot(BaseBot):
    def act(self, map_):
        chopps = []
        laps = []
        position = self.position(map_)
        for i_row, row in enumerate(self.map):
            for i_colum, slot in enumerate(row):
                if slot == constants.CHOPP:
                    chopps.append((i_row, i_colum))
                elif slot == constants.LAPTOP:
                    laps.append((i_row, i_colum))

        def distance(a, b):
            return sum([abs(a[i]-b[i]) for i in [0, 1]])

        closest_chopp = []
        for chopp in chopps:
            chopp_distance = distance(chopp, position)
            if closest_chopp:
                if chopp_distance < closest_chopp[1]:
                    closest_chopp = [chopp, chopp_distance]
            else:
                closest_chopp = [chopp, chopp_distance]

        if closest_chopp:
            return utils._a_star(map_, position, closest_chopp[0])

        else:
            return constants.DANCE


def create_bot(id_, map_, other_player):
    return DrunkBot(id_, map_, other_player)
