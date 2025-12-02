from enum import StrEnum
class Suit(StrEnum):
    def __new__(cls, symbol: str, color: str):
        member = str.__new__(cls, symbol)
        member._value_ = symbol
        member.color = color
        return member

    SPADES   = ("♠", "Black")
    HEARTS   = ("♥", "Red")
    CLUBS    = ("♣", "Black")
    DIAMONDS = ("♦", "Red")

    def __str__(self) -> str:
        """
        Provides the default string representation when you call str(suit) or print(suit).
        We'll make it return a human-readable combination of name and symbol.
        """
        return f"{self.value}"
        # This will output: "Clubs ♣" or "Diamonds ♦"

    def __format__(self, format_spec: str) -> str:
        """
        Allows custom formatting using f-strings format specifiers, e.g., f"{suit:c}" or f"{suit:name}".
        """
        if format_spec == "symbol" or format_spec == "s":
            return self.value
        if format_spec == "name" or format_spec == "n":
            return self.name.capitalize()
        if format_spec == "color" or format_spec == "c":
            return self.color

        # Default behavior if no specific format is requested
        return self.__str__()
    
    def __repr__(self) -> str:
        """
        Provides the unambiguous representation used in debugging/consoles.
        It clearly shows the class name, name, and color data.
        """
        return f"{self.__class__.__name__}.{self.name}(symbol='{self.value}', color='{self.color}')"

    def __init__(self, symbol: str, color: str):
        """helper __init__ for better type hinting
        (It might not run at runtime but helps Mypy understand the attributes exist)"""
        self.color:str = color