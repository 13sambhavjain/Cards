from . import Chips, Player, ID
from typing import Optional
from collections import deque

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
        self.init_active_player_stack_forced()
        self.round_count = 0
        # self.current_rount
    def init_active_player_stack_forced(self):
        for player in self.players:
            player.make_stack_of(min(self.max_buyin, player.bankroll))