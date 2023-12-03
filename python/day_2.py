import numpy as np


def read_file_to_list(path):
    with open(path, 'r') as f:
        return f.readlines()


def take_sets(list_of_games):
    games_dict = {}
    for game in list_of_games:
        game_name, sets_str = game.split(':')
        _, game_Id = game_name.split()
        sets = sets_str.split(';')
        games_dict[game_Id] = sets
    return games_dict


def change_set_to_list_of_int(set_):
    intlist = [0, 0, 0]
    all_balls = set_.split(',')
    all_balls_color_separated = [colored_balls.split() for colored_balls in all_balls]
    for nballs, color in all_balls_color_separated:
        match color:
            case 'red':
                intlist[0] = int(nballs)
            case 'green':
                intlist[1] = int(nballs)
            case 'blue':
                intlist[2] = int(nballs)
    return intlist


def create_sets_arrays(games_dict):
    games_dict_arrays = {}
    for key in games_dict.keys():
        sets = games_dict[key]
        sets_int = []
        for set_ in sets:
            intlist = change_set_to_list_of_int(set_)
            sets_int += [intlist]
        games_dict_arrays[key] = np.array(sets_int)
    return games_dict_arrays


def check_arrays(games_dict_arrays, condition):
    set_id = set()
    for key in games_dict_arrays.keys():
        for set_ in games_dict_arrays[key]:
            if np.any(set_ > condition):
                set_id.add(int(key))
    return set_id


def get_minimum_balls_number(games_dict_arrays):
    min_balls_dict = {}
    for key in games_dict_arrays.keys():
        min_balls_dict[key] = np.max(games_dict_arrays[key], axis=0)
    return min_balls_dict


def get_power_sets(min_balls_dict):
    sets_power_dict = {}
    for key in min_balls_dict.keys():
        sets_power_dict[key] = np.prod(min_balls_dict[key])
    return sets_power_dict


if __name__ == '__main__':
    games_str = read_file_to_list('../input_files/day_2.txt')
    games_dict = take_sets(games_str)
    games_dict_arrays = create_sets_arrays(games_dict)
    impossible_games_id = check_arrays(games_dict_arrays, np.array([12, 13, 14]))
    print('sum set Ids not possible', sum(impossible_games_id))
    print('sum set Ids possible', sum(range(1, 101))-sum(impossible_games_id))
    min_balls_dict = get_minimum_balls_number(games_dict_arrays)
    sets_power_dict = get_power_sets(min_balls_dict)
    print('sum sets power', sum(sets_power_dict.values()))
