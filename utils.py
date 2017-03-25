import importlib


def find_thing(map_, target):
    for r_number, columns in enumerate(map_):
        for c_number, thing in enumerate(columns):
            if thing == target:
                return r_number, c_number

    raise ValueError('Target not found: ' + target)


def position_in_map(map_, position):
    row, col = position
    return 0 <= row <= len(map_) and 0 <= col <= len(map_[0])


def get_bot(bot_name, id_, other_player, map_):
    module = importlib.import_module('bots.%s' % bot_name)
    bot = module.create_bot(map_, id_, other_player)
    return bot
