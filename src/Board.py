import numpy as np

class Board:
    def __init__(self):
        self.b = -1*np.ones((4,4),dtype=np.uintc) # Initialize board as empty
        self.open_squares = [(i,j) for i in range(4) for j in range(4)]

    def clear(self):
        self.b = -1*np.ones((4,4),dtype=np.uintc)
        self.open_squares = [(i, j) for i in range(4) for j in range(4)]

    def has_victory(self):
        # Check if the binary representations of nums have the same bit in at least one place
        def all_overlap(nums):
            if nums[0] == -1:
                return False
            one_overlap = np.array([int(i) for i in '{0:04b}'.format(nums[0])])
            zero_overlap = 1 - one_overlap
            for n in nums:
                if n == -1:
                    return False
                one_overlap = one_overlap * np.array([int(i) for i in '{0:04b}'.format(n)])
                zero_overlap = zero_overlap * (1 - np.array([int(i) for i in '{0:04b}'.format(n)]))
            return 1 in one_overlap or 1 in zero_overlap

        return any([all_overlap(pcs) for pcs in [list(self.b[i,:]) for i in range(4)] # Rows
                                              + [list(self.b[:,i]) for i in range(4)] # Columns
                                              + [[self.b[i,i] for i in range(4)], [self.b[i,3-i] for i in range(4)]]]) # Diagonals

    def place_piece(self, piece, coord):
        self.b[coord] = piece
        self.open_squares.remove(coord)

    def print_open(self):
        for i in range(4):
            for j in range(4):
                if self.b[i,j] == -1:
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
                if self.b[i,j] != -1:
                    print(self.b[i,j], end=" ")
                else:
                    print("_", end=" ")
            print()
