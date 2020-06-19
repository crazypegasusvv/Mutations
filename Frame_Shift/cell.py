class Cell:
    """
    Class representing cell of the matrix with value and directions
    """

    def __init__(self):
        self.value = None
        self.directions = None
    
    
    def __str__(self):
        value = "None" if self.value is None else str(self.value)
        direction = "None" if self.directions is None else str(self.directions)
        return f"Value: {value}, Direction: {direction}"
    

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.value == other.value and self.directions == other.directions
        return False
        