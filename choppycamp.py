import click

from constants import PLAYER_X, PLAYER_Y, CHOPP, LAPTOP
from game.map_generator import generate, add_things_randomly
from game.core import Game
from utils import get_bot
from game.visualizer import MapVisualizer


@click.command()
@click.option('--max-turns', default=10, help='Max number of game turns.')
@click.option('--player-x', default='random_bot', help='First player.')
@click.option('--player-y', default='random_bot', help='Second player.')
@click.option('--map_file', default=None, help='Map to play the game in.')
@click.option('--map_width', default=35, help='Map width to be used in map generation.')
@click.option('--map_height', default=20, help='Map height to be used in map generation.')
@click.option('--fps', default=3, help='Frames per second.')
def main(player_x, player_y, max_turns, map_file, map_width, map_height, fps):
    if not map_file:
        map_ = generate(
            map_width, map_height,
            box_density=0.1,
            laptop_density=0.01,
            chopp_density=0.05,
        )

    add_things_randomly(
        map_,
        {
            PLAYER_X: 1,
            PLAYER_Y: 1,
        },
    )

    game = Game(
        players={
            PLAYER_X: get_bot(player_x, PLAYER_X, player_y, map_),
            PLAYER_Y: get_bot(player_y, PLAYER_Y, player_x, map_),
        },
        max_turns=max_turns,
        map_=map_,
        visualizer=MapVisualizer(fps=fps),
    )
    game.play()


if __name__ == '__main__':
    main()
