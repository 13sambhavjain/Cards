from core import CardPile, Deck52
import random
from typing import Iterable
class Poker():
    def __init__(self, player_ids: Iterable, initial_blind_id=None):
        self.players = {id: CardPile([], f"Hand of Player({id})") for id in player_ids}
        self.deck = Deck52("Starting deck of all cards").shuffle()
        self.community = CardPile([], "Comunity cards of Poker game (Flop, Turn, River)")
        self.blind = initial_blind_id if initial_blind_id else random.choice(self.players)

    def round_deal(self):
        
