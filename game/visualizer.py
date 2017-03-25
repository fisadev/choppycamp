import shutil
import time
import os

import sys
sys.path.append('../')

from constants import PLAYER_X, PLAYER_Y, DANCE, UP

class MapVisualizer():
    def __init__(self, fps=3):
        self.fps = fps
        self.max_cols, self.max_raws = shutil.get_terminal_size()

    def check_map_size(self, map_matrix):
        if len(map_matrix) > self.max_raws:
            raise ValueError("Raw len {} > {}".format(len(map_matrix), self.max_raws))

        for raw in map_matrix:
            if len(raw) > self.max_cols:
                raise ValueError("Col len {} > {}".format(len(raw), self.max_cols))

    def draw_matrix(self, matrix):
        for raw in matrix:
            line = ''
            for tile in raw:
                line = line + tile
            print(line)

    def draw(self, map_matrix, actions, score):
        self.check_map_size(map_matrix)

        os.system('clear')
        if actions is not None:
            if actions[PLAYER_X] == DANCE or actions[PLAYER_Y] == DANCE:
                for cycle in range(10):
                    for raw_index, raw in enumerate(map_matrix):
                        try:
                            xcol_index = raw.index(PLAYER_X)
                            xraw_index = raw_index
                        except ValueError:
                            pass

                        try:
                            ycol_index = raw.index(PLAYER_Y)
                            yraw_index = raw_index
                        except ValueError:
                            pass

                    if actions[PLAYER_X] == DANCE:
                        map_matrix[xraw_index][xcol_index] = PLAYER_X.lower() if cycle % 2 else PLAYER_X.upper()
                    if actions[PLAYER_Y] == DANCE:
                        map_matrix[yraw_index][ycol_index] = PLAYER_Y.lower() if cycle % 2 else PLAYER_Y.upper()

                    self.draw_matrix(map_matrix)
                    time.sleep(0.5)
                    os.system('clear')

        self.draw_matrix(map_matrix)
        time.sleep(1 / self.fps)

    def game_over(self, score):
        pass


def generate_raw_map(raws, cols):
    matrix = [['.' for _ in range(cols)] for _ in range(raws)]
    matrix[int(raws/2)][int(cols/2)] = PLAYER_X
    matrix[int(raws/2)+1][int(cols/2)+1] = PLAYER_Y
    return matrix

if __name__ == '__main__':
    map_visualizer = MapVisualizer()

    example_map = generate_raw_map(map_visualizer.max_raws, map_visualizer.max_cols)
    map_visualizer.draw(example_map, None, None)

    example_map = generate_raw_map(map_visualizer.max_raws + 1, map_visualizer.max_cols)
    try:
        map_visualizer.draw(example_map, None, None)
    except ValueError as e:
        print(e)

    example_map = generate_raw_map(map_visualizer.max_raws, map_visualizer.max_cols + 1)
    try:
        map_visualizer.draw(example_map, None, None)
    except ValueError as e:
        print(e)

    example_map = generate_raw_map(10, 10)
    map_visualizer.draw(example_map, None, None)

    map_visualizer.draw(example_map, {PLAYER_X: DANCE, PLAYER_Y: DANCE}, None)
