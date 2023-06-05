from typing import Union


class ColorNotInRangeException(Exception):
    """
    This Exception will be raised when a color is not in that range.

    A valid color must take an integer value between 0 and 16777216 inclusive
    """

    color: Union[str, int]

    def __init__(self, color: Union[str, int]) -> None:
        self.color = color
        super().__init__()

    def __str__(self) -> str:
        return repr(
            f"{self.color!r} is not in valid range of colors. The valid ranges "
            "of colors are 0 to 16777215 inclusive (INTEGERS) and 0 "
            "to FFFFFF inclusive (HEXADECIMAL)"
        )
