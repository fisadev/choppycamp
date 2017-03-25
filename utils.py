import importlib
import constants


def find_thing(map_, target):
    for r_number, columns in enumerate(map_):
        for c_number, thing in enumerate(columns):
            if thing == target:
                return r_number, c_number

    raise ValueError('Target not found: ' + target)


def map_size(map_):
    return len(map_), len(map_[0])


def position_in_map(map_, position):
    row, col = position
    rows, columns = map_size(map_)
    return 0 <= row < rows and 0 <= col < columns


def get_bot(bot_name, id_, other_player, map_):
    module = importlib.import_module('bots.%s' % bot_name)
    bot = module.create_bot(id_, map_, other_player)
    return bot


def a_star_calculate_h( from_coords, to_coords):
    drow = abs(from_coords[0] - to_coords[0])
    dcol = abs(from_coords[1] - to_coords[1])

    return drow + dcol


def next_move(path):
    if not path:
        return constants.DANCE
    return path[0]['action']


def next_node_to_process( pending_nodes):
    return sorted(pending_nodes, key=lambda node: node['F'])[0]


def path(objective):
    result = []

    node = objective
    while node['points_to'] is not None:
        result.append(node)
        node = node['points_to']

    return list(reversed(result))


def proccess_adjacent(map_, pending_nodes, closed_nodes, node_to_process, to_point):
    for adjacent_node in get_adjacent_nodes(map_, closed_nodes, node_to_process):
        adjacent_node['g'] = node_to_process['g'] + 1
        adjacent_node['h'] = a_star_calculate_h(adjacent_node['coords'], to_point)
        adjacent_node['F'] = adjacent_node['g'] + adjacent_node['h']

        if already_visited(pending_nodes, adjacent_node['coords']):
            continue

        pending_nodes.append(adjacent_node)


def already_visited(closed_nodes, coords):
    for node in closed_nodes:
        if node['coords'] == coords:
            return True
    return False


def is_walkable(tile):
    return tile not in [
        constants.WALL,
        constants.BOX,
        constants.PLAYER_X,
        constants.PLAYER_Y
    ]


def get_adjacent_nodes(map_, closed_nodes, node_to_process):
    nodes = []

    for action, (drow, dcol) in constants.ACTION_DELTAS.items():
        if action == constants.DANCE:
            continue

        row = node_to_process['coords'][0] + drow
        column = node_to_process['coords'][1] + dcol

        if already_visited(closed_nodes, (row, column)):
            continue

        if not position_in_map(map_, (row, column)):
            continue

        tile = map_[row][column]

        if is_walkable(tile):
            nodes.append({
                'coords': (row, column),
                'tile': tile,
                'points_to': node_to_process,
                'action': action
            })

    return nodes


def a_star(map_, from_point, to_point):
    closed_nodes = []

    initial_position = from_point

    node_to_process = {
        'coords': initial_position,
        'tile': constants.EMPTY,
        'g': 0,
        'h': a_star_calculate_h(initial_position, to_point),
        'points_to': None,
        'action': constants.DANCE
    }
    node_to_process['F'] = node_to_process['g'] + node_to_process['h']

    pending_nodes = [node_to_process]

    while pending_nodes:
        node_to_process = next_node_to_process(pending_nodes)
        pending_nodes.remove(node_to_process)
        closed_nodes.append(node_to_process)

        if node_to_process['coords'] == to_point:
            return next_move(path(node_to_process))

        proccess_adjacent(map_, pending_nodes, closed_nodes, node_to_process, to_point)
    return constants.DANCE
