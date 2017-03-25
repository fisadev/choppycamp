import constants
from bots.base_bot import BaseBot
import random
import utils

class NormalBot(BaseBot):
    def act(self, map_):
        laps_and_chopps = []
        position = self.position(map_)
        for i_row, row in enumerate(self.map):
            for i_colum, slot in enumerate(row):
                if slot in constants.SCORE_THINGS:
                    laps_and_chopps.append((i_row, i_colum))

        def distance(a, b):
            return sum([abs(a[i]-b[i]) for i in [0, 1]])

        closest_objective = []
        for objective in laps_and_chopps:
            objective_distance = distance(objective, position)
            if clossest_objective:
                if objective_distance < clossest_objective[1]:
                    clossest_objective = [objective, objective_distance]
            else:
                clossest_objective = [objective, objective_distance]

        if clossest_objective:
            return utils._a_star(map_, position, clossest_objective[0])

        else:
            return constants.DANCE


def create_bot(id_, map_, other_player):
    return NormalBot(id_, map_, other_player)
