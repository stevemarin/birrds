from dataclasses import _DefaultFactory, dataclass
from enum import IntEnum, auto
from copy import copy

class Bird(IntEnum):
    Cardinal = auto()
    Bunting = auto()
    Bluebird = auto()
    Finch = auto()


class Direction(IntEnum):
    Bottom = auto()
    Right = auto()
    Top = auto()
    Left = auto()


@dataclass
class Side:
    bird: Bird
    top: bool

    def matches(self, other: "Side") -> bool:
        return True if self.top ^ other.top and self.bird == other.bird else False


@dataclass
class Card:
    id: int
    bottom: Side
    right: Side
    top: Side
    left: Side

    def matches(self, other: "Card", self_direction: Direction, other_direction: Direction) -> bool:
        if self.id == other.id:
            return False
        
        if self.get_side(self_direction).matches(other.get_side(other_direction)):
            return True
        
        return False
        

    def get_side(self, direction: Direction) -> Side:
        match direction:
            case Direction.Bottom:
                return self.bottom
            case Direction.Right:
                return self.right
            case Direction.Top:
                return self.top
            case Direction.Left:
                return self.left



    def rotate(self, times: int = 1):
        match times % 4:
            case 0:
                pass
            case 1:
                self.right, self.top, self.left, self.bottom = (
                    self.bottom,
                    self.right,
                    self.top,
                    self.left,
                )
            case 2:
                self.top, self.left, self.bottom, self.right = (
                    self.bottom,
                    self.right,
                    self.top,
                    self.left,
                )
            case 3:
                self.left, self.bottom, self.right, self.top = (
                    self.bottom,
                    self.right,
                    self.top,
                    self.left,
                )
            case _:
                raise NotImplementedError

def valid_board(board: list[Card]) -> bool:
    # the board layout is:
    #   [0 1 2
    #    3 4 5
    #    6 7 8]

    if (
        # l to r top row
        board[0].right.matches(board[1].left)
        and board[1].right.matches(board[2].left)
        # top to middle row
        and board[0].bottom.matches(board[3].top)
        and board[1].bottom.matches(board[4].top)
        and board[2].bottom.matches(board[5].top)
        # l to r middle row
        and board[3].right.matches(board[4].left)
        and board[4].right.matches(board[5].left)
        # middle to bottom row
        and board[3].bottom.matches(board[6].top)
        and board[4].bottom.matches(board[7].top)
        and board[5].bottom.matches(board[8].top)
        # l to r bottom row
        and board[6].right.matches(board[7].left)
        and board[7].right.matches(board[8].left)
    ):
        return True

    return False



if __name__ == "__main__":

    cards = [
        Card(
            0,
            Side(Bird.Cardinal, True),
            Side(Bird.Bunting, True),
            Side(Bird.Bluebird, False),
            Side(Bird.Bluebird, True),
        ),
        Card(
            1,
            Side(Bird.Finch, True),
            Side(Bird.Bluebird, True),
            Side(Bird.Bunting, False),
            Side(Bird.Finch, False),
        ),
        Card(
            2,
            Side(Bird.Finch, True),
            Side(Bird.Bunting, False),
            Side(Bird.Bluebird, True),
            Side(Bird.Cardinal, False),
        ),
        Card(
            3,
            Side(Bird.Cardinal, True),
            Side(Bird.Finch, True),
            Side(Bird.Bunting, False),
            Side(Bird.Bluebird, False),
        ),
        Card(
            4,
            Side(Bird.Finch, False),
            Side(Bird.Cardinal, False),
            Side(Bird.Bluebird, True),
            Side(Bird.Bunting, True),
        ),
        Card(
            5,
            Side(Bird.Bluebird, False),
            Side(Bird.Bunting, True),
            Side(Bird.Finch, True),
            Side(Bird.Cardinal, True),
        ),
        Card(
            6,
            Side(Bird.Bunting, False),
            Side(Bird.Bluebird, False),
            Side(Bird.Finch, False),
            Side(Bird.Cardinal, False),
        ),
        Card(
            7,
            Side(Bird.Bluebird, False),
            Side(Bird.Finch, True),
            Side(Bird.Cardinal, False),
            Side(Bird.Bunting, False),
        ),
        Card(
            8,
            Side(Bird.Finch, True),
            Side(Bird.Bunting, False),
            Side(Bird.Bluebird, True),
            Side(Bird.Cardinal, True),
        ),
    ]


    assert len(cards) == 9
    assert (
        len(
            {
                side.bird
                for card in cards
                for side in (card.bottom, card.right, card.top, card.right)
            }
        )
        == 4
    )

    rotated_cards = [copy(card) for card in cards for _ in range(4)]
    for idx in range(len(rotated_cards)):
        card = rotated_cards[idx]
        card.rotate(idx % 4)


        def matches_left_to_right(card: Card, other: Card) -> bool:
            if (card.id != other.id and card.right.matches(other.left)):
                return True
            return False
        
        def matches_top_to_bottom(card: Card, other: Card) -> bool:
            if (card.id != other.id and card.bottom.matches(other.top)):
                return True
            return False

        def matches_both(card: Card, other: Card) -> bool:
            if matches_left_to_right(card, other) and matches_top_to_bottom(card, other):
                return True
            return False


        queue = [([card], filter(lambda other: card.id != other.id, copy(rotated_cards))) for card in cards]

        while len(queue) > 0:
            board, remaining_cards = queue.pop()
            last_card_idx = len(board) - 1

            assert 0 < last_card_idx < 7

            if last_card_idx in (1, 3, 4, 6, 7):
                # check right
                pass

            if last_card_idx in (3, 4, 5, 6, 7, 8):
                # check up
                pass
            