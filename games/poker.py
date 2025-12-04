from core import CardPile, Deck52
import random
from typing import Iterable, Optional
from functools import total_ordering
from collections import deque

@total_ordering
class Chips:
    def __init__(self, amount: int=0) -> None:
        self._amount: int = Chips.validate_amount(amount)
    
    @property
    def amount(self) -> int:
        return self._amount
    
    @amount.setter
    def amount(self, value: int):
        self._amount = self.validate_amount(value)

    def clear(self) -> None:
        self._amount = 0

    @staticmethod
    def validate_amount(amount: int) -> int:
        """returns amount after performing validation (if fails raises ValueError)"""
        if not isinstance(amount, int): 
            raise ValueError(f"Amount of chips must be a int, not {type(amount)=}.")
        if amount < 0:
            raise ValueError(f"Amount of chips must be non negative, {amount=}.")
        return amount
    
    def __int__(self):
        return self._amount
    
    def __str__(self):
        return f"{self._amount} chips"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self._amount})"
    
    def __add__(self, other: Chips) -> Chips:
        if not isinstance(other, Chips): return NotImplemented
        return Chips(self._amount + other._amount)
    
    def __iadd__(self, other: Chips) -> Chips:
        if not isinstance(other, Chips): return NotImplemented
        self._amount += other._amount
        return self

    def __sub__(self, other: Chips) -> Chips:
        if not isinstance(other, Chips): return NotImplemented
        return Chips(self._amount - other._amount)
    
    def __isub__(self, other: Chips) -> Chips:
        if not isinstance(other, Chips): return NotImplemented
        self._amount -= other._amount
        return self
    
    def __mul__(self, other: int) -> Chips:
        if not isinstance(other, int): return NotImplemented
        return Chips(self._amount*other)
    __rmul__ = __mul__
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chips): return NotImplemented
        return self._amount == other._amount

    def __lt__(self, other: Chips) -> bool:
        if not isinstance(other, Chips): return NotImplemented
        return self._amount < other._amount
    
    def __radd__(self, other: int) -> Chips:
        return NotImplemented

    def __rsub__(self, other: int) -> Chips:
        return NotImplemented

ID = str 
class Player:
    def __init__(self, id:ID, bankroll: Chips, stack: Optional[Chips]):
        # Overall Attributes
        self.id = id
        self.bankroll: Chips = bankroll
        # Table Attributes
        self.stack: Chips = stack if stack else Chips(0)
        self.active = True
        self.auto_buyin_atmax = False
        self.auto_top_up = False
        # Round Attributes
        self.hand: Optional[CardPile] = None
        self.folded = False
        self.all_in: bool = False
        self.current_bet: Chips = Chips(0)

    def shift_to_stack(self, amount: Chips) -> None:
        if amount > self.bankroll:
            raise ValueError(f"Insufficient bank role({self.bankroll}), of player({self.id}), for shifting {amount} to stack.")
        else:
            self.bankroll -= amount
            self.stack += amount

    def make_stack_of(self, amount: Chips) -> None:
        self.bankroll += self.stack
        self.stack = Chips(0)
        self.shift_to_stack(amount)

    def bet(self, amount: Chips):
        net_amount = amount - self.current_bet
        if net_amount > self.stack:
            raise ValueError(f"Cannot bet more than the stack. {self.id=}, {self.stack=}, {net_amount=}")
        self.stack -= net_amount
        self.current_bet += net_amount
    

class Table():
    _SIZE_LIMIT = 10 # anything less that 22 but prefer less than 10
    _DEFAULT_BLIND2BUYIN_MIN = 10
    _DEFAULT_BLIND2BUYIN_MAX = 50

    def __init__(self, players: list[Player], blind_amount: Chips, 
                 min_buyin: Optional[Chips]=None, max_buyin: Optional[Chips]=None,
                 low_chips_amount: Optional[Chips] = None,
                 initial_dealer_id=None, size_limit: Optional[int]=None):
        
        # Rules for the table ...mostly will remain unchanged
        self.size_limit:int = size_limit if size_limit else Table._SIZE_LIMIT
        self.blind_amount: Chips = blind_amount
        self.low_chips_amount: Chips = low_chips_amount if low_chips_amount else Chips(0)
        self.max_buyin: Chips = min_buyin if min_buyin else self._DEFAULT_BLIND2BUYIN_MAX*self.blind_amount
        self.min_buyin: Chips = max_buyin if max_buyin else self._DEFAULT_BLIND2BUYIN_MIN*self.blind_amount
        # validating some rules
        if self.min_buyin > self.max_buyin:
            raise ValueError(f"{max_buyin=} is less that {min_buyin=}.")
        if len(players) > self.size_limit:
            raise ValueError("More players are given than the size limit of the table.")
        # players setup
        self.players: deque[Player] = deque(players)
        self.player_map: dict[ID, Player] = {player.id: player for player in players}
        if initial_dealer_id is None:
            initial_dealer_id = self.players[0].id
        elif initial_dealer_id in self.player_map:
            index = self.players.index(self.player_map[initial_dealer_id])
            self.players.rotate(-index)
        else:
            raise ValueError(f"Given ({initial_dealer_id=}) is not in current Table.")
        # Other Game Attributes
        self.round_count = 0
        # self.current_rount
        
class Round:
    def __init__(self, table: Table):
        # round-table linking
        self.table = table
        self.id = table.round_count + 1
        # fixed start of a round
        self.deck: CardPile = Deck52(f"Start deck of round {self.id}").shuffle()
        self.players = self.get_active_players()
        if len(self.players) < 2:
            raise ValueError(f"not enought active players on the table to play poker")
        self.dealCards()
        self.main_pot = Chips(0)
        self.current_bets: dict[ID, Chips] = {}

    @property
    def dealer(self):
        return self.players[0]
    @property
    def small_blind(self):
        return self.players[1]
    @property
    def small_blind(self):
        return self.players[2]
    



    def get_active_players(self) -> list[Player]:
        active_players = []
        for player in self.table.players:
            if player.active:
                if player.auto_top_up:
                    player.make_stack_of(min(player.bankroll, self.table.max_buyin))
                elif player.stack <= self.table.low_chips_amount:
                    if player.auto_buyin_atmax and (player.bankroll + player.stack) >= self.table.min_buyin:
                        player.make_stack_of(min(player.bankroll, self.table.max_buyin))
                    else:
                        player.active=False
                        continue
                player.folded = False
                player.hand = CardPile()
                active_players.append(player)
        return active_players
    
    def dealCards(self):
        for _ in range(2):
            for player in self.players:
                self.deck.dealCard(player.hand, face_up=False)
    
    def place_blinds(self):
        self.current_bets


        
        




        
