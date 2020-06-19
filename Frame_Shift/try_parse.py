"""
Functions trying parse text to number
"""


def to_int(text):
    try:
        return int(text), True
    except ValueError:
        return text, False
        
        
def to_float(text):
    try:
        return float(text), True
    except ValueError:
        return text, False
        