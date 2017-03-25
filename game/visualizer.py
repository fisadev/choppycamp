import shutil
import os


class MapVisualizer():
    def __init__(self):
        self.max_cols, self.max_raws = shutil.get_terminal_size()
    
    def check_map_size(self, map_matrix):
        if len(map_matrix) > self.max_raws:
            raise ValueError("Raw len {} > {}".format(len(map_matrix), self.max_raws))

        for raw in map_matrix:
            if len(raw) > self.max_cols:
                raise ValueError("Col len {} > {}".format(len(raw), self.max_cols))

    def draw(self, map_matrix):
        self.check_map_size(map_matrix)

        os.system('clear')
        for raw in map_matrix:
            line = ''
            for tile in raw:
                line = line + tile 
            print(line)

def generate_raw_map(raws, cols):
    return [['#'] * cols] * raws

if __name__ == '__main__':
    map_visualizer = MapVisualizer()

    example_map = generate_raw_map(map_visualizer.max_raws, map_visualizer.max_cols)
    map_visualizer.draw(example_map)

    example_map = generate_raw_map(map_visualizer.max_raws + 1, map_visualizer.max_cols)
    try:
        map_visualizer.draw(example_map)
    except ValueError as e:
        print(e)

    example_map = generate_raw_map(map_visualizer.max_raws, map_visualizer.max_cols + 1)
    try:
        map_visualizer.draw(example_map)
    except ValueError as e:
        print(e)

    example_map = generate_raw_map(10, 10)
    map_visualizer.draw(example_map)

