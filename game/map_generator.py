import itertools
import random

from game import visualizer
import constants
from utils import map_size, is_valid_position, is_walkable


__all__ = ['build_map']


def add_item(matrix, items_amount, empty_pairs, representation):
    for _ in range(items_amount):
        pair = empty_pairs.pop(0)
        matrix[pair[1]][pair[0]] = representation
    return matrix


def generate(width, height, box_density=0, chopp_density=0, laptop_density=0):

    if (box_density + chopp_density + laptop_density) >= 1:
        raise ValueError('Density <= 1')

    room_width = width - 2
    room_height = height - 2

    boxes = int((room_width) * (room_height) * box_density)
    chopp = int((width - 2) * (height - 2) * chopp_density)
    laptop = int((width - 2) * (height - 2) * laptop_density)

    # matrix width lines
    matrix = [[constants.WALL_VERTICAL if i in (0, width - 1) else constants.EMPTY
              for i in range(width)]
              for i in range(height)]

    # fill first and last with walls
    full_line = [constants.WALL_HORIZONTAL] * width
    matrix[0] = full_line
    matrix[height-1] = full_line

    empty_pairs = list(itertools.product(range(1, width - 1), range(1, height - 1)))
    random.shuffle(empty_pairs)

    add_item(matrix, boxes, empty_pairs, constants.BOX)
    add_item(matrix, chopp, empty_pairs, constants.CHOPP)
    add_item(matrix, laptop, empty_pairs, constants.LAPTOP)

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


def overlap_matrices(m1, m2, init_x, init_y):
    room_wall_positions = []
    for row in m2:
        for index, item in enumerate(row):
            m1[init_y][init_x + index] = item

            # keep track m2 wall positions
            if item in constants.WALL_COMPOSITION:
                room_wall_positions.append((init_x + index, init_y))
        init_y += 1
    return m1, room_wall_positions


def add_door(current_map, room_wall_positions):
    random.shuffle(room_wall_positions)
    for _ in range(len(room_wall_positions)):
        x, y = room_wall_positions.pop(0)

        available_top = is_valid_position(current_map, y + 1, x) and \
            is_walkable(current_map[y + 1][x])
        available_bottom = is_valid_position(current_map, y - 1, x) and \
            is_walkable(current_map[y - 1][x])
        available_left = is_valid_position(current_map, y, x + 1) and \
            is_walkable(current_map[y][x + 1])
        available_right = is_valid_position(current_map, y, x - 1) and \
            is_walkable(current_map[y][x - 1])

        if (all([available_top, available_bottom]) or all([available_left, available_right])):
            current_map[y][x] = constants.EMPTY
            break
    return current_map


def add_room(current_map, room):
    map_width = len(current_map[0])
    map_height = len(current_map)
    room_width = len(room[0])
    room_height = len(room)

    init_x = random.randint(0, map_width - room_width)
    init_y = random.randint(0, map_height - room_height)

    current_map, room_wall_positions = overlap_matrices(current_map, room, init_x, init_y)

    # crate door logic
    random.shuffle(room_wall_positions)

    current_map = add_door(current_map, room_wall_positions)

    return current_map


def build_map(map_width, map_height, room_width, room_height,
              box_density, chopp_density, laptop_density,
              room_box_density, room_chopp_density, room_laptop_density, rooms):
    """Principal function used by the game, the rest should be private for this module."""
    m = generate(map_width, map_height, box_density, chopp_density, laptop_density)
    r = generate(room_width, room_height, room_box_density, room_chopp_density, room_laptop_density)
    for _ in range(rooms):
        m = add_room(m, r)

    return m


def main():
    m = generate(50, 40, 0.01, 0.01, 0.05)
    r = generate(8, 8, 0, 0.2, 0.4)
    m = add_room(m, r)
    v = visualizer.MapVisualizer()
    v.draw(m, None, None)
