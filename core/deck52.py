from core import CardPile, Card
from .rank import STANDARD_RANKS
from .suit import STANDARD_SUITS
import copy
class Deck52(CardPile):
    ALLCards: list[Card] = [Card(suit=suit, rank=rank) for suit in STANDARD_SUITS for rank in STANDARD_RANKS]
    def __init__(self, comment: str="") -> None:
        super().__init__(cards=copy.deepcopy(Deck52.ALLCards), comment=comment)
    
    
