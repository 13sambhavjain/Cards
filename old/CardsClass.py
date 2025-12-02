from enum import auto, StrEnum, IntEnum, Enum
import random
import itertools
class Suit(StrEnum):
    Spades = auto()
    Hearts = auto()
    Clubs = auto()
    Diamonds = auto()

class Rank(IntEnum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11 
    Queen = 12
    King = 13
    Ace = 14
    # Joker = 0

class SRank(IntEnum):
    Joker = 0
            
class Card():
    def __init__(self, suit: Suit, rank: Rank, face_up: bool|None = None):
        self.suit: Suit = suit
        self.rank: Rank = rank
        self.face_up: bool|None = face_up
    
    def __str__(self, forceReveal: bool = False) -> str:
        if forceReveal or self.face_up != False:
            return f'{self.rank.name} of {self.suit.name}'
        else:
            return f'Hidden Card'
        
    def __repr__(self) -> str:
        return f'Card(suit={self.suit.name}, rank={self.rank.name}, face_up={self.face_up})'
    
    def flip(self):
        self.face_up = not self.face_up
        return
    
    def __hash__(self):
        return hash((self.suit, self.rank))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card): return NotImplemented
        return self.suit == other.suit and self.rank == other.rank

class Deck():
    _PossibleCards: list[Card] = list(Card(*args) for args in itertools.product(Suit, Rank))
    def __init__(self, /, allowDuplicate: bool = False, numberOfCards: int=0, cards: list[Card] = None) -> None:
        if cards==None:
            cards = list()
        self.allowDuplicate: bool = allowDuplicate
        self.cards: list[Card] = cards
        cards2Add = numberOfCards - len(self.cards)
        self.addRandomCards(cards2Add)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def addCard(self, card: Card) -> Card|None:
        if not self.allowDuplicate:
            if card in self.cards:
                return None
        self.cards.append(card)
        return card
    
    def insertCard(self, card: Card, index:int|None=None) -> Card|None:
        """give index = None, if want to insert randomly
        """
        if not self.allowDuplicate:
            if card in self.cards:
                return None
        if index==None:
            index = random.randint(0,len(self.cards))
        self.cards.insert(index, card)
        return card
    
    def addCards(self, cards: list[Card]) -> list[Card]:
        if self.allowDuplicate:
            cards = list(set(cards) - set(self.cards))
        self.cards += cards
        return cards
        
    def addRandomCard(self, PossibleCardsList: Deck|list[Card] = _PossibleCards) -> Card | None:
        if self.allowDuplicate:
            card: Card = random.choice(set(PossibleCardsList) - set(self.cards))
        else:
            card: Card = random.choice(PossibleCardsList)
        if card:
            self.cards.append(card)
            return card
        return None

    def addRandomCards(self, Cards2Add:int=1, PossibleCardsList: Deck|list[Card] = _PossibleCards) -> Card | None:
        if not self.allowDuplicate:
            PossibleCardsList: Card = list(set(PossibleCardsList) - set(self.cards))
        
        added = list(random.sample(PossibleCardsList, Cards2Add))
        self.cards += added
        return added
    
    def dealCard(self, deck: Deck, func: callable = lambda x: x) -> Deck:
        card: Card = self.cards.pop()
        card = func(card)
        deck.addCard(card)
        return self
    
    def __str__(self, forceReveal: bool = True) -> str:
        resp = "Deck From Top => \n"
        for card in reversed(self.cards):
            resp += card.__repr__() + '\n'
        return resp

    def reverse(self) -> Deck:
        self.cards.reverse()
        return self

    def flipCards(self) -> Deck:
        for card in self.cards:
            if card is None:
                print(self.cards)
                k = input('asda')
                return self
            card.flip()
        return self
    
    def flip(self) -> Deck:
        self.reverse()
        self.flipCards()
        return self
    
    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, key:int|slice) -> Card:
        return self.cards[key]
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __reversed__(self):
        return reversed(self.cards)
    
    def __setitem__(self, key: int|slice, card: Card):
        self.cards[key] = card

    def __delitem__(self, key: int|slice):
        del self.cards[key]

    def __add__(self, other: Deck) -> Deck:
        self.cards += other.cards
        self.allowDuplicate |= other.allowDuplicate
        del other
        return self
    
    def __repr__(self):
        return f'cards = {self.cards}\nallowDuplicate = {self.allowDuplicate}'

def magic1():
    deck = Deck(numberOfCards=12)
    cards2insert = [Card(s, SRank.Joker, face_up=True) for s in Suit]
    for card in cards2insert:
        deck.insertCard(card)
    deck.shuffle()
    flip = False
    deck.reverse()
    for card in deck:
        if flip:
            card.flip()
        flip = not flip
    grid = [[Deck() for _ in range(4)] for __ in range(4)]
    # print(deck)
    # print(grid)
    for row in grid:
        for d in row:
            deck.dealCard(d)
    grid[1].reverse()
    grid[3].reverse()
    def foldarow(grid: list[list[Deck]], r=None, c=None):
        if r != None:
            if r == 0:
                r1 = 1
            elif r == -1:
                r1 = -2
            else:
                raise ValueError('r can be either 0 or -1.')
            for i in range(len(grid[r])):
                grid[r1][i] += grid[r][i].flip()
            del grid[r]
        elif c != None:
            if c == 0:
                c1 = 1
            elif c == -1:
                c1 = -2
            else:
                raise ValueError('c can be either 0 or -1.')
            for i in range(len(grid)):
                grid[i][c1] += grid[i][c].flip()
                del grid[i][c]
        else:
            raise ValueError('need to give either r or c as 0 or -1.')
    folds = list()
    args = [0, -1]
    for _ in range(3):
        folds.append((None, random.choice(args)))
        folds.append((random.choice(args), None))
    random.shuffle(folds)
    for fold in folds:
        foldarow(grid, *fold)
    print(grid)














def main():
    magic1()

if __name__ == "__main__":
    main()





