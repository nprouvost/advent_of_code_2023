import numpy as np


def read_file_to_list(path):
    with open(path, 'r') as f:
        lines_without_endlines = [line[:-1] for line in f.readlines()]
        return lines_without_endlines


example_input = ['32T3K 765',
                 'T55J5 684',
                 'KK677 28',
                 'KTJJT 220',
                 'QQQJA 483',
                 ]

example_input2 = ['32TQK 765',
                  'T5555 684',
                  'KKK77 28',
                  'KTJJT 220',
                  'QQQQQ 483',
                  ]

example_input3 = ['7T849 684',
                  'TQK56 483',
                  '5J984 765',
                  '963J5 220',
                  'A7T4J 28',
                  ]


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


def get_power_hand_and_values_list(hand_list):
    power_hand = []
    values_hand_list = []
    for hand in hand_list:
        values_hand = get_values_hand(hand)
        values_hand_list += [values_hand]
        if np.any(np.array(values_hand) == 5):
            power_hand += [6]
            continue
        elif np.any(np.array(values_hand) == 4):
            power_hand += [5]
            continue
        elif np.any(np.array(values_hand) == 3):
            if np.any(np.array(values_hand) == 2):
                power_hand += [4]
                continue
            power_hand += [3]
            continue
        elif np.any(np.array(values_hand) == 2):
            if np.sum(np.array(values_hand) == 2) == 2:
                power_hand += [2]
                continue
            power_hand += [1]
            continue
        else:
            power_hand += [0]
    return power_hand, values_hand_list


def get_power_best_cards(number_cards_per_value):
    power_best_cards = 0
    power_card_value = 0
    for number_cards in list(number_cards_per_value):
        power_card_value = 5 * power_card_value + 1
        power_best_cards += power_card_value * number_cards
        # print(power_card_value, power_best_cards)
    max_power_card_value = 5 * power_card_value
    # print(max_power_card_value)
    return power_best_cards, max_power_card_value


def convert_total_power_hands(power_hand, values_hand_list):
    total_power_hands = []
    for i, power in enumerate(power_hand):
        power_best_cards, max_power_card_value = get_power_best_cards(values_hand_list[i])
        total_power_hands += [power * (max_power_card_value + 1) + power_best_cards]
    return total_power_hands


if __name__ == '__main__':
    hand_and_bid = read_file_to_list('../input_files/day_7_marcel.txt')
    hand_and_bid_dict = make_input_to_dict(hand_and_bid)  # example_input # hand_and_bid
    # get the number of cards of each type and a power value according to the value of the card combination
    power_hand, values_hand_list = get_power_hand_and_values_list(hand_and_bid_dict['hand'])
    # convert value card combination and value best cards to a total hand power value
    total_power_hands = convert_total_power_hands(power_hand, values_hand_list)

    ranks = (np.argsort(np.argsort(total_power_hands)) + 1)
    print('total_winnings', np.sum(ranks*np.array(hand_and_bid_dict['bid'])))
