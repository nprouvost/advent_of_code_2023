import re
import numpy as np

def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


def check_adjacency(engine_status, index_line, indices, regex_exp):
    adjacency = False
    # contains for each gear the index of the list and the gear position, 2D if there are several
    # gears for one number (doesn't seem to happen, but done anyway)
    matches = []
    # check up
    if index_line != 0:
        # diagonal left
        if indices[0] != 0:
            if re.match(regex_exp, engine_status[index_line-1][indices[0]-1]):
                matches += [[index_line-1, indices[0]-1]]
                adjacency = True
        # diagonal right
        if indices[-1] != len(engine_status[index_line]):
            if re.match(regex_exp, engine_status[index_line-1][indices[-1]]):
                matches += [[index_line-1, indices[-1]]]
                adjacency = True
        # straight up
        if (match := list(re.finditer(regex_exp, engine_status[index_line-1][indices[0]:indices[-1]]))):
            matches += [[index_line-1, indices[0]+match_.span()[0]] for match_ in match]
            adjacency = True
    # check down
    if index_line != len(engine_status)-1:
        # diagonal left
        if indices[0] != 0:
            if re.match(regex_exp, engine_status[index_line+1][indices[0]-1]):
                matches += [[index_line+1, indices[0]-1]]
                adjacency = True
        # diagonal right
        if indices[-1] != len(engine_status[index_line]):
            if re.match(regex_exp, engine_status[index_line+1][indices[-1]]):
                matches += [[index_line+1, indices[-1]]]
                adjacency = True
        # straight down
        if (match := list(re.finditer(regex_exp, engine_status[index_line+1][indices[0]:indices[-1]]))):
            matches += [[index_line+1, indices[0]+match_.span()[0]] for match_ in match]
            adjacency = True
    # check left
    if indices[0] != 0:
        if (match := re.match(regex_exp, engine_status[index_line][indices[0]-1])):
            matches += [[index_line, indices[0]-1]]
            adjacency = True
    # check right
    if indices[-1] != len(engine_status[index_line]):
        if (match := re.match(regex_exp, engine_status[index_line][indices[-1]])):
            matches += [[index_line, indices[-1]]]
            adjacency = True
    return adjacency, matches


def get_numbers_with_adjacency(engine_status, numbers_matched):
    numbers_with_adjacency_list = []
    for iline, line in enumerate(numbers_matched):
        for match in line:
            existence, _ = check_adjacency(engine_status,
                                           iline,
                                           match.span(),
                                           regex_exp='[^0-9a-zA-Z\.]')
            if existence:
                numbers_with_adjacency_list += [int(match.group())]
    return numbers_with_adjacency_list


def get_gears_for_numbers(engine_status, numbers_matched):
    numbers_and_gears = {'numbers': [], 'gears': []}
    for iline, line in enumerate(numbers_matched):
        for match in line:
            existence, matching_results = check_adjacency(engine_status,
                                                          iline,
                                                          match.span(),
                                                          regex_exp='\*')
            if existence:
                numbers_and_gears['numbers'] += [int(match.group())]
                numbers_and_gears['gears'] += [matching_results]
    # as there is no number with several gears, change to array for easier masking later
    # throws an error if one number has several gears
    numbers_and_gears['gears'] = np.squeeze(np.array(numbers_and_gears['gears']), axis=1)
    numbers_and_gears['numbers'] = np.array(numbers_and_gears['numbers'])
    return numbers_and_gears


def get_acceptable_numbers_and_gears(numbers_and_gears):
    true_numbers_and_gears = {'number_pairs': [], 'gears': []}

    for inumbers, numbers in enumerate(numbers_and_gears['numbers']):
        mask = np.ones(len(numbers_and_gears['gears']), dtype=bool)
        mask[inumbers] = 0
        line_mask = numbers_and_gears['gears'][inumbers][0] == numbers_and_gears['gears'][mask][:, 0]
        index_mask = numbers_and_gears['gears'][inumbers][1] == numbers_and_gears['gears'][mask][:, 1]
        if np.any(line_mask & index_mask):
            # since two numbers correspond to one gear, avoid duplication in resulting array
            # (or divide by two result at the end)
            # This assume no gear has two pairs of pairs connecting to it...
            if tuple(numbers_and_gears['gears'][inumbers]) in true_numbers_and_gears['gears']:
                continue
            true_numbers_and_gears['gears'] += [tuple(numbers_and_gears['gears'][inumbers])]
            second_number = numbers_and_gears['numbers'][mask][line_mask & index_mask][0]
            true_numbers_and_gears['number_pairs'] += [np.array([numbers, second_number])]

    return true_numbers_and_gears


def get_gear_ratios(number_pairs):
    return [np.prod(number_pair) for number_pair in number_pairs]


if __name__ == '__main__':
    engine_status = read_file_to_list('../input_files/day_3.txt')
    numbers_matched = [list(re.finditer('\d+', line)) for line in engine_status]
    numbers_with_adjacency_list = get_numbers_with_adjacency(engine_status, numbers_matched)
    print('sum numbers with adjacency', sum(numbers_with_adjacency_list))
    numbers_and_gears = get_gears_for_numbers(engine_status, numbers_matched)
    true_numbers_and_gears = get_acceptable_numbers_and_gears(numbers_and_gears)
    gear_ratios = get_gear_ratios(true_numbers_and_gears['number_pairs'])
    print('sum gears', sum(gear_ratios))
