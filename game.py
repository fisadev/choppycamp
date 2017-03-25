import random

import click

from constants import PLAYERS, ACTIONS, ACTION_DELTAS, WALL, SCORE_THINGS
from utils import find_thing, position_in_map


class Game:
    def __init__(self, players, max_turns, map_, visualizer=None):
        self.map = map_
        self.players = players
        self.visualizer = visualizer
        self.max_turns = max_turns

        self.scores = {}

    def apply_actions(self, actions):
        random.shuffle(actions)

        for player_id, action in actions:
            player_r, player_c = find_thing(self.map_, player_id)
            delta_r, delta_c = ACTION_DELTAS[action]
            new_r, new_c = player_r + delta_r, player_c + delta_c

            if position_in_map(self.map_, (new_r, new_c)):
                target = self.map[new_r][new_c]

                if target in SCORE_THINGS:
                    self.scores[player_id] += SCORE_THINGS[target]
                    self.map[new_r][new_c] = player_id
                elif not target:
                    self.map[new_r][new_c] = player_id

    def play(self):
        pass

    def step(self):
        actions = self.get_actions_from_players()
        self.apply_actions(actions)
        if self.visualizer is not None:
            self.visualizer.draw(self.map, self.scores)

    def get_actions_from_players(self):
        actions = []
        for player_name, player in self.players.items():
            actions.append(player_name, player.act(self.map))
        return actions


@click.command()
def main():
    game = Game([])
    game.play()


if __name__ == '__main__':
    main()
