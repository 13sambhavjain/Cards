from .suit import Suit
from .rank import Rank

class Card():
    def __init__(self, suit: Suit, rank: Rank, face_up: bool = False):
        self.suit: Suit = suit
        self.rank: Rank = rank
        self.face_up: bool = face_up
    
    def __str__(self) -> str:
        if self.face_up != False:
            return f'{self.suit}{self.rank}'
        else:
            return f'##'
        
    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}(suit={self.suit.__class__.__name__}.{self.suit.name}, '
                f'rank={self.rank.__class__.__name__}.{self.rank.name}, face_up={self.face_up})')
    
    def flip(self):
        self.face_up = not self.face_up
        return
    
    def __hash__(self):
        return hash((self.suit, self.rank))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.suit == other.suit and self.rank == other.rank