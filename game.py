import random

import click
from constants import (ACTION_DELTAS, ACTIONS, CHOPP, LAPTOP, PLAYER_X,
                       PLAYER_Y, PLAYERS, SCORE_THINGS, WALL, WON, TIE, LOST)
from game.map_generator import generate
from utils import find_thing, get_bot, position_in_map


class Game:
    def __init__(self, players, max_turns, map_, visualizer=None):
        self.map = map_
        self.players = players
        self.visualizer = visualizer
        self.max_turns = max_turns
        self.current_turn = None

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
        self.current_turn = 0
        while not self.game_finished():
            self.step()
            self.current_turn += 1
        self.notify_results()

    def game_finished(self):
        return not (self.current_turn < self.max_turns and self.prizes_in_board())

    def prizes_in_board(self):
        for row in self.map_:
            for value in row:
                if value in SCORE_THINGS:
                    return True
        return False

    def notify_results(self):
        x_score = self.scores[PLAYER_X]
        y_score = self.scores[PLAYER_Y]

        if x_score > y_score:
            x_result = WON
            y_result = LOST
        elif x_score < y_score:
            x_result = LOST
            y_result = WON
        else:
            x_result = TIE
            y_result = TIE

        self.players[PLAYER_X].game_over(x_result, self.map, self.scores)
        self.players[PLAYER_Y].game_over(y_result, self.map, self.scores)

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
@click.option('--max-turns', default=10, help='Max number of game turns.')
@click.option('--player-x', default='random', help='First player.')
@click.option('--player-y', default='random', help='Second player.')
@click.option('--visualizer', default=True, help='Use visualization or not.')
@click.option('--map', default=None, help='Map to play the game in.')
def main(player_x, player_y, max_turns, visualizer, map_):
    if not map_:
        map_ = generate()

    game = Game(
        players={
            PLAYER_X: get_bot(player_x, PLAYER_X, player_y, map_),
            PLAYER_Y: get_bot(player_y, PLAYER_Y, player_x, map_),
        },
        max_turns=max_turns,
        map_=map_,
        visualizer=None,
    )
    game.play()


if __name__ == '__main__':
    main()
