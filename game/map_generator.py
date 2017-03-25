import itertools
import random
import sys
sys.path.append('../')

import visualizer
import constants
from utils import map_size


def generate(width, height, box_density=0, chopp_density=0, laptop_density=0,
             representation=constants.WALL):

    if (box_density + chopp_density + laptop_density) >= 1:
        raise ValueError('Density <= 1')

    room_width = width - 2
    room_height = height - 2
    boxes = int((room_width) * (room_height) * box_density)
    chopp = int((width - 2) * (height - 2) * chopp_density)
    laptop = int((width - 2) * (height - 2) * laptop_density)

    # matrix width lines
    matrix = [[representation if i in (0, width - 1) else constants.EMPTY for i in range(width)]
              for i in range(height)]

    # fill first and last with walls
    full_line = [representation]*width
    matrix[0] = full_line
    matrix[height-1] = full_line

    # add boxes
    empty_pairs = list(itertools.product(range(1, width - 1), range(1, height - 1)))
<<<<<<< HEAD

=======
>>>>>>> 21ee8690aeff4b28d309eefdee2a91a6a889ce5f
    random.shuffle(empty_pairs)

    for _ in range(boxes):
        pair = empty_pairs.pop(0)
        matrix[pair[1]][pair[0]] = representation

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

            if map_[row][col] == constants.EMPTY:
                map_[row][col] = thing
                added += 1


def add_room(current_map, room):
    map_width = len(current_map[0])
    map_height = len(current_map)
    room_width = len(room[0])
    room_height = len(room)

    init_x = random.randint(0, map_width - room_width)
    init_y = random.randint(0, map_height - room_height)

    for row in room:
        for index, item in enumerate(row):
            current_map[init_y][init_x + index] = item
        init_y += 1

    return current_map


if __name__ == '__main__':
    m = generate(50, 40, 0.01, 0.01, 0.05)
    r = generate(8, 8, 0, 0.2, 0.4, representation=constants.ROOM)
    m = add_room(m, r)
    v = visualizer.MapVisualizer()
    v.draw(m, None, None)
