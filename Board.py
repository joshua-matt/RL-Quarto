import numpy as np

class Board:
    def __init__(self):
        self.b = np.zeros((4,4),dtype=np.uintc) # Initialize board as empty
        self.open_squares = [(i,j) for i in range(4) for j in range(4)]

    def clear(self):
        self.b = np.zeros((4,4))

    def has_victory(self):
        # Check if the binary representations of nums have the same bit in at least one place
        def all_overlap(nums):
            one_overlap = nums[0]
            zero_overlap = ~nums[0]
            for n in nums:
                if n == 0:
                    return False
                one_overlap = one_overlap & n
                zero_overlap = zero_overlap & ~n
            return one_overlap > 0 or zero_overlap > 0

        return any([all_overlap(pcs) for pcs in [list(self.b[i,:]) for i in range(4)] # Rows
                                              + [list(self.b[:,i]) for i in range(4)] # Columns
                                              + [[self.b[i,i] for i in range(4)], [self.b[i,3-i] for i in range(4)]]]) # Diagonals

    def place_piece(self, piece, coord):
        self.b[coord] = piece
        self.open_squares.remove(coord)

    def print_open(self):
        for i in range(4):
            for j in range(4):
                if self.b[i,j] == 0:
                    print(4*j + i + 1, end=" ")
                else:
                    print("X", end=" ")
            print()

    def to_string(self):
        st = ""
        for i in range(4):
            for j in range(4):
                if self.b[i,j] != 0:
                    st += str(self.b[i,j]) + " "
                else:
                    st += "_ "
        return st

    def print_board(self):
        for i in range(4):
            for j in range(4):
                if self.b[i,j] != 0:
                    print(self.b[i,j], end=" ")
                else:
                    print("_", end=" ")
            print()
