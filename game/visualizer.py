import shutil
import time
import os
import string
import random

import sys
sys.path.append('../')

from constants import PLAYER_X, PLAYER_Y, DANCE, UP, REVERSE

CENTER = 'center'
LEFT = 'left'
RIGHT = 'right'


class Box():
    def __init__(self, width, height, border='*', empty=' '):
        self.width = width
        self.height = height
        self.empty = empty
        self.border = border
        self.clean()

    def clean(self):
        self.matrix = [[self.empty for _ in range(self.width)] for _ in range(self.height)]
        self.matrix[0] = [self.border for _ in range(self.width)]
        self.matrix[-1] = [self.border for _ in range(self.width)]
        for row in range(self.height):
            self.matrix[row][0] = self.border
            self.matrix[row][-1] = self.border

    def random(self):
        printables = string.printable[:-5]
        for row in range(self.height):
            for col in range(self.width):
                self.matrix[row][col] = printables[random.randint(0, len(printables)-1)]

    def get_center(self):
        return int(self.width/2), int(self.height/2)

    def put_text(self, col, row, text, align=CENTER):
        text_len = len(text)

        if align == CENTER:
            col -= int(text_len/2)
        elif align == RIGHT:
            col -= text_len

        if col < 0:
            raise ValueError("Col out of range %r" % col)

        for index in range(text_len):
            self.matrix[row][col + index] = text[index]

    def put_box(self, col, row, box, align=CENTER):

        if align == CENTER:
            col -= int(box.width/2)
            row -= int(box.height/2)
        elif align == RIGHT:
            col -= box.width
            row -= box.height

        if col < 0:
            raise ValueError("Col out of range %r" % col)
        if row < 0:
            raise ValueError("Row out of range %r" % row)

        for col_index in range(box.width):
            for row_index in range(box.height):
                self.matrix[row + row_index][col + col_index] = box.matrix[row_index][col_index]


class DebugBox(Box):
    def __init__(self, width, height):
        super(DebugBox, self).__init__(width, height, ' ')

    def update(self, debug_lines):
        self.clean()
        for i, line in enumerate(debug_lines):
            self.put_text(0, i, line, align=LEFT)

class PlayerScoreBoard(Box):
    def __init__(self, width, height, player_name):
        super(PlayerScoreBoard, self).__init__(width, height, '%')
        self.player_name = player_name 
        self.update(0, 0, 0)

    def update(self, score, nerding, drunkness):
        self.clean()
        col, row = self.get_center()
        self.put_text(col, 3, self.player_name, align=CENTER)
        self.put_text(col, 5, 'Score: ' + str(score), align=CENTER)
        self.put_text(col, 6, 'Drunknes: ' + str(drunkness), align=CENTER)
        self.put_text(col, 7, 'Nerdnes: ' + str(nerding), align=CENTER)


class Window():
    def __init__(self):
        self.max_cols, self.max_rows = shutil.get_terminal_size()
        self.max_rows -= 2
        self.max_cols -= 2

        if self.max_cols < 50 or self.max_rows < 30:
            raise ValueError("Console too small {}x{}".format(self.max_rows, self.max_cols))

        self.frame = Box(self.max_cols, self.max_rows, border=' ')

    def clean_screen(self):
        self.frame.clean()
        self.update()

    def welcome_screen(self, title="Choppy by PyCamp 2017"):
        self.frame.random()
        text_box = Box(len(title) + 4, 5, border=' ')
        text_box.clean()
        col, row = text_box.get_center()
        text_box.put_text(col, row, title, align=CENTER)

        col, row = self.frame.get_center()
        self.frame.put_box(col, row, text_box)

        self.update()

    def game_over_screen(self, text, winer):
        self.frame.clean()
        text_box = Box(35, 7, border='$')
        text_box.clean()
        col, row = text_box.get_center()
        text_box.put_text(col, row - 1, text, align=CENTER)
        text_box.put_text(col, row + 1, 'THE WINER ' + winer, align=CENTER)

        col, row = self.frame.get_center()
        self.frame.put_box(col, row, text_box)

        self.update()

    def draw_frame(self):
        for row in self.frame.matrix:
            line = ''
            for tile in row:
                line += tile 
            print(line)

    def update(self):
        os.system('clear')
        self.draw_frame()


