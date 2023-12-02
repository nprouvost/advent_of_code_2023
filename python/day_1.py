import numpy as np
import re

name_to_int_dict = {"zero":"0", "one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8", "nine":"9"}
name_inv_to_int_dict={}
for key in name_to_int_dict.keys():
    name_inv_to_int_dict[key[::-1]] = name_to_int_dict[key]
name_to_int_dict.update(name_inv_to_int_dict)

def read_file_to_array(path):
    with open(path,"r") as f:
        return np.array(f.readlines())

def match_pattern(array, pattern_fix, pattern_to_reverse):
    pattern = "("+pattern_fix+"|"+pattern_to_reverse+")"
    value = np.array([name_to_int_dict.get((value:=re.search(pattern, string_).group()),value) for string_ in array])
    return value

def get_all_numbers(array, pattern_fix, pattern_to_reverse):
    first_value = match_pattern(array, pattern_fix, pattern_to_reverse)
    array_reversed = np.array([i[::-1] for i in array])
    pattern_reversed = pattern_to_reverse[::-1]
    last_value = match_pattern(array_reversed, pattern_fix, pattern_reversed)
    return np.char.add(first_value, last_value).astype("i8")
    
if __name__ == "__main__":
    str_array = read_file_to_array("../input_files/day_1.txt")
    values = get_all_numbers(str_array, "\d","zero|one|two|three|four|five|six|seven|eight|nine")
    print(np.sum(values))
