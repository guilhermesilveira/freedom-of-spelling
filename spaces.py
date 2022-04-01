def space_simplest(cut_number, cut1=None, cut2=None):
    if cut_number == 1:
        return range(7, 8)
    if cut_number == 2:
        return range(max(cut1, 12), 26)
    return range(max(cut2, 25), 39)


def space_optimized(cut_number, cut1=None, cut2=None):
    if cut_number == 1:
        return range(7, 21)
    if cut_number == 2:
        return range(max(cut1, 12), 26)
    return range(max(cut2, 25), 39)


def space_full(cut_number, cut1=None, cut2=None):
    if cut_number == 1:
        return range(2, 49)
    if cut_number == 2:
        return range(cut1, 50)
    return range(cut2, 51)
