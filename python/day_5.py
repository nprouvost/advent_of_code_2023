import numpy as np
import time


def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


def get_seeds_and_maps_dict(almanac_list_str):
    seeds_str = almanac_list_str[0].split(":")[1]
    seeds_list_str = seeds_str.split()
    seeds = [int(seed) for seed in seeds_list_str]
    all_maps_dict = {}
    for iline, line in enumerate(almanac_list_str[2:]):
        if len(line.split(":"))>1:
            key = line.split(":")[0]
            new_map = []
        elif line == "":
            all_maps_dict[key] = new_map
        else:
            new_map += [[int(number) for number in line.split()]]
        if iline == len(almanac_list_str[2:])-1:
            all_maps_dict[key] = new_map
    return seeds, all_maps_dict


def find_index(index, list_of_ranges):
    for list_ in list_of_ranges:
        # from IPython import embed; embed()
        if index in range(list_[1], list_[1]+list_[2]):
            position = index-list_[1]
            return range(list_[0], list_[0]+list_[2])[position]
    return index


def get_last_indices(seeds, all_maps_dict):
    last_indices = set()
    for iseed, seed in enumerate(seeds):
        for key in all_maps_dict.keys():
            seed = find_index(seed, all_maps_dict[key])
        last_indices.add(seed)
    return last_indices


def get_seeds_ranges(seeds):
    ranges_of_seeds = []
    for iseed, seed in enumerate(seeds):
        if iseed % 2 == 0:
            ranges_of_seeds += [[seed, seeds[iseed+1]]]
    return ranges_of_seeds


def calculate_new_ranges(seed_range_, sorted_almanach_ranges):
    new_ranges = []
    for i, sorted_almanach_range in enumerate(sorted_almanach_ranges):
        if seed_range_[0] >= (sorted_almanach_range[1] + sorted_almanach_range[2]):
            continue
        # from IPython import embed; embed()
        start_value = sorted_almanach_range[0] + seed_range_[0] - sorted_almanach_range[1]
        if seed_range_[0] + seed_range_[1] > (sorted_almanach_range[1] + sorted_almanach_range[2]):
            if i == len(sorted_almanach_ranges)-1:
                print("error?, value seed bigger than 10B")
            else:
                length = sorted_almanach_range[2] - (seed_range_[0]-sorted_almanach_range[1])
                new_ranges += [[start_value, length]]
                seed_range_[0] = seed_range_[0] + length
                seed_range_[1] = seed_range_[1] - length
        else:
            new_ranges += [[start_value, seed_range_[1]]]
            break
    return new_ranges


def get_last_ranges(seed_ranges, no_hole_sorted_all_maps_dict):
    last_ranges = []
    for seed_range_ in seed_ranges:
        seed_ranges_ = [seed_range_]
        for key in no_hole_sorted_all_maps_dict.keys():
            new_ranges = []
            for range_ in seed_ranges_:
                new_ranges += calculate_new_ranges(range_, no_hole_sorted_all_maps_dict[key])
            seed_ranges_ = new_ranges
        last_ranges += new_ranges
    return last_ranges


def sort_all_maps_dict(all_maps_dict):
    sorted_all_maps_dict = {}
    for key in all_maps_dict.keys():
        sorted_list = sorted(all_maps_dict[key], key=lambda x:x[1])
        sorted_all_maps_dict[key] = sorted_list
    return sorted_all_maps_dict


def add_missing_unity_ranges(sorted_all_maps_dict):
    no_hole_sorted_all_maps_dict = {}
    for key in sorted_all_maps_dict.keys():
        no_hole_list = []
        for ilist,list_ in enumerate(sorted_all_maps_dict[key]):
            if ilist==0:
                if list_[1]!=0:
                    no_hole_list.append([0,0,list_[1]])
                no_hole_list.append(list_)
                continue
            if list_[1]>(sorted_all_maps_dict[key][ilist-1][1]+sorted_all_maps_dict[key][ilist-1][2]):
                start_value = sorted_all_maps_dict[key][ilist-1][1]+sorted_all_maps_dict[key][ilist-1][2]
                no_hole_list.append([start_value,start_value,list_[1]-start_value])
                no_hole_list.append(list_)
            if list_[1]==(sorted_all_maps_dict[key][ilist-1][1]+sorted_all_maps_dict[key][ilist-1][2]):
                no_hole_list.append(list_)
            if ilist==len(sorted_all_maps_dict[key])-1:
                no_hole_list.append([list_[1]+list_[2],list_[1]+list_[2],10000000000-list_[1]-list_[2]])
        no_hole_sorted_all_maps_dict[key] = no_hole_list
    return no_hole_sorted_all_maps_dict


if __name__ == '__main__':
    time_begin=time.time()
    almanac_list_str = read_file_to_list('../input_files/day_5.txt')
    seeds, all_maps_dict = get_seeds_and_maps_dict(almanac_list_str)
    last_indices = get_last_indices(seeds, all_maps_dict)
    print("last_indices", last_indices)
    print("min", min(last_indices))

    # part 2
    seed_ranges = get_seeds_ranges(seeds)
    sorted_all_maps_dict = sort_all_maps_dict(all_maps_dict)
    no_hole_sorted_all_maps_dict = add_missing_unity_ranges(sorted_all_maps_dict)
    last_ranges = get_last_ranges(seed_ranges, no_hole_sorted_all_maps_dict)
    print("last_ranges", last_ranges)
    print("min", np.min(np.array(last_ranges)[:, 0]))
    time_end=time.time()
    print("time needed", time_end-time_begin)