class MapVisualizer():
    def __init__(self, map_matrix, welcome_screen=True, fps=3, dance_frames=4):
        self.fps = fps
        self.dance_frames = dance_frames
        self.window = Window()
        if welcome_screen:
            self.window.welcome_screen()
            time.sleep(1.5)
        self.window.clean_screen()
        self.window.update()

        self.map = Box(len(map_matrix[0]), len(map_matrix), ' ')
        self.map.matrix = map_matrix

        score_width = 20
        score_height = 10

        total_width = 2 + score_width + 2 + self.map.width 
        if (score_height*2 > self.map.height):
            total_height = 4 + score_height*2
        else:
            total_height = 4 + self.map.height

        self.debugbox = DebugBox(total_width, total_height)

        self.playerX = PlayerScoreBoard(score_width, score_height, 'Player_X')
        self.playerY = PlayerScoreBoard(score_width, score_height, 'Player_Y')

        col, row = self.window.frame.get_center()
        self.sub_boxes = [{'col': 0, 'row': 0, 'box': self.debugbox},
                          {'col': col - int(total_width/2), 'row': row - int(total_height/2), 'box': self.playerX},
                          {'col': col - int(total_width/2), 'row': row, 'box': self.playerY},
                          {'col': col, 'row': row - int(total_height/2), 'box': self.map}]

    def update_game(self):
        for sub_box in self.sub_boxes:
            self.window.frame.put_box(sub_box['col'], sub_box['row'], sub_box['box'], align=LEFT)
        self.window.update()

    def game_over(self, scores):
        text = 'PLAYER_X: ' + str(scores[PLAYER_X]) + ' / '
        text += 'PLAYER_Y: ' + str(scores[PLAYER_Y])
        if scores[PLAYER_X] == scores[PLAYER_Y]:
            winer = 'Tide'
        elif scores[PLAYER_X] > scores[PLAYER_Y]:
            winer = 'PLAYER_X'
        else:
            winer = 'PLAYER_Y'

        self.window.game_over_screen(text, winer)
    
    def draw(self, map_matrix, actions, scores, nerding, drunkness, debug_lines=None):
        if debug_lines is not None:
            self.debugbox.update(debug_lines)

        if scores is not None:
            self.playerX.update(scores[PLAYER_X], nerding[PLAYER_X], drunkness[PLAYER_X])
            self.playerY.update(scores[PLAYER_Y], nerding[PLAYER_Y], drunkness[PLAYER_Y])

        if actions is not None:
            if actions[PLAYER_X] == DANCE or actions[PLAYER_Y] == DANCE:
                for cycle in range(self.dance_frames):
                    for row_index, row in enumerate(map_matrix):
                        try:
                            xcol_index = row.index(PLAYER_X)
                            xrow_index = row_index
                        except ValueError:
                            pass

                        try:
                            ycol_index = row.index(PLAYER_Y)
                            yrow_index = row_index
                        except ValueError:
                            pass

                    if actions[PLAYER_X] == DANCE:
                        map_matrix[xrow_index][xcol_index] = PLAYER_X if cycle % 2 else '{0}{1}'.format(REVERSE, PLAYER_X)
                    if actions[PLAYER_Y] == DANCE:
                        map_matrix[yrow_index][ycol_index] = PLAYER_Y if cycle % 2 else '{0}{1}'.format(REVERSE, PLAYER_Y)

                    self.map.matrix = map_matrix
                    self.update_game()
                    time.sleep(1 / self.fps)

        self.map.matrix = map_matrix
        self.update_game()
        time.sleep(1 / self.fps)


from game import map_generator
if __name__ == '__main__':
    example_map = map_generator.generate(40, 40, 0.01, 0.01, 0.05)
    map_visualizer = MapVisualizer(example_map, welcome_screen=True)
    map_visualizer.draw(example_map, None, {PLAYER_X: 60, PLAYER_Y: 1})

    for i in range(10):
        map_visualizer.draw(example_map, None, {PLAYER_X: i, PLAYER_Y: i*2})
        time.sleep(1)
