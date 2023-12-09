import numpy as np
from ast import literal_eval
import re


example_input = ['LLR',
                 '',
                 'AAA = (BBB, BBB)',
                 'BBB = (AAA, ZZZ)',
                 'ZZZ = (ZZZ, ZZZ)']


def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


def change_direction_to_value(direction):
    if direction == 'L':
        return 0
    else:
        return 1


def get_directions_and_nodes_dict(directions_file):
    directions_str = directions_file[0]
    directions_list = [change_direction_to_value(direction) for direction in directions_str]
    node_dict = {}
    for iline, line in enumerate(directions_file[2:]):
        key, tuple_ = line.split('=')
        key = key.strip()
        new_tuple = ''
        for i, char_ in enumerate(tuple_.strip()):
            if char_ in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if tuple_.strip()[i-1] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    char_ = '"' + char_
                elif tuple_.strip()[i+1] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    char_ = char_ + '"'
            new_tuple += char_
        array = np.array(literal_eval(new_tuple))
        node_dict[key] = array
    return directions_list, node_dict


def node_loop(node_dict, directions_list):
    node = 'VVA'
    step = 0
    node_list = ['XDZ', 'JVZ', 'DDZ', 'THZ', 'SRZ', 'ZZZ']
    while ((node not in node_list) or (step == 13301)):
        step_node = step % len(directions_list)
        node = node_dict[node][directions_list[step_node]]
        step += 1
    return step


def node_loop_numpyzed(node_dict, directions_list):
    node_begin_pattern = '[A-Z]{2}A'  # ['GNA' 'FCA' 'AAA' 'MXA' 'VVA' 'XHA']
    node_end_pattern = '[A-Z]{2}Z'  # ['XDZ', 'JVZ', 'DDZ', 'THZ', 'SRZ', 'ZZZ']
    # print(node_dict.keys())
    nodes_array = np.array([node for node in node_dict.keys() if re.match(node_begin_pattern, node)])
    # print(nodes_array)
    step = 0
    r = re.compile(node_end_pattern)
    vmatch = np.vectorize(lambda x: bool(r.match(x)))
    return 5
    while not np.all(vmatch(nodes_array)):
        step_node = step % len(directions_list)
        key_user = np.vectorize(lambda x: node_dict[x][directions_list[step_node]])
        nodes_array = key_user(nodes_array)
        step += 1
        if step % 10000 == 0:
            print(step)
    return step


def node_loop_each_pattern(node_dict, directions_list):
    node_begin_pattern = '[A-Z]{2}A'  # ['GNA' 'FCA' 'AAA' 'MXA' 'VVA' 'XHA']
    node_end_pattern = '[A-Z]{2}Z'  # ['XDZ', 'JVZ', 'DDZ', 'THZ', 'SRZ', 'ZZZ']
    # print(node_dict.keys())
    nodes_array = np.array([node for node in node_dict.keys() if re.match(node_begin_pattern, node)])
    end_nodes_array = np.array([node for node in node_dict.keys() if re.match(node_end_pattern, node)])
    # print(nodes_array)
    steps = []
    for node in nodes_array:
        step = 0
        new_node = node
        while node not in end_nodes_array:  # (node not in node_list) or (step == 13301)
            step_node = step % len(directions_list)
            node = node_dict[node][directions_list[step_node]]
            step += 1
        print(node, 'matches to', new_node)
        steps += [step]
    return steps


if __name__ == '__main__':
    directions_file = read_file_to_list('../input_files/day_8.txt')
    directions_list, node_dict = get_directions_and_nodes_dict(directions_file)  # example_input # directions_file
    # print(directions_list, node_dict)
    steps = node_loop(node_dict, directions_list)
    print('number of steps: ', steps)

    # part 2:
    # steps = node_loop_numpyzed(node_dict, directions_list) -> way too long

    # through short test phase after hypothesis: observation: the numbers *A and *Z patterns are matched one to one
    # and they repeat themselves every x loop, with x the number of steps for the first time
    # reaching the Z pattern. Hence, we are looking for the lcm of the steps for each pattern
    steps_list = node_loop_each_pattern(node_dict, directions_list)
    # 17263, 13301, 14999, 12169, 20093, 22357
    # result 10371555451871

    print('number of steps: ', np.lcm.reduce(steps_list))
