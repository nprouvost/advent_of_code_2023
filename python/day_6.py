import numpy as np


def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


example_input = ['Time:      7  15   30',
                 'Distance:  9  40  200']


def make_int_dict(times_and_distances):
    int_dict = {}
    for line in times_and_distances:
        key, values = line.split(':')
        values_list = [int(value) for value in values.split()]
        int_dict[key] = values_list
    return int_dict


def calculate_distance_traveled(time, time_on_button):
    return (time-time_on_button)*time_on_button


def find_max_distances(time):
    if time % 2 == 0:
        max_distance = (time/2)**2
        n_value = 1
    if time % 2 == 1:
        max_distance = (time**2-1)/4  # = (time+1)/2*(time-1)/2
        n_value = 2
    return max_distance, n_value


def find_number_possible_distances(times, distances):
    number_possible_distances = []
    for i, time in enumerate(times):
        max_distance, nvalue_original = find_max_distances(time)
        distance = max_distance
        nvalue = nvalue_original
        step = 1
        if distance < distances[i]:
            number_possible_distances += [0]
            continue
        while distance > distances[i]:
            # time even: (n+m)(n-m)=n**2-m**2  with n = time/2, m=step
            # time odd: ((n+1)/2 +m)((n-1)/2-m) = (n +1+2m)(n-1-2m)/4 = (n**2-1-4m-4m**2)/4 with n = time, m=step
            if nvalue_original == 1:
                distance = max_distance - step**2
            if nvalue_original == 2:
                distance = max_distance - step**2 - step
            if distance > distances[i]:
                nvalue += 2
                step += 1
        number_possible_distances += [nvalue]

    return number_possible_distances


def make_int_dict2(times_and_distances):
    int_dict = {}
    for line in times_and_distances:
        key, values = line.split(':')
        values_list = [value for value in values.split()]
        value_list = [int(''.join(values_list))]
        int_dict[key] = value_list
    return int_dict


if __name__ == '__main__':
    times_and_distances = read_file_to_list('../input_files/day_6.txt')
    times_and_distances_dict = make_int_dict(times_and_distances)  # example_input # times_and_distances
    number_possible_distances = find_number_possible_distances(list(times_and_distances_dict.values())[0],
                                                               list(times_and_distances_dict.values())[1])
    print(number_possible_distances, np.prod(np.array(number_possible_distances)))

    # part 2
    times_and_distances_dict = make_int_dict2(times_and_distances)  # example_input # times_and_distances
    number_possible_distances = find_number_possible_distances(list(times_and_distances_dict.values())[0],
                                                               list(times_and_distances_dict.values())[1])
    print(number_possible_distances)
