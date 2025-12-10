from . import CardPile, Chips
from typing import Optional

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
        self.hand: CardPile
        self.folded = False
        self.all_in: bool = False
        self.last_pot_index = -1
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



