"""
Head        -> Upper
Tail        -> Lower
Bunting     -> B
Cardinal    -> C
Finch       -> F
Bluebird    -> L
"""

from collections import Counter

top_left = 0
top_center = 1
top_right = 2
center_left = 3
center = 4
center_right = 5
bottom_left = 6
bottom_center = 7
bottom_right = 8

top = 0
right = 1
bottom = 2
left = 3

MISMATCH = {ord("b"): 3, ord("F"): 3}

CARDS = [
    list(map(ord, c))
    for c in ["CBlL", "FLbf", "FbLc", "CFbl", "fcLB", "lBFC", "blfc", "lFcb", "FbLC"]
]

# fmt: off
EXTERIOR = [
    (top_left,      left),
    (top_left,      top),
    (top_center,    top),
    (top_right,     top),
    (top_right,     right),
    (center_left,   left),
    (center_right,  right),
    (bottom_left,   left),
    (bottom_left,   bottom),
    (bottom_center, bottom),
    (bottom_right,  bottom),
    (bottom_right,  right)]
# fmt: on

# fmt: off
COMPARISONS = [
    (top_left,      right,  top_center,     left),
    (top_left,      bottom, center_left,    top),
    (top_center,    right,  top_right,      left),
    (top_center,    bottom, center,         top),
    (top_right,     bottom, center_right,   top),
    (center_left,   right,  center,         left),
    (center_left,   bottom, bottom_left,    top),
    (center,        right,  center_right,   left),
    (center,        bottom, bottom_center,  top),
    (center_right,  bottom, bottom_right,   top),
    (bottom_left,   right,  bottom_center,  left),
    (bottom_center, right,  bottom_right,   left),
]
# fmt: on


def rotate(s: list, n: int) -> list:
    return s[n:] + s[:n]


def is_valid(cards: list[list[int]]) -> bool:
    exterior = Counter([cards[c][o] for c, o in EXTERIOR])
    for k, v in MISMATCH.items():
        if exterior[k] != v:
            return False

    for c1, o1, c2, o2 in COMPARISONS:
        if abs(cards[c1][o1] - cards[c2][o2]) != 32:
            return False

    return True


if __name__ == "__main__":
    from math import factorial

    # print("Face Counts:", sorted(Counter("".join(CARDS)).items()))
    print("Total Combinations:", factorial(9) * 9**4)

    print(is_valid(CARDS))
