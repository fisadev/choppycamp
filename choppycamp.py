import click

from constants import PLAYER_X, PLAYER_Y, CHOPP, LAPTOP
from game.map_generator import build_map, add_things_randomly
from game.core import Game
from utils import get_bot
from game.visualizer import MapVisualizer


@click.command()
@click.option('--max-turns', default=10, help='Max number of game turns.')
@click.option('--player-x', default='random_bot', help='First player.')
@click.option('--player-y', default='random_bot', help='Second player.')
@click.option('--map-file', default=None, help='Map to play the game in.')
@click.option('--map-width', default=35, help='Map width to be used in map generation.')
@click.option('--map-height', default=20, help='Map height to be used in map generation.')
@click.option('--fps', default=3, help='Frames per second.')
@click.option('--box-density', default=0.1, help='Density of beers in the map.')
@click.option('--chopp-density', default=0.05, help='Density of chopps in the map.')
@click.option('--laptop-density', default=0.01, help='Density of laptops in the map.')
@click.option('--room-width', default=5, help='Map width to be used in room generation.')
@click.option('--room-height', default=5, help='Map height to be used in room generation.')
@click.option('--room-box-density', default=0.0, help='Density of beers in the room.')
@click.option('--room-chopp-density', default=0.05, help='Density of chopps in the room.')
@click.option('--room-laptop-density', default=0.71, help='Density of laptops in the room.')
@click.option('--rooms', default=1, help='Number of rooms.')
@click.option('--nerd-factor', default=1, help='How much does a laptop nerdifies players.')
@click.option('--drunk-factor', default=1, help='How much does chopp affect reflexes.')
def main(player_x, player_y, max_turns, map_file, map_width, map_height, fps,
         box_density, chopp_density, laptop_density, room_width, room_height,
         room_box_density, room_chopp_density, room_laptop_density, rooms,
         drunk_factor, nerd_factor):
    if not map_file:
        map_ = build_map(
            map_width, map_height,
            room_width, room_height,
            box_density=box_density,
            chopp_density=chopp_density,
            laptop_density=laptop_density,
            room_box_density=room_box_density,
            room_chopp_density=room_chopp_density,
            room_laptop_density=room_laptop_density,
            rooms=rooms
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
        visualizer=MapVisualizer(map_, fps=fps),
        drunk_factor=drunk_factor,
        nerd_factor=nerd_factor,
    )
    game.play()


if __name__ == '__main__':
    main()
