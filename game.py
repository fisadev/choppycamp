class Game:
    def __init__(self):
        pass

    def step(self):
        actions = self.get_actions_from_players()
        self.apply_actions(actions)
        if self.visualizer is not None:
            self.visualizer.draw(self.map, self.scores)

    def get_actions_from_players(self):
        actions = []
        for player in self.players:
            actions.append(player, player.act(self.map))
        return actions
