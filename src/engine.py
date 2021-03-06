from Board import Board
from numpy import random as rn

class Game:
    def __init__(self, p1, p2):
        self.remaining_pieces = list(range(1,17))
        self.board = Board()
        self.p1 = p1
        self.p2 = p2

        self.players = [p1, p2]
        self.current_p = 0

    def remove_piece(self, piece):
        self.remaining_pieces.remove(piece)

    def play_piece(self, piece, coord):
        self.board.place_piece(piece,coord)

    def open_squares(self):
        return self.board.open_squares

    def play_game(self,verbose=False):
        trajectory = []
        winner = -1

        while len(self.board.open_squares) > 0:
            if verbose:
                print("\n" * 30)
                print("CURRENT BOARD")
                self.board.print_board()
                print()

            curr = self.players[self.current_p]
            piece = curr.choose_piece(self.board, self.remaining_pieces)
            self.remove_piece(piece)

            coord = self.players[(self.current_p+1)%2].place_piece(self.board, piece)
            self.play_piece(piece, coord)
            self.current_p = (self.current_p+1)%2
            trajectory.append((self.board.to_string(), piece, self.board.open_squares, coord))

            if self.board.has_victory():
                winner = (self.current_p+1)%2
                break

        if verbose:
            print("\n\nFINAL BOARD")
            self.board.print_board()
            print("Player %d wins!" % (self.current_p+2))

        return (trajectory, winner)

class HumanPlayer:
    def choose_piece(self, board, options):
        print("Which piece would you like to give your opponent? Options: ", options)
        return int(input())

    def place_piece(self, board, piece):
        board.print_open()
        print("Your opponent gave you piece %d. Where would you like to place it?" % (piece))
        choice = int(input())

        while ((choice-1) % 4, (choice-1) // 4) not in board.open_squares:
            print("That square already has a piece in it! Where would you like to place piece %d?" % (piece))
            choice = int(input())

        return ((choice-1) % 4, (choice-1) // 4)

class AIPlayer:
    def __init__(self, mdp):
        self.mdp = mdp

    def choose_piece(self, board, options):
        return self.mdp.choice_function(board, options)

    def place_piece(self, board, piece):
        return self.mdp.piece_function(board, piece)
