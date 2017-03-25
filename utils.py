def find_thing(map_, target):
    for r_number, columns in enumerate(map_):
        for c_number, thing in enumerate(columns):
            if thing == target:
                return r_number, c_number

    raise ValueError('Player not found: ' + player)


def position_in_map(map_, position):
    row, col = position
    return 0 <= row <= len(map_) and 0 <= col <= len(map_[0])
