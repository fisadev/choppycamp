import shutil
import time
import os
import string
import random

import sys
sys.path.append('../')

from constants import PLAYER_X, PLAYER_Y, DANCE, UP, REVERSE

class Window():
    def __init__(self):
        self.max_cols, self.max_raws = shutil.get_terminal_size()
        self.max_raws -= 2
        self.max_cols -= 2

        if self.max_cols < 50 or self.max_raws < 30:
            raise ValueError("Console too small {}x{}".format(self.max_raws, self.max_cols))

        self.cols_center = int(self.max_cols/2)
        self.raws_center = int(self.max_raws/2)

        self.clean_screen()

    def clean_screen(self):
        self.matrix = [[' ' for _ in range(self.max_cols)] for _ in range(self.max_raws)]

    def welcome_screen(self):
        printables = string.printable[:-5]
        for raw in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                self.matrix[raw][col] = printables[random.randint(0, len(printables)-1)]

        title = "Choppy by PyCamp 2017"

        for i in range(self.cols_center - int(len(title)/2) - 3, self.cols_center +
                int(len(title)/2) + 3):
            self.matrix[self.raws_center - 1][i] = ' '
            self.matrix[self.raws_center][i] = ('   ' + title + '   ')[i - self.cols_center - int(len(title)/2) - 3] 
            self.matrix[self.raws_center + 1][i] = ' '

    def init_score(self):
        self.matrix[0] = ['*' for _ in range(len(self.matrix[0]))]
        self.matrix[1] = ['*' for _ in range(len(self.matrix[0]))]
        self.matrix[3] = ['*' for _ in range(len(self.matrix[0]))]
        self.matrix[4] = ['*' for _ in range(len(self.matrix[0]))]

        self.matrix[2][0] = '*'
        self.matrix[2][-1] = '*'
        player1_ini = self.cols_center - int(self.cols_center/2)
        player1_string = 'Player 1: 0'
        self.player1_score_index = player1_ini + len(player1_string) - 1
        player2_ini = self.cols_center + int(self.cols_center/2)
        player2_string = 'Player 2: 0'
        self.player2_score_index = player2_ini + len(player2_string) - 1

        for col in range(player1_ini, player1_ini + len(player1_string)):
            self.matrix[2][col] = player1_string[col - player1_ini]
        for col in range(player2_ini, player2_ini + len(player2_string)):
            self.matrix[2][col] = player2_string[col - player2_ini]

    def update_score(self, score):
        self.matrix[2][self.player1_score_index] = str(score[PLAYER_X])
        self.matrix[2][self.player2_score_index] = str(score[PLAYER_Y])

    def update_map(self, map_matrix):
        map_raw_ini = self.raws_center - int(len(map_matrix)/2)
        map_col_ini = self.cols_center - int(len(map_matrix[0])/2)
        for raw in range(map_raw_ini, map_raw_ini + len(map_matrix)):
            for col in range(map_col_ini, map_col_ini + len(map_matrix[0])):
                self.matrix[raw][col] = map_matrix[raw - map_raw_ini][col - map_col_ini]

    def draw_matrix(self):
        for raw in self.matrix:
            line = ''
            for tile in raw:
                line += tile 
            print(line)

    def update(self):
        os.system('clear')
        self.draw_matrix()


class MapVisualizer():
    def __init__(self, welcome_screen=False, fps=3, dance_frames=4):
        self.fps = fps
        self.dance_frames = dance_frames
        self.window = Window()
        if welcome_screen:
            self.window.welcome_screen()
            self.window.update()
            time.sleep(5)
        self.window.clean_screen()
        self.window.init_score()
        self.window.update()

        self.map_max_raws = self.window.max_raws
        self.map_max_cols = self.window.max_cols
    
    def check_map_size(self, map_matrix):
        if len(map_matrix) > self.map_max_raws:
            raise ValueError("Raw len {} > {}".format(len(map_matrix), self.map_max_raws))

        for raw in map_matrix:
            if len(raw) > self.map_max_cols:
                raise ValueError("Col len {} > {}".format(len(raw), self.map_max_cols))


    def draw(self, map_matrix, actions, score):
        self.check_map_size(map_matrix)

        if score is not None:
            self.window.update_score(score)

        if actions is not None:
            if actions[PLAYER_X] == DANCE or actions[PLAYER_Y] == DANCE:
                for cycle in range(self.dance_frames):
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
                        map_matrix[xraw_index][xcol_index] = PLAYER_X if cycle % 2 else '{0}{1}'.format(REVERSE, PLAYER_X)
                    if actions[PLAYER_Y] == DANCE:
                        map_matrix[yraw_index][ycol_index] = PLAYER_Y if cycle % 2 else '{0}{1}'.format(REVERSE, PLAYER_Y)

                    self.window.update_map(map_matrix)
                    self.window.update()
                    time.sleep(1 / self.fps)

        self.window.update_map(map_matrix)
        self.window.update()
        time.sleep(1 / self.fps)


from game import map_generator
if __name__ == '__main__':
    map_visualizer = MapVisualizer()
    example_map = map_generator.generate(30, 30, 0.01, 0.01, 0.05)

    map_visualizer.draw(example_map, None, {PLAYER_X: 60, PLAYER_Y: 1})
    time.sleep(5)
