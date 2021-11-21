# Copyright and Performance rights by Guilherme Silveira
from itertools import permutations
from typing import List, Tuple
from tqdm import tqdm
import random

import numpy as np
import z3
from z3 import AtMost, Distinct, unsat, unknown, Z3Exception, Solver


def simulate(cuts: Tuple[int], deck: Tuple[int]):
    stacks = np.array([range(cuts[0]),
                       range(cuts[0], cuts[1]),
                       range(cuts[1], cuts[2]),
                       range(cuts[2], 52)], dtype="object")
    resulting_stack = np.concatenate(stacks[[*deck]])
    return resulting_stack


class Language:

    def values(self):
        return self._values

    def suits(self):
        return self._suits

    def retrieve_card_name(self, position):
        value = (position - 1) % 13
        suit = (position - 1) // 13
        return self.values()[value] + " of " + self.suits()[suit]

    def all_card_names(self):
        return list(map(self.retrieve_card_name, range(1, 53)))


class Portuguese(Language):
    def __init__(self):
        self._values = ["as", "dois", "tres", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez",
                        "valete", "dama", "reis"]
        self._suits = ["paus", "copas", "espadas", "ouros"]


class English(Language):
    def __init__(self):
        self._values = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                        "jack", "queen", "king"]
        self._suits = ["clubs", "hearts", "spades", "diamonds"]


def rules_all_cards_on_deck(all_vars: List[z3.Int]) -> z3.And:
    rules = [z3.And([card >= 0, card <= 51]) for card in all_vars]
    return z3.And(rules)


def card_length_for(card_name):
    return len(card_name.replace(" ", ""))


def spelling_rules(all_vars: List[z3.Int],
                   deck: List[int],
                   language: Language,
                   can_be_same) -> z3.Or:
    rules = []
    for card in range(1, 53):

        # if card == 27, it is the ace of spades
        name = language.retrieve_card_name(card)
        # ace of spades has length 11
        card_length = card_length_for(name)

        # if card = 27, the 26nd variable
        var = all_vars[card - 1]

        # ace of spades should be at position 12 in the deck (11 in python)
        # original_position = 0 means it should be at the first position of the starting deck
        finishing_position = card_length
        original_position = int(deck[finishing_position])
        rules.append(var == original_position)

        # print(card, name, card_length, var, finishing_position, original_position)

        # ace of spades should be at position 11 in the deck (10 in python)
        # original_position = 0 means it should be at the first position of the starting deck
        if can_be_same:
            finishing_position = card_length - 1
            original_position = int(deck[finishing_position])
            rules.append(var == original_position)

        # print(card, name, card_length, var, finishing_position, original_position, deck)

    return z3.Or(rules)


def freedom_of_spelling(all_vars: List[z3.Int],
                        cuts: Tuple[int],
                        sequence: Tuple[int],
                        language: Language,
                        can_be_same) -> z3.Or:
    deck = simulate(cuts, sequence)
    return spelling_rules(all_vars, deck, language, can_be_same)


def freedom_search(language: Language, space, generate_rules_only=False,
                   distinct=False,
                   can_be_same=True):
    rules = set()
    names = language.all_card_names()
    all_vars = list(map(z3.Int, names))

    print(names)
    print(all_vars)

    for cut1 in tqdm(space(1)):
        for cut2 in space(2, cut1):
            for cut3 in space(3, cut1, cut2):
                for sequence in permutations(range(4)):
                    cuts = (cut1, cut2, cut3)
                    rule = freedom_of_spelling(all_vars, cuts, sequence, language, can_be_same)
                    rules.add(rule)

    if distinct:
        rules.add(Distinct(all_vars))
    else:
        for position in range(0, 52):
            at_starting_point = [card == position for card in all_vars]
            rule = AtMost(*at_starting_point, 1)
            rules.add(rule)

    rules.add(rules_all_cards_on_deck(all_vars))

    if generate_rules_only:
        return

    print(len(rules))

    s = Solver()
    s.set('smt.arith.random_initial_value', True)

    # random_seed (unsigned int) random seed (default: 0)
    s.set('random_seed', random.randint(0, 2 ** 8))

    # seed (unsigned int) random seed. (default: 0)
    s.set('seed', random.randint(0, 2 ** 8))

    s.add(rules)
    r = s.check()
    if r == unsat:
        print("no solution")
    elif r == unknown:
        print("failed to solve")
        try:
            print(s.reason_unknown())
            print(s.model())
        except Z3Exception:
            return
    else:
        print(s.model())
