import choppycamp.constants as constants


class BaseBot(object):
    def __init__(self, name, map_, enemy):
        self.name = name
        self.map = map_
        self.enemy = enemy

    def act(self, map_):
        return constants.DANCE
