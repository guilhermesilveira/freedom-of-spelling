import numpy as np
from typing import Tuple


def simulate_deck(deck: Tuple[int], cuts: Tuple[int], sequence: Tuple[int]):
    stacks = np.array([deck[:cuts[0]],
                       deck[cuts[0]:cuts[1]],
                       deck[cuts[1]:cuts[2]],
                       deck[cuts[2]:]], dtype=object)

    return np.concatenate(stacks[[*sequence]])
