from . import Table, CardPile, Deck52, Chips, Player

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
        half_bets: set[Chips] = set() 
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
                            if amount < self.last_call:
                                print("Wrong amount...it should be more than call")
                                continue
                            bet = self.raise_bet(player, amount)
                        else:
                            print("Wrong Input)")
                            continue
                        if bet != self.last_call:
                            # need to make a side pot
                            half_bets.add(bet)
                    break
        if half_bets:
            reduce: list[Chips] = list(half_bets)
            reduce.sort()
            for r in reduce:
                side_pot = Chips(0)
                for player in self.players:
                    if player.folded or (not player.active) or player.current_bet==0:
                        continue
                    player.current_bet -= r
                    side_pot += r
                    if player.current_bet == 0:
                        player.last_pot_index = len(self.pots)
                self.pots.append(side_pot)
                    
    
    def fold(self, player:Player):
        player.folded = True
        player.current_bet = Chips(0)
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
        self.deck.dealCard(self.burns, face_up=False)
    # community card openings
    def open_flop(self) -> None:
        self.burn_card()
        for _ in range(3):
            self.deck.dealCard(self.community_cards, face_up=True)
    def open_turn(self):
        self.burn_card()
        self.deck.dealCard(self.community_cards, face_up=True)
    open_river = open_turn



# to be moved out

import itertools
def cyclic(lst, start=0):
    return itertools.islice(itertools.cycle(lst), start, None)