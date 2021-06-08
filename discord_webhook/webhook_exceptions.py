class ColourNotInRangeException(Exception):
    """
    A valid colour must take an integer value between 0 and 16777216 inclusive

    This Exception will be raised when a colour is not in that range.
    """

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return repr('"{}" is not in valid range of colors. The valid ranges '
                    'of colors are 0 to 16777215 inclusive (INTEGERS) and 0 '
                    'to FFFFFF inclusive (HEXADECIMAL)'.format(self.color))
