from core import CardPile, Rank, Card, Suit
import copy
RANKS: list[Rank] = [Rank(14)] + [Rank(x) for x in range(2, 14)]
SUITS: list[Suit] = [Suit.SPADES, Suit.HEARTS, Suit.CLUBS, Suit.DIAMONDS]
class Deck52(CardPile):
    ranks = RANKS
    suits = SUITS
    ALLCards: list[Card] = [Card(suit=suit, rank=rank) for suit in SUITS for rank in RANKS]
    def __init__(self, comment: str="") -> None:
        super().__init__(cards=copy.deepcopy(Deck52.ALLCards), comment=comment)
    
    
