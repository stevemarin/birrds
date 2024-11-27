from itertools import permutations

from .birds import CARDS, Card, Game

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
