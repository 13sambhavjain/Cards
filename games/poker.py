from core import CardPile, Deck52, Rank, Card
import random, itertools
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
    def __init__(self, id:ID, bankroll: Chips, stack: Optional[Chips]=None):
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

    def bet(self, amount: Chips) -> Chips:
        "returns the net amount that a play adds to his current bet, all-in if insufficient"
        net_amount = amount - self.current_bet
        if net_amount >= self.stack:
            net_amount = self.stack
            self.all_in = True
            # raise ValueError(f"Cannot bet more than the stack. {self.id=}, {self.stack=}, {net_amount=}")
        self.stack -= net_amount
        self.current_bet += net_amount
        return net_amount

def cyclic(lst, start=0):
    return itertools.islice(itertools.cycle(lst), start, None)


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
        
class Round:
    def __init__(self, table: Table):
        # round-table linking
        self.table = table
        self.id = table.round_count + 1
        # fixed start of a round
        self.deck: CardPile = Deck52(f"Start deck of round {self.id}")
        self.deck.shuffle()
        self.players = self.get_active_players()
        if len(self.players) < 2:
            raise ValueError(f"not enought active players on the table to play poker")
        self.dealCards()
        self.community_cards = CardPile([], f"Community cards for round({self.id})")
        self.burns = CardPile([], f"Burn cards for round({self.id})")
        self.pots= [Chips(0)]
        self.call_amount: Chips = Chips(0)


    @property
    def dealer(self):
        return self.players[0]
    @property
    def small_blind(self):
        return self.players[1]
    @property
    def big_blind(self):
        return self.players[2%len(self.players)]
    @property
    def current_pot(self):
        return self.pots[-1]
    @current_pot.setter
    def current_pot(self, value: Chips):
        self.pots[-1] = value


    def get_active_players(self) -> list[Player]:
        active_players = []
        for player in self.table.players:
            if player.active:
                if player.auto_top_up:
                    player.make_stack_of(min(player.bankroll, self.table.max_buyin))
                if player.stack <= self.table.low_chips_amount:
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
        blind = self.small_blind.bet(self.table.blind_amount)
        b_blind = self.big_blind.bet(2*self.table.blind_amount)
        self.current_pot = blind + b_blind
        self.last_call = max(blind, b_blind)
        

    def betting_round(self, start: int=0):
        half_bets = []
        for player in cyclic(self.players, start):
            if player.all_in or player.folded or (not player.active):
                continue
            elif self.last_call == player.current_bet:
                break
            else:
                while True:
                    play = input(f"{player.id=} fold(f), call(c) {self.call_amount}, raise(r <amount>)")
                    if play == 'f':
                        self.fold(player)
                    else:
                        if play == 'c':
                            bet = self.call(player)
                        elif play[0] == 'r':
                            amount = Chips(int(play.split()[-1]))
                            bet = self.raise_bet(player, amount)
                        else:
                            print("Wrong Input)")
                            continue
                        if bet != self.last_call:
                            # need to make a side pot
                            half_bets.append(bet)
                    break
             


    
    def fold(self, player:Player):
        player.folded = True
    def call(self, player: Player):
        bet = player.bet(self.last_call)
        self.current_pot += bet
        return bet
    def raise_bet(self, player: Player, amount: Chips):
        bet = player.bet(amount)
        self.current_pot += bet
        self.last_call = max(self.last_call, bet)
        return bet
    def burn_card(self) -> None:
        self.deck.dealCard(self.burns, face_up=None)
    # community card openings
    def open_flop(self) -> None:
        self.burn_card()
        for _ in range(3):
            self.deck.dealCard(self.community_cards, face_up=True)
    def open_turn(self):
        self.burn_card()
        self.deck.dealCard(self.community_cards, face_up=True)
    open_river = open_turn
    
    def rank_hand(self, player: Player) -> tuple[int, list[Card]]:
        net = self.community_cards + player.hand
        suit_counts = net.suit_counts()
        flush = False
        for suit, count in suit_counts.items():
            if count >= 5:
                # check staright flush to flush
                # check straight fluch here
                flush = True
                f_suit = suit
                break
        if flush:
            f_suit_cards: list[Card] = []
            for card in net:
                if card.suit == f_suit:
                    f_suit_cards.append(card)
            f_suit_cards.sort(reverse=True, key=lambda card: card.rank)
            s_flush = self.straight_flush(f_suit_cards)
            if s_flush:
                if s_flush[0].rank == Rank.Ace:
                    return 1, s_flush # Royal Flush
                else:
                    return 2, s_flush # Straight Flush
            
        rank_counts = dict(sorted(net.rank_counts().items() ,key=lambda x: (x[1], x[0]), reverse=True))
        if rank_counts[0] == 4:
            # Four of a kind
            pass
        if rank_counts[0] == 3 and rank_counts[1] >= 2:
            # Full House
            pass
        if flush:
            return 5, f_suit_cards[:6]
        if 




            
                
    def rank_hands(self):
        ans = dict()
        for player in self.players:
            if player.active and not player.folded:
                ans[player.id] = self.rank_hand(player)
        return ans
        
        
        # not straight flush
        # check four of a kind, three    
    def round_end(self):
        
        pass

    @staticmethod
    def straight_flush(f_suit_cards: list[Card]) -> bool|list[Card]:
        count = 0
        for i in range(1, len(f_suit_cards)):
            if f_suit_cards[i-1].rank - f_suit_cards[i].rank == 1:
                count += 1
                if count == 5: #straight flush is there
                    last_card_index = i
                    break
            else:
                count = 0
                if i > 3:
                    return False
        else:
            return False
        return f_suit_cards[last_card_index-5: last_card_index+1]
    
    def

        



        
        




        
