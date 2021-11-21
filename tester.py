from itertools import permutations

from freedom import card_length_for
from simulator import simulate_deck
from spaces import *


def has_at_least_one_match(stack, debug=False):
    for i in range(15 + 1):

        # card at position i counts i+1 cards
        # because i starts at 0
        # the 10th card is at i=9
        position = i + 1

        # "ace of spades" has length 11 therefore
        # expected_position = 11
        card_name = stack[i]
        name_length = card_length_for(card_name)
        expected_position = name_length

        if debug:
            print(f"{i} : {position} : {name_length} : {expected_position}/{expected_position+1} : {card_name}")

        # for ace_of_spades
        # both position==11 or position==12 would be ok
        if expected_position == position or expected_position + 1 == position:
            return True

    return False


def print_cards(deck):
    print("-------------------------------")
    for i, card in enumerate(deck):
        length = card_length_for(card)
        print(f"{i} : {i + 1} : {length} : {card}")
    print("-------------------------------")


class Tester:
    def __init__(self, rules):
        self._rules = rules

    def validate(self, space, stop_on_error=False):
        deck = []
        for i in range(52):
            deck.append(self._rules[i])
        yes = 0
        no = 0
        for cut1 in space(1):
            for cut2 in space(2, cut1):
                for cut3 in space(3, cut1, cut2):
                    for sequence in permutations(range(4)):
                        cuts = (cut1, cut2, cut3)
                        result = simulate_deck(deck, cuts, sequence)
                        has = has_at_least_one_match(result)
                        if has:
                            yes += 1
                            continue
                        no += 1
                        print(f"error with {cuts}, {sequence}")
                        if stop_on_error:
                            print_cards(result)
                            has_at_least_one_match(result, debug=True)
                            exit(0)
        if no != 0:
            print(f"yes = {yes} no = {no}")


def load_rules(filename: str, debug=False):
    rules = {}
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if "=" not in line:
                continue

            # removes the first and last character besides new line
            line = line.rstrip()[1:-1]

            # extracts the name and number
            name, number = line.split(" = ")
            rules[int(number)] = name

    if debug:
        print(len(rules), rules)
    return rules


def check(filename: str, stop_on_error=False, debug=False, space_creator=space_optimized):
    if debug:
        print(f"checking {filename}")
    rules = load_rules(filename, debug)
    Tester(rules).validate(space_creator, stop_on_error)


