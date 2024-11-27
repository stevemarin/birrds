"""
Head        -> Upper
Tail        -> Lower
Bunting     -> B
Cardinal    -> C
Finch       -> F
Bluebird    -> L
"""

from itertools import permutations
from textwrap import dedent
from typing import Iterable


PARTS = {
    "b": 0b000,
    "B": 0b001,
    "c": 0b100,
    "C": 0b101,
    "f": 0b010,
    "F": 0b011,
    "l": 0b110,
    "L": 0b111,
}

INVERTED_PARTS = {v: k for k, v in PARTS.items()}

# fmt: off
CARDS = ["bcfl", "bFCl", "LFfb", 
         "cFlb", "BlCF", "LbFC",
         "cLbF", "lBCL", "fBLc"]
# fmt: on


class Card:
    __slots__ = ("top", "right", "bottom", "left")

    def __init__(self, b: str) -> None:
        for val, name in zip(b, self.__slots__):
            setattr(self, name, PARTS[val])

    def __repr__(self) -> str:
        return "".join(map(INVERTED_PARTS.__getitem__, [self.top, self.right, self.bottom, self.left]))

    def rotate(self) -> None:
        self.right, self.bottom, self.left, self.top = (self.top, self.right, self.bottom, self.left)


class Game:
    def __init__(self, cards: Iterable[Card]):
        self.cards = list(cards)

    def __repr__(self) -> str:
        return dedent(f"""
             {INVERTED_PARTS[self.cards[0].top]}   {INVERTED_PARTS[self.cards[1].top]}   {INVERTED_PARTS[self.cards[2].top]} 
            {INVERTED_PARTS[self.cards[0].left]} {INVERTED_PARTS[self.cards[0].right]} {INVERTED_PARTS[self.cards[1].left]} {INVERTED_PARTS[self.cards[1].right]} {INVERTED_PARTS[self.cards[2].left]} {INVERTED_PARTS[self.cards[2].right]}
             {INVERTED_PARTS[self.cards[0].bottom]}   {INVERTED_PARTS[self.cards[1].bottom]}   {INVERTED_PARTS[self.cards[2].bottom]} 
             {INVERTED_PARTS[self.cards[3].top]}   {INVERTED_PARTS[self.cards[4].top]}   {INVERTED_PARTS[self.cards[5].top]} 
            {INVERTED_PARTS[self.cards[3].left]} {INVERTED_PARTS[self.cards[3].right]} {INVERTED_PARTS[self.cards[4].left]} {INVERTED_PARTS[self.cards[4].right]} {INVERTED_PARTS[self.cards[5].left]} {INVERTED_PARTS[self.cards[5].right]}
             {INVERTED_PARTS[self.cards[3].bottom]}   {INVERTED_PARTS[self.cards[4].bottom]}   {INVERTED_PARTS[self.cards[5].bottom]} 
             {INVERTED_PARTS[self.cards[6].top]}   {INVERTED_PARTS[self.cards[7].top]}   {INVERTED_PARTS[self.cards[8].top]} 
            {INVERTED_PARTS[self.cards[6].left]} {INVERTED_PARTS[self.cards[6].right]} {INVERTED_PARTS[self.cards[7].left]} {INVERTED_PARTS[self.cards[7].right]} {INVERTED_PARTS[self.cards[8].left]} {INVERTED_PARTS[self.cards[8].right]}
             {INVERTED_PARTS[self.cards[6].bottom]}   {INVERTED_PARTS[self.cards[7].bottom]}   {INVERTED_PARTS[self.cards[8].bottom]} 
        """)

    @staticmethod
    def check_edges(a: int, b: int) -> bool:
        return (a >> 1) == (b >> 1) and a != b

    def check_left(self, idx: int) -> bool:
        if idx % 3 == 0:
            return True
        else:
            return self.check_edges(self.cards[idx - 1].right, self.cards[idx].left)

    def check_up(self, idx: int) -> bool:
        if idx < 3:
            return True
        else:
            return self.check_edges(self.cards[idx - 3].bottom, self.cards[idx].top)

    def check_idx(self, idx: int) -> bool:
        for _ in range(4):
            if self.check_up(idx) and self.check_left(idx):
                if idx == 8:
                    return True
                else:
                    return self.check_idx(idx + 1)
            else:
                self.cards[idx].rotate()

        return False


if __name__ == "__main__":
    game = None
    for i, card_order in enumerate(permutations(range(9))):
        if i % 1000 == 0:
            print("idx =", i)
        game = Game(map(Card, [CARDS[idx] for idx in card_order]))
        if game.check_idx(0):
            break

    assert game is not None
    print("AAA", game)
