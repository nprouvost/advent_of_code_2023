import numpy as np


def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


example_input = ['0 3 6 9 12 15',
                 '1 3 6 10 15 21',
                 '10 13 16 21 30 45']


def get_history_lists(history_values):
    return [np.array([int(value) for value in line.split()]) for line in history_values]


def calculate_series(history_values_lists):
    series = []
    for history in history_values_lists:
        history_part = history
        all_history_parts = []
        all_history_parts += [history]
        while not np.all(history_part == 0):
            history_part = np.array([history_part[i]-history_part[i-1] for i, value in enumerate(history_part) if i !=0])
            all_history_parts += [history_part]
        series += [all_history_parts]
    return series


def get_next_value(list_of_lists):
    next_value = 0
    # invert to get the difference steps from the bottom
    for list_ in list_of_lists[::-1]:
        next_value = next_value + list_[-1]
    return next_value


def get_previous_value(list_of_lists):
    previous_value = 0
    for list_ in list_of_lists[::-1]:
        previous_value = list_[0] - previous_value
    return previous_value


if __name__ == '__main__':
    history_values = read_file_to_list('../input_files/day_9.txt')
    history_values_lists = get_history_lists(history_values)  # example_input # history_values
    # calculate all the difference lists for all histories
    series = calculate_series(history_values_lists)
    all_next_values = [get_next_value(list_of_lists) for list_of_lists in series]
    # print("all_next_values", all_next_values)
    print("sum is", sum(all_next_values))

    all_previous_values = [get_previous_value(list_of_lists) for list_of_lists in series]
    # print("all_previous_values", all_previous_values)
    print("sum is", sum(all_previous_values))
