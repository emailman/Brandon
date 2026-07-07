"""
| Create a deck of cards
| Shuffle the deck
| Deal the cards to 4 players
| Show each player's cards
"""

import random


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
        for i, card in enumerate(self.cards):
            players[i % len(players)].hand.append(card)

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


def main():
    # Create a list of 52 cards
    cards = []
    for suit in SUITS:
        for rank in RANKS:
            cards.append(Card(suit, rank))

    # Create a deck using the cards
    deck = Deck(cards)

    # Shuffle the deck
    deck.shuffle()

    # Deal the deck to each of the players
    deck.deal(PLAYERS)

    # Show each player's hand
    for player in PLAYERS:
        print(f"\n{player}:")
        for card in sort_hand(player.hand):
            print(f"\t{card}")


if __name__ == '__main__':
    main()
