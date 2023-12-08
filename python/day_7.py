import numpy as np
import operator


def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


def make_input_to_dict(hand_and_bid):
    hand_and_bid_dict = {}
    hand_list, bid_list = [], []
    for line in hand_and_bid:
        hand, bid = line.split()
        hand_list += [hand]
        bid_list += [int(bid)]
    hand_and_bid_dict['hand'] = hand_list
    hand_and_bid_dict['bid'] = bid_list
    return hand_and_bid_dict


def get_values_hand(hand):
    dictionary_values = {}
    for card in '23456789TJQKA':
        dictionary_values[card] = 0
    for card in hand:
        dictionary_values[card] += 1
    return list(dictionary_values.values())


def get_type_list(hand_list):
    type_hand = []
    for hand in hand_list:
        values_hand = get_values_hand(hand)
        if np.any(np.array(values_hand) == 5):
            type_hand += [6]
            continue
        elif np.any(np.array(values_hand) == 4):
            type_hand += [5]
            continue
        elif np.any(np.array(values_hand) == 3):
            if np.any(np.array(values_hand) == 2):
                type_hand += [4]
                continue
            type_hand += [3]
            continue
        elif np.any(np.array(values_hand) == 2):
            if np.sum(np.array(values_hand) == 2) == 2:
                type_hand += [2]
                continue
            type_hand += [1]
            continue
        else:
            type_hand += [0]
    return type_hand


def convert_cards_hand_with_joker(hand):
    values_hand = []
    for card_found in hand:
        value = 0
        for card in 'J23456789TQKA':
            if card == card_found:
                values_hand += [value]
            value += 1
    return values_hand


def get_type_list_with_joker(hand_list):
    type_hand = []
    for hand in hand_list:
        n_joker = 0
        if 'J' in hand:
            for card in hand:
                if card == 'J':
                    n_joker += 1
        values_hand = get_values_hand(hand)
        if np.any(np.array(values_hand) == 5):
            type_hand += [6]
            continue
        elif np.any(np.array(values_hand) == 4):
            if n_joker > 0:
                type_hand += [6]
                continue
            else:
                type_hand += [5]
                continue
        elif np.any(np.array(values_hand) == 3):
            if n_joker == 2:
                type_hand += [6]
                continue
            if np.any(np.array(values_hand) == 2):
                if n_joker == 3:
                    type_hand += [6]
                    continue
                else:
                    type_hand += [4]
                    continue
            if (n_joker == 3) or (n_joker == 1):
                type_hand += [5]
                continue
            type_hand += [3]
            continue
        elif np.any(np.array(values_hand) == 2):
            if np.sum(np.array(values_hand) == 2) == 2:
                if n_joker == 2:
                    type_hand += [5]
                    continue
                if n_joker == 1:
                    type_hand += [4]
                    continue
                type_hand += [2]
                continue
            if (n_joker == 2) or (n_joker == 1):
                type_hand += [3]
                continue
            type_hand += [1]
            continue
        else:
            if n_joker == 1:
                type_hand += [1]
                continue
            type_hand += [0]
    return type_hand


def convert_cards_hand(hand):
    values_hand = []
    for card_found in hand:
        value = 0
        for card in '23456789TJQKA':
            if card == card_found:
                values_hand += [value]
            value += 1
    return values_hand


if __name__ == '__main__':
    hand_and_bid = read_file_to_list('../input_files/day_7.txt')
    hand_and_bid_dict = make_input_to_dict(hand_and_bid)
    # get the type for each hand
    type_hands = get_type_list(hand_and_bid_dict['hand'])
    # associate a value to each card depending on strength and return it instead of card itself
    hands_list = [convert_cards_hand(hand) for hand in hand_and_bid_dict['hand']]
    # concatenate
    type_and_hands_conc = [[type_hands[i], *hands_list[i]] for i in range(len(type_hands))]
    # sort
    ordered_hands = sorted(enumerate(type_and_hands_conc),
                           key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4], x[1][5]))
    ordering = [index for index, hand in ordered_hands]
    print('total_winnings', np.sum(range(1, len(type_hands)+1)*np.array(hand_and_bid_dict['bid'])[ordering]))

    # part 2
    type_hands = get_type_list_with_joker(hand_and_bid_dict['hand'])
    hands_list = [convert_cards_hand_with_joker(hand) for hand in hand_and_bid_dict['hand']]
    type_and_hands_conc = [[type_hands[i], *hands_list[i]] for i in range(len(type_hands))]
    ordered_hands = sorted(enumerate(type_and_hands_conc),
                           key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3], x[1][4], x[1][5]))
    ordering = [index for index, hand in ordered_hands]

    print('total_winnings', np.sum(range(1, len(type_hands)+1)*np.array(hand_and_bid_dict['bid'])[ordering]))
