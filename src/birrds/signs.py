# from collections import defaultdict
from enum import Enum, auto
from itertools import permutations

class Sign(Enum):
    I22 = auto()
    Route16 = auto()
    Route45 = auto()
    Route56 = auto()
    Route66 = auto()
    Flag = auto()
    Stop = auto()


class Card:
    def __init__(self, nw: Sign, ne: Sign, se: Sign, sw: Sign):
        self.nw = nw
        self.ne = ne
        self.se = se
        self.sw = sw

    def __repr__(self):
        return f"Card: top={(self.nw, self.ne)} right={(self.ne, self.se)} bottom={(self.se, self.sw)} left={(self.sw, self.nw)}"

    def rotate(self) -> None:
        self.nw, self.ne, self.se, self.sw = self.sw, self.nw, self.ne, self.se
        # match n % 4:
        #     case 0:
        #         pass
        #     case 1:
        #         self.nw, self.ne, self.se, self.sw = self.sw, self.nw, self.ne, self.se
        #     case 2:
        #         self.nw, self.ne, self.se, self.sw = self.se, self.sw, self.nw, self.ne
        #     case 3:
        #         self.nw, self.ne, self.se, self.sw = self.ne, self.se, self.sw, self.nw


class Game:
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def check_up(self, idx: int) -> bool:
        if idx < 6:
            return True
        
        bottom, top = self.cards[idx], self.cards[idx - 6]
        return bottom.nw == top.sw and bottom.ne == top.se

    def check_left(self, idx: int) -> bool:
        if idx % 6 == 0:
            return True

        right, left = self.cards[idx], self.cards[idx - 1]
        return right.nw == left.ne and right.sw == left.se

    def check_rotation(self, idx: int) -> bool:
        return self.check_left(idx) and self.check_up(idx)

    def check_layout_to_idx(self, idx: int) -> bool:
        for _ in range(4):
            if self.check_rotation(idx):
                if idx == 35:
                    return True
                else:
                    return self.check_layout_to_idx(idx + 1)
            else:
                self.cards[idx].rotate()

        return False

    def solve(self):
        for _, card_order in enumerate(permutations(range(36))):
            if _ % 1_000_000 == 0:
                print("on layout:", _)
            self.cards = [self.cards[idx] for idx in card_order]
            if self.check_layout_to_idx(0):
                print("solution found")
                break
        else:
            print("no solution found")


if __name__ == "__main__":
    cards = [
        Card(Sign.Stop, Sign.Route56, Sign.Route16, Sign.Flag),
        Card(Sign.I22, Sign.Route45, Sign.Route56, Sign.Stop),
        Card(Sign.Flag, Sign.Route66, Sign.Route45, Sign.I22),
        Card(Sign.I22, Sign.Route56, Sign.Route66, Sign.Flag),
        Card(Sign.Route45, Sign.Stop, Sign.Route56, Sign.I22),
        Card(Sign.Route45, Sign.Flag, Sign.Route16, Sign.Stop),
        Card(Sign.Route56, Sign.Route66, Sign.Route45, Sign.Route16),
        Card(Sign.Route45, Sign.I22, Sign.Route66, Sign.Route56),
        Card(Sign.Route66, Sign.Stop, Sign.I22, Sign.Route45),
        Card(Sign.Route66, Sign.Route56, Sign.Route16, Sign.Stop),
        Card(Sign.Stop, Sign.Route45, Sign.Route16, Sign.Route56),
        Card(Sign.Route16, Sign.Route66, Sign.Route45, Sign.Stop),
        Card(Sign.Route16, Sign.I22, Sign.Route45, Sign.Route66),
        Card(Sign.Route56, Sign.Route16, Sign.Route66, Sign.I22),
        Card(Sign.Route45, Sign.Route56, Sign.I22, Sign.Stop),
        Card(Sign.I22, Sign.Route45, Sign.Stop, Sign.Route16),
        Card(Sign.Route56, Sign.I22, Sign.Route16, Sign.Route45),
        Card(Sign.I22, Sign.Route56, Sign.Route45, Sign.Route66),
        Card(Sign.Stop, Sign.Route66, Sign.I22, Sign.Route16),
        Card(Sign.Route66, Sign.Stop, Sign.Route16, Sign.Route56),
        Card(Sign.Route16, Sign.Route66, Sign.Route56, Sign.Route45),
        Card(Sign.Stop, Sign.Route16, Sign.Route45, Sign.I22),
        Card(Sign.Route66, Sign.Stop, Sign.I22, Sign.Route56),
        Card(Sign.Stop, Sign.Route66, Sign.Route56, Sign.I22),
        Card(Sign.Route66, Sign.Stop, Sign.Route45, Sign.Route56),
        Card(Sign.Stop, Sign.Route66, Sign.I22, Sign.Route45),
        Card(Sign.Route66, Sign.Route16, Sign.Route56, Sign.I22),
        Card(Sign.Route16, Sign.Stop, Sign.I22, Sign.Route56),
        Card(Sign.Stop, Sign.Route66, Sign.Route16, Sign.I22),
        Card(Sign.Route66, Sign.Stop, Sign.Route56, Sign.Route16),
        Card(Sign.Route16, Sign.Route45, Sign.Route66, Sign.I22),
        Card(Sign.Route45, Sign.Route56, Sign.I22, Sign.Route66),
        Card(Sign.Flag, Sign.Route56, Sign.Route45, Sign.Stop),
        Card(Sign.Route56, Sign.Flag, Sign.Route45, Sign.Route16),
        Card(Sign.I22, Sign.Route16, Sign.Stop, Sign.Route45),
        Card(Sign.Route56, Sign.Route45, Sign.Route16, Sign.I22),
    ]

    # sides = defaultdict(set)
    # for card in cards:
    #     sides[card.top].add(card)
    #     sides[card.right].add(card)
    #     sides[card.bottom].add(card)
    #     sides[card.left].add(card)

    # played_cards = set()
    # for initial_card_idx in range(12):
    #     card = cards[initial_card_idx]
    #     played_cards.add(card)

    game = Game(cards)
    sides = {}
    for card in game.cards:
        print(card)

    game.solve()
    for card in game.cards:
        print(card)
