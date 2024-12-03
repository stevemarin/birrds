from collections import defaultdict
from enum import Enum
from functools import reduce
from textwrap import dedent


class Sign(Enum):
    I22 = 2
    Route16 = 3
    Route45 = 5
    Route56 = 7
    Route66 = 11
    Flag = 13
    Stop = 17


class Card:
    __slots__ = ("nw", "ne", "se", "sw")

    def __init__(self, nw: Sign, ne: Sign, se: Sign, sw: Sign):
        self.nw = nw
        self.ne = ne
        self.se = se
        self.sw = sw

    def __repr__(self):
        return f"Card: top={(self.nw, self.ne)} right={(self.ne, self.se)} bottom={(self.se, self.sw)} left={(self.sw, self.nw)}"

    def __hash__(self) -> int:
        max_value, num_rotations = reduce(
            lambda a, b: a if a[0] > b[0] else b,
            ((self.nw.value, 0), (self.ne.value, 3), (self.se.value, 2), (self.sw.value, 1)),
        )
        card = self.rotate(num_rotations)
        assert max_value == card.nw.value

        return hash((card.nw.value, card.ne.value, card.se.value, card.sw.value))

    def rotate(self, rotations: int) -> "Card":
        match rotations:
            case 0:
                return Card(self.nw, self.ne, self.se, self.sw)
            case 1:
                return Card(self.sw, self.nw, self.ne, self.se)
            case 2:
                return Card(self.se, self.sw, self.nw, self.ne)
            case 3:
                return Card(self.ne, self.se, self.sw, self.nw)
            case _:
                raise ValueError("invalid number rotations")


def print_cards(played_cards: list[Card]) -> str:
    def print_row(played_cards: list[Card]) -> str:
        return dedent(f"""
            |{played_cards[0].nw.name:>8}{played_cards[0].ne.name:>8}|{played_cards[1].nw.name:>8}{played_cards[1].ne.name:>8}|{played_cards[2].nw.name:>8}{played_cards[2].ne.name:>8}|{played_cards[3].nw.name:>8}{played_cards[3].ne.name:>8}|{played_cards[4].nw.name:>8}{played_cards[4].ne.name:>8}|{played_cards[5].nw.name:>8}{played_cards[5].ne.name:>8}|
            |{played_cards[0].sw.name:>8}{played_cards[0].se.name:>8}|{played_cards[1].sw.name:>8}{played_cards[1].se.name:>8}|{played_cards[2].sw.name:>8}{played_cards[2].se.name:>8}|{played_cards[3].sw.name:>8}{played_cards[3].se.name:>8}|{played_cards[4].sw.name:>8}{played_cards[4].se.name:>8}|{played_cards[5].sw.name:>8}{played_cards[5].se.name:>8}|""")

    return "\n".join(print_row(played_cards[row * 6 : (row + 1) * 6]) for row in range(len(played_cards) // 6))


def check_up(card: Card, played_cards: list[Card]) -> bool:
    if len(played_cards) < 6:
        return True

    above = played_cards[-6]
    return card.nw == above.sw and card.ne == above.se


def check_left(card: Card, played_cards: list[Card]) -> bool:
    if len(played_cards) % 6 == 0:
        return True

    left = played_cards[-1]
    return card.nw == left.ne and card.sw == left.se


def add_card(played_cards: list[Card] = []) -> bool:
    above = None if len(played_cards) < 6 else played_cards[-6]
    cards_matching_above = side_to_cards[above.se.value | above.sw.value] if above is not None else all_cards

    left = None if len(played_cards) % 6 == 0 else played_cards[-1]
    cards_matching_left = side_to_cards[left.ne.value | left.se.value] if left is not None else all_cards

    potential_cards = cards_matching_above.intersection(cards_matching_left) - set(played_cards)

    # print(f"""Played: {len(played_cards)} Potential: {len(potential_cards)}""")

    for card in potential_cards:
        if hash(card) in set(hash(c) for c in played_cards):
            continue
        for num_rotations in range(4):
            rotated_card = card.rotate(num_rotations)
            
            if check_left(rotated_card, played_cards) and check_up(rotated_card, played_cards) and len(set(played_cards + [card])) == len(played_cards) + 1:
                if len(played_cards) == 35:
                    print(print_cards(played_cards + [rotated_card]))
                    hashes = set()
                    for card in played_cards:
                        hashes.add(hash(card))
                    hashes.add(hash(rotated_card))
                    assert len(hashes) == 36
                    exit(0)
                else:
                    add_card(played_cards + [rotated_card])

    return False


if __name__ == "__main__":
    all_cards = set(
        (
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
        )
    )

    assert len(all_cards) == 36

    hashes = set()
    for card in all_cards:
        local_hashes = set()
        for num_rotations in range(4):
            rotated = card.rotate(num_rotations)
            local_hashes.add(hash(rotated))
        assert len(local_hashes) == 1
        hashes = hashes.union(local_hashes)
    print(len(hashes))
    assert len(hashes) == 36

    side_to_cards = defaultdict(set)
    for card in all_cards:
        side_to_cards[card.nw.value | card.ne.value].add(card)
        side_to_cards[card.ne.value | card.se.value].add(card)
        side_to_cards[card.se.value | card.sw.value].add(card)
        side_to_cards[card.sw.value | card.nw.value].add(card)

    print(sorted(side_to_cards.items()))

    # for idx, card in enumerate(all_cards):
    #     print(idx, card.__hash__(), card)

    print(add_card())
