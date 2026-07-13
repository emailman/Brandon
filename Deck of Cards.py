"""
| Create a deck of cards
| Shuffle the deck
| Deal the cards to 4 players
| Show each player's cards
"""

import random
from pathlib import Path
from guizero import *


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        i = 0
        while self.cards:
            card = self.cards.pop()
            players[i % len(players)].hand.append(card)
            i += 1

    def __str__(self):
        return '\n'.join(str(card) for card in self.cards)


class Player:
    def __init__(self, name, hand: list[Card] | None = None):
        self.name = name
        self.hand = hand if hand is not None else []

    def __str__(self):
        return self.name


def sort_hand(hand):
    return sorted(hand, key=lambda card: (SUITS.index(card.suit),
                                          RANKS.index(card.rank)))


SUITS = 'Clubs', 'Diamonds', 'Hearts', 'Spades'
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10',
         'Jack', 'Queen', 'King', 'Ace')
PLAYERS = [Player(name) for name in ('East', 'South', 'West', 'North')]

CARD_IMAGE_DIR = Path(__file__).parent / "cards"
CARD_WIDTH, CARD_HEIGHT = 55, 84
CARD_OFFSET = 25
CARD_MARGIN = 10


def card_image_path(card):
    return str(CARD_IMAGE_DIR / f"{card.rank.lower()}_of_{card.suit.lower()}.png")


def main():
    def show_players():
        boxes = {'North': box_north, 'South': box_south,
                 'East': box_east, 'West': box_west}
        for player in PLAYERS:
            print(f"\n{player}:")
            hand = sort_hand(player.hand)
            for card in hand:
                print(f"\t{card}")

            box = boxes[player.name]
            for i, card in enumerate(hand):
                # visible=False stops guizero re-packing every sibling each
                # time a new Picture is added, which would undo the place()
                # positioning below.
                picture = Picture(box, image=card_image_path(card),
                                   width=CARD_WIDTH, height=CARD_HEIGHT,
                                   visible=False)
                # overlap the cards so all 13 fit in the TitleBox
                picture.tk.place(x=CARD_MARGIN + i * CARD_OFFSET, y=CARD_MARGIN)

    # Create a graphical playing table
    app = App(height=800, width=1000)

    Box(app, height=50, width=100)
    box_top = Box(app, height=200, width=500, border=1)
    box_north = TitleBox(box_top, text='North', height=190, width=400, border=1)

    Box(app, height=50, width=100)
    box_middle = Box(app, height=200, width=900, border=1)
    box_west = TitleBox(box_middle, text='West', height=190, width=400, border=1,
                        align='left')
    box_east = TitleBox(box_middle, text='East', height=190, width=400, border=1,
                        align='right')


    Box(app, height=50, width=100)
    box_bottom = Box(app, height=200, width=500, border=1)
    box_south = TitleBox(box_bottom, text='South', height=190, width=400, border=1)

    # Create a list of 52 cards
    cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    # Create a deck using the cards
    deck = Deck(cards)

    # Shuffle the deck
    deck.shuffle()

    # Deal the deck to each of the players
    deck.deal(PLAYERS)

    # Show each player's hand
    show_players()

    app.display()


if __name__ == '__main__':
    main()
