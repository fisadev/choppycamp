import constants
from bots.base_bot import BaseBot
import random
import utils

class PriorityBot(BaseBot):
    '''This bot try to find the laptops first, and then the chops'''
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

        closest_lap = []
        for lap in laps:
            lap_distance = distance(lap, position)
            if closest_lap:
                if lap_distance < closest_lap[1]:
                    closest_lap = [lap, lap_distance]
            else:
                closest_lap = [lap, lap_distance]

        if closest_lap:
            return utils._a_star(map_, position, closest_lap[0])

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
    return PriorityBot(id_, map_, other_player)
