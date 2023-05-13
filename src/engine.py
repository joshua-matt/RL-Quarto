from Board import Board
import pygame as pg
import random as rn

class Game:
    def __init__(self, p1, p2):
        self.remaining_pieces = list(range(0,16))
        self.board = Board()
        self.p1 = p1
        self.p2 = p2

        self.players = [p1, p2]
        self.current_p = 0
        self.turn_phase = 0
        self.key_pressed = pg.K_0

    def pass_key(self, key):
        self.key_pressed = key

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

            has_victory, info = self.board.has_victory()
            win_method = ""
            if info < 4:
                win_method = "row" + str(info + 1)
            elif info >= 4 and info < 8:
                win_method = "col" + str(info - 3)
            else:
                win_method = "diag" + str(info - 5)

            if has_victory:
                winner = (self.current_p+1)%2
                break

        if verbose:
            print("\n\nFINAL BOARD")
            self.board.print_board()
            print("Player %d wins by %s!" % (self.current_p+1, win_method))

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

class MDP:
    def choice_function(self, board, options):
        return rn.choice(options)

    def piece_function(self, board, piece):
        return rn.choice(board.open_squares)