from enum import IntFlag


class Direction(IntFlag):
    """
    Enum representing directions
    """

    UP = 1
    LEFT = 2
    DIAG = 4
    