from core import CardPile, Deck52
import random
from typing import Iterable, Optional
from functools import total_ordering
from collections import deque

@total_ordering
class Chips:
    def __init__(self, amount: int) -> None:
        self._amount: int = Chips.validate_amount(amount)
    
    @property
    def amount(self) -> int:
        return self._amount
    
    @amount.setter
    def amount(self, value: int):
        self._amount = self.validate_amount(value)

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
    def __init__(self, id:ID, bankroll: Chips, stack: Chips=0):
        self.id = id
        self.bankroll: Chips = bankroll
        self.stack: Chips = stack
        self.hand: CardPile
        self.active = True
        self.folded = False
        self.auto_buyin_atmax = False
        self.auto_top_up = False

    def shift_to_stack(self, amount: Chips) -> None:
        if amount > self.bankroll:
            raise ValueError(f"Insufficient bank role({self.bankroll}), of player({self.id}), for shifting {amount} to stack.")
        else:
            self.bankroll -= amount
            stack += amount

    def make_stack_of(self, amount: Chips) -> None:
        self.bankroll += self.stack
        self.stack = 0
        self.shift_to_stack(amount)

class Table():
    _SIZE_LIMIT = 10 # anything less that 22 but prefer less than 10
    _DEFAULT_BLIND2BUYIN_MIN = 10
    _DEFAULT_BLIND2BUYIN_MAX = 50

    def __init__(self, players: list[Player], blind_amount: Chips, 
                 min_buyin: Optional[Chips]=None, max_buyin: Optional[Chips]=None,
                 low_chips_amount: Optional[Chips] = None,
                 initial_dealer_id=None, size_limit: Optional[int]=None):
        
        self.size_limit:int = size_limit if size_limit else Table._SIZE_LIMIT
        if len(players) > self.size_limit:
            raise ValueError("More players are given than the size limit of the table.")
        
        self.players: deque[Player] = deque(players)
        self.player_map: dict[ID, Player] = {player.id: player for player in players}

        if initial_dealer_id is None:
            initial_dealer_id = random.choice(self.player_map.keys())
        if initial_dealer_id in self.player_map:
            index = self.players.index(self.player_map[initial_dealer_id])
            self.players.rotate(-index)
        else:
            raise ValueError(f"Given ({initial_dealer_id=}) is not in current Table.")
        
        self.blind_amount = blind_amount
        self.max_buyin = min_buyin if min_buyin else self._DEFAULT_BLIND2BUYIN_MAX*self.blind_amount
        self.min_buyin = max_buyin if max_buyin else self._DEFAULT_BLIND2BUYIN_MIN*self.blind_amount
        if self.min_buyin > self.max_buyin:
            raise ValueError(f"{max_buyin=} is less that {min_buyin=}.")
        self.low_chips_amount = low_chips_amount if low_chips_amount else 2*self.blind_amount
        

        
class Round:
    def __init__(self, table: Table):
        self.table = table
    def get_active_players(self):
        active_players = []
        for player in self.table.players:
            if player.active:
                if player.auto_top_up:
                    player.make_stack_of(min(player.bankroll, self.table.max_buyin))
                if player.stack <= self.table.low_chips_amount:
                    if player.auto_buyin_atmax and (player.bankroll+) >= self.table.min_buyin:
                        player.make_stack_of(min(player.bankroll, self.table.max_buyin))
                    else:
                        player.active=False
                        continue
                player.folded = False
                active_players.append(player)

    def dealCards

        
