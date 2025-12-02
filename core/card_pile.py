from .card import Card
import random

# _PossibleCards: list[Card] = list(Card(*args) for args in itertools.product(Suit, Rank))
class CardPile():
    "A stack of Cards in the event"
    "Last element of cards is the topmost card of the deck"
    def __init__(self, /, 
                 cards: list[Card] = None, #type: ignore
                 comment: str=""
                 ) -> None:
        # self.allowDuplicate: bool = allowDuplicate
        self._cards: list[Card] = cards if cards else list()
        self.comment: str = comment

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def addCard(self, card: Card) -> None:
        self._cards.append(card)

    def insertCard(self, index:int, card: Card) -> None:
        self._cards.insert(index, card)

    def addCards(self, cards: list[Card]) -> None:
        self._cards += cards
    
    def dealCard(self, deck: CardPile, face_up: bool|None = None) -> CardPile:
        card: Card = self._cards.pop()
        if face_up is not None:
            card.face_up = face_up
        deck.addCard(card)
        return self
    
    def __str__(self) -> str:
        resp = f"CardPile({self.comment!r}) From Bottom to Top => "
        # for card in self._cards:
        #     resp += card.__repr__() + '\n'
        return resp + " ".join(str(card) for card in self._cards)

    def reverse(self) -> None:
        self._cards.reverse()

    def flipCards_inplace(self) -> None:
        for card in self._cards:
            card.flip()

    def flip(self) -> None:
        self._cards.reverse()
        self.flipCards_inplace()
    
    def __iter__(self):
        return iter(self._cards)

    def __getitem__(self, key):
        return self._cards[key]
    
    def __len__(self) -> int:
        return len(self._cards)
    
    def __reversed__(self):
        return reversed(self._cards)
    
    def __setitem__(self, key, card):
        self._cards[key] = card

    def __delitem__(self, key: int|slice):
        del self._cards[key]

    def __add__(self, other: CardPile|Card|list[Card]) -> CardPile:
        if isinstance(other, CardPile):
            return CardPile(
                cards=self._cards + other._cards,
                comment=self.comment + other.comment
            )
        elif isinstance(other, list):
            return CardPile(self._cards + other, self.comment)
        elif isinstance(other, Card):
            return CardPile(self._cards + [other], self.comment)
        else:
            return NotImplemented
        
    def __iadd__(self, other: CardPile|Card|list[Card]) -> CardPile:
        if isinstance(other, CardPile):
            self._cards += other._cards
            self.comment += other.comment
        elif isinstance(other, list):
            self._cards += other
        elif isinstance(other, Card):
            self._cards.append(other)
        else:
            return NotImplemented
        return self
    
    def __repr__(self):
        return f'{self.__class__.__name__}(cards={self._cards!r},comment={self.comment})'


