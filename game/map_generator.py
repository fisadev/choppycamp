import itertools
import random
import sys
sys.path.append('../')

import constants
from utils import map_size


def generate(width, height, box_density=0, chopp_density=0, laptop_density=0):
    # if (box_density + chopp_density + laptop_density) >= 1:
    #     raise ValueError('Density sumatory should be less than 1')

    room_width = width - 2
    room_height = height - 2
    boxes = int((room_width) * (room_height) * box_density)
    chopp = int((width - 2) * (height - 2) * chopp_density)
    laptop = int((width - 2) * (height - 2) * laptop_density)

    # matrix width lines
    matrix = [[constants.WALL if i in (0, width - 1) else constants.EMPTY for i in range(width)]
              for i in range(height)]

    # fill first and last with walls
    full_line = [constants.WALL]*width
    matrix[0] = full_line
    matrix[height-1] = full_line

    # add boxes
    empty_pairs = list(itertools.product(range(1, width - 1), range(1, height - 1)))
    random.shuffle(empty_pairs)

    for _ in range(boxes):
        pair = empty_pairs.pop(0)
        matrix[pair[1]][pair[0]] = constants.WALL

    for _ in range(chopp):
        pair = empty_pairs.pop(0)
        matrix[pair[1]][pair[0]] = constants.CHOPP

    for _ in range(laptop):
        pair = empty_pairs.pop(0)
        matrix[pair[1]][pair[0]] = constants.LAPTOP

    return matrix


def add_things_randomly(map_, quantities):
    rows, columns = map_size(map_)

    for thing, quantity in quantities.items():
        added = 0
        while added < quantity:
            row = random.randint(0, rows - 1)
            col = random.randint(0, columns - 1)

            if not map_[row][col]:
                map_[row][col] = thing
                added += 1
