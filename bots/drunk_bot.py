import constants
from bots.base_bot import BaseBot
import random
import utils

class DrunkBot(BaseBot):

    def __init__(self, id_, map_=None, enemy=None):
        super(DrunkBot, self).__init__(id_, map_, enemy)
        self.drunk = False

    def act(self, map_):
        if self.drunk:
            self.drunk = False
            return constants.DANCE

        chopps = []
        laps = []
        position = self._position(map_)
        for i_row, row in enumerate(map_):
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
            if distance(closest_chopp[0], position) == 1:
                self.drunk = True
            return utils.a_star(map_, position, closest_chopp[0])

        else:
            return constants.DANCE


def create_bot(id_, map_, other_player):
    return DrunkBot(id_, map_, other_player)
