import constants
from bots.base_bot import BaseBot
import utils


class PriorityBot(BaseBot):
    '''This bot try to find the laptops first, and then the chops'''
    def act(self, map_):
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

        closest_lap = []
        for lap in laps:
            lap_distance = distance(lap, position)
            if closest_lap:
                if lap_distance < closest_lap[1]:
                    next_step = utils.a_star(map_, position, lap)
                    if next_step != constants.DANCE:
                        closest_lap = [lap, lap_distance, next_step]
            else:
                next_step = utils.a_star(map_, position, lap)
                closest_lap = [lap, lap_distance, next_step]

        if closest_lap:
            return closest_lap[2]

        closest_chopp = []
        for chopp in chopps:
            chopp_distance = distance(chopp, position)
            if closest_chopp:
                if chopp_distance < closest_chopp[1]:
                    next_step = utils.a_star(map_, position, chopp)
                    if next_step != constants.DANCE:
                        closest_chopp = [chopp, chopp_distance, next_step]
            else:
                next_step = utils.a_star(map_, position, chopp)
                closest_chopp = [chopp, chopp_distance, next_step]

        if closest_chopp:
            return closest_chopp[2]

        else:
            return constants.DANCE


def create_bot(id_, map_, other_player):
    return PriorityBot(id_, map_, other_player)
