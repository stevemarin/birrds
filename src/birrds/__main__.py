from itertools import permutations

from .birds import CARDS, Card, Game

game = None
for i, card_order in enumerate(permutations(range(9))):
    game = Game(map(Card, [CARDS[idx] for idx in card_order]))
    if game.check_idx(0):
        print(game)
        break
else:
    print("No answer found...")
