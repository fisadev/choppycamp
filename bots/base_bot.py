import constants
from utils import find_thing, position_in_map

class BaseBot(object):
    def __init__(self, id_, map_=None, enemy=None):
        self.id = id_
        self.map = map_
        self.enemy = enemy

    def act(self, map_):
        return constants.DANCE

    def game_over(self, result, map_, scores):
        pass

    def _position(self, map_):
        return find_thing(map_, self.id)

    def _a_star(self, map_, to_point):
        closed_nodes = []
        processed = []

        initial_position = self._position(map_)

        node_to_process = {
            'coords': initial_position,
            'tile': constants.EMPTY,
            'g': 0,
            'h': self._calculate_h(initial_position, to_point),
            'points_to': None
        }
        node_to_process['F'] = node_to_process['g'] + node_to_process['h']

        while node_to_process['coords'] != to_point:
            closed_nodes.append(node_to_process)
            self._proccess_adjacent(map_, processed, node_to_process, to_point)

            node_to_process = self._next_node_to_process(processed)
        closed_nodes.append(node_to_process)

        path = self._path(closed_nodes, to_point)
        return self._next_move(path)

    def _next_move(self, path):
        import ipdb; ipdb.set_trace()
        if len(path) < 2:
            return constants.DANCE

        if path[0]['coords'][0] < path[1]['coords'][0]:
            return constants.UP
        elif path[0]['coords'][0] > path[1]['coords'][0]:
            return constants.DOWN
        elif path[0]['coords'][1] < path[1]['coords'][1]:
            return constants.RIGHT
        elif path[0]['coords'][1] > path[1]['coords'][1]:
            return constants.LEFT

        return constants.DANCE

    def _next_node_to_process(self, processed):
        return sorted(processed, key=lambda node: node['F'])[0]

    def _path(self, closed_nodes, to_point):
        path = []

        node = closed_nodes.pop()
        while node['points_to'] is not None:
            path.append(node)
            node = node['points_to']
        path.append(node)

        return list(reversed(path))

    def _proccess_adjacent(self, map_, processed, node_to_process, to_point):
        for adjacent_node in self._get_adjacent_nodes(map_, node_to_process):
            adjacent_node['g'] = node_to_process['g'] + 1
            adjacent_node['h'] = self._calculate_h(adjacent_node['coords'], to_point)
            adjacent_node['F'] = adjacent_node['g'] + adjacent_node['h']

            processed.append(adjacent_node)

    def _get_adjacent_nodes(self, map_, node_to_process):
        nodes = []

        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if drow == 0 and dcol == 0:
                    continue

                row = node_to_process['coords'][0] + drow
                column = node_to_process['coords'][1] + dcol
                if position_in_map(map_, (row, column)):
                    tile = map_[row][column]

                    if self._is_walkable(tile):
                        nodes.append({
                            'coords': (row, column),
                            'tile': tile,
                            'points_to': node_to_process
                        })

        return nodes

    def _calculate_h(self, from_coords, to_coords):
        drow = abs(from_coords[0] - to_coords[0])
        dcol = abs(from_coords[1] - to_coords[1])

        return drow + dcol

    def _is_walkable(self, tile):
        return (
            tile != constants.WALL and
            tile != self._enemy_id()
        )

    def _enemy_id(self):
        if self.id == constants.PLAYER_X:
            return constants.PLAYER_Y
        return constants.PLAYER_X
