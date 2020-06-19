import numpy as np

from direction import Direction
from cell import Cell


class NeedlemanWunschAlgorithm:
    """
    Class representing Needleman-Wunsch algorithm
    """

    def __init__(self, seq1, seq2, config):
        self.seq1 = "-" + seq1
        self.seq2 = "-" + seq2
        self.len1 = len(seq1)
        self.len2 = len(seq2)
        self.config = config
        self._scoring_matrix = None
    
    
    def _prepare_scoring_matrix(self):
        # Scoring matrix dimensions
        n_row = self.len2 + 1
        n_col = self.len1 + 1

        scoring_matrix = np.empty((n_row, n_col), dtype = Cell)
        
        scoring_matrix[0, 0] = Cell()
        scoring_matrix[0, 0].value = 0
        scoring_matrix[0, 0].directions = None
        #filling first row values
        for j in range(1, n_col):
            scoring_matrix[0, j] = Cell()
            scoring_matrix[0, j].value = j * self.config.GAP_PENALTY
            scoring_matrix[0, j].directions = Direction.LEFT
        #filling first column    
        for i in range(1, n_row):
            scoring_matrix[i, 0] = Cell()
            scoring_matrix[i, 0].value = i * self.config.GAP_PENALTY
            scoring_matrix[i, 0].directions = Direction.UP

            for j in range(1, n_col):
                val_up = scoring_matrix[i-1, j].value + self.config.GAP_PENALTY
                val_left = scoring_matrix[i, j-1].value + self.config.GAP_PENALTY
                val_diag = scoring_matrix[i-1, j-1].value + (self.config.SAME if self.seq1[j] == self.seq2[i] else self.config.DIFF)
                values = {Direction.UP: val_up, Direction.LEFT: val_left, Direction.DIAG: val_diag}

                scoring_matrix[i, j] = self._get_cell(values)

        return scoring_matrix
    
    
    def _get_cell(self, values):
        max_value = max(values.values())
        
        directions_list = [idx for idx, val in values.items() if val == max_value]
        
        direction = 0
        for d in directions_list:
            direction = direction | d
            
        cell = Cell()
        cell.value = max_value
        cell.directions = direction
            
        return cell
            
            
    def _next_step(self, char, main_direction, directions):
        value = directions.value
        if value & Direction.UP.value:
            yield char if main_direction == Direction.UP else "_", (0, -1)
        if value & Direction.LEFT.value:
            yield char if main_direction == Direction.LEFT else "_", (-1, 0)
        if value & Direction.DIAG.value:
            yield char, (-1, -1)
            
 
    def _get_result(self, x, y, R, seq, direction):
        if x == 0 and y == 0:
            yield R
            return
        
        cell = self.get_scoring_matrix()[x, y]        
        char = seq[y if direction == Direction.LEFT else x]
        
        for letter, coord in self._next_step(char, direction, cell.directions):
            new_R = letter + R
            new_x = x + coord[1]
            new_y = y + coord[0]
            for result in self._get_result(new_x, new_y, new_R, seq, direction):
                yield result
    
    
    def get_result(self):
        gen1 = self._get_result(self.len2, self.len1, "", self.seq1, Direction.LEFT)
        gen2 = self._get_result(self.len2, self.len1, "", self.seq2, Direction.UP)
        try:
            for i in range(0, self.config.MAX_NUMBER_PATHS):
                yield (next(gen1), next(gen2))
        except StopIteration:
            return
    
    
    def get_scoring_matrix(self):
        if self._scoring_matrix is None:
            self._scoring_matrix = self._prepare_scoring_matrix()
        for i in range(self.len2 + 1):
            for j in range(self.len1 + 1):
                print(i,":",j,"--",self._scoring_matrix[i,j].value ," : : ",self._scoring_matrix[i,j].directions)    
        return self._scoring_matrix
    
    
    def get_score(self):
        return self.get_scoring_matrix()[self.len2, self.len1].value
    
    
    def print_results(self, output):
        with open(output, "w") as out:
            out.write(f"SCORE={self.get_score()} \n")
            result = self.get_result()
            result_list = list(result)
            for r in result_list:
                out.write("\n")
                out.write(f"{r[0]}\n")
                out.write(f"{r[1]}\n")
