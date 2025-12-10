from functools import total_ordering

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
    