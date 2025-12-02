from enum import IntEnum
class Rank(IntEnum):
    def __new__(cls, value: int, short_name: str):
        member = int.__new__(cls, value)
        member._value_ = value
        member.short_name = short_name
        return member

    def __init__(self, value: int, short_name: str="") -> None:
        """Just for type checkers...wont run in runtime"""
        self.short_name = short_name
        
    # Define members: NAME = (INTEGER_VALUE, SHORT_NAME)
    Two   = (2, "2")
    Three = (3, "3")
    Four  = (4, "4")
    Five  = (5, "5")
    Six   = (6, "6")
    Seven = (7, "7")
    Eight = (8, "8")
    Nine  = (9, "9")
    Ten   = (10, "T")
    Jack  = (11, "J")
    Queen = (12, "Q")
    King  = (13, "K")
    Ace   = (14, "A")

    def __str__(self) -> str:
        """
        Returns the short name as the default string representation.
        """
        return self.short_name

    def __repr__(self) -> str:
        """
        Unambiguous representation for debugging.
        """
        return f"{self.__class__.__name__}.{self.name}(value={self.value}, short_name='{self.short_name}')"

    def __format__(self, format_spec: str) -> str:
        """
        Allows formatting for value, name, or short_name.
        """
        if format_spec == "value" or format_spec == "v":
            return str(self.value)
        if format_spec == "name" or format_spec == "n":
            return self.name.capitalize()
        if format_spec == "short" or format_spec == "s":
            return self.short_name
        return self.__str__()
    
    