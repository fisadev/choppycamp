import random

from constants import (ACTION_DELTAS, LOST, PLAYER_X, PLAYER_Y, SCORE_THINGS, TIE, WON)
from utils import find_thing, position_in_map


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
        if self.visualizer is not None:
            self.visualizer.game_over(self.scores)

    def step(self):
        actions = self.get_actions_from_players()
        self.apply_actions(actions)
        if self.visualizer is not None:
            self.visualizer.draw(self.map, actions, self.scores)

    def get_actions_from_players(self):
        actions = []
        for player_name, player in self.players.items():
            actions.append(player_name, player.act(self.map))
        return actions