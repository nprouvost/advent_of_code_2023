
def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


def obtain_numbers_in_cards(list_of_cards):
    cards_dict = {}
    for card in list_of_cards:
        card_name, winning_and_obtained_numbers_str = card.split(':')
        _, card_Id = card_name.split()
        winning_numbers_str, obtained_numbers_str = winning_and_obtained_numbers_str.split('|')
        winning_numbers = set()
        for winning_number in winning_numbers_str.split():
            winning_numbers.add(int(winning_number))
        obtained_numbers = set()
        for obtained_number in obtained_numbers_str.split():
            obtained_numbers.add(int(obtained_number))
        cards_dict[card_Id] = [winning_numbers, obtained_numbers]
    return cards_dict


def count_matching_numbers_in_cards(cards_dict):
    matching_numbers_in_cards = {}
    for key in cards_dict.keys():
        matching_numbers_in_cards[key] = sum(x in cards_dict[key][0] for x in cards_dict[key][1])
    return matching_numbers_in_cards


def calculate_value_cards(matching_numbers_in_cards):
    cards_value = {}
    for key in matching_numbers_in_cards.keys():
        if matching_numbers_in_cards[key] == 0:
            cards_value[key] = 0
        else:
            cards_value[key] = 2**(matching_numbers_in_cards[key]-1)
    return cards_value


def create_lookup_table_number_of_scratchcards(matching_numbers_in_cards):
    # to redo with recursion -> reach recursion limit?
    lookup_table_number_scratchcards = {}
    for key in matching_numbers_in_cards.keys():
        lookup_table_number_scratchcards[key] = 1

    def update_lookup_table(key):
        for i in range(1, matching_numbers_in_cards[key]+1):
            if int(key)+i > len(matching_numbers_in_cards.keys()):
                break
            lookup_table_number_scratchcards[str(int(key)+i)] += lookup_table_number_scratchcards[key]

    for key in lookup_table_number_scratchcards.keys():
        update_lookup_table(key)
    return lookup_table_number_scratchcards


if __name__ == '__main__':
    list_of_cards = read_file_to_list('../input_files/day_4.txt')
    cards_dict = obtain_numbers_in_cards(list_of_cards)
    matching_numbers_in_cards = count_matching_numbers_in_cards(cards_dict)
    all_cards_values = calculate_value_cards(matching_numbers_in_cards)
    print('in total, cards are worth', sum(all_cards_values.values()), 'points')
    lookup_table_number_scratchcards = create_lookup_table_number_of_scratchcards(matching_numbers_in_cards)
    print('number_of_scratchcards', sum(lookup_table_number_scratchcards.values()))
