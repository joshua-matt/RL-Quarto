import Board
import numpy as np
from engine import Game, AIPlayer
from numpy import random as rn

class QuartoMDP:
    def __init__(self, ep, lambd, Q={}):
        self.ep = ep # For epsilon-greedy policy
        self.lambd = lambd # For eligibility trace
        self.Q = Q

    def train_self_play(self, episodes):
        opp = self
        av_return = 0
        returns = [0]

        for i in range(1, episodes+1):
            self.ep = 1 / i # Doubles as epsilon and alpha

            cached = QuartoMDP(self.ep, self.lambd, self.Q)

            player = rn.randint(0,2) # Have me play first or second?
            if player == 0:
                g = Game(AIPlayer(self), AIPlayer(opp))
            else:
                g = Game(AIPlayer(opp), AIPlayer(self))

            trajectory, winner = g.play_game()

            idx = player
            trace = np.zeros(len(trajectory))
            trace[len(trajectory) - 1] = 1
            for j in range(len(trajectory) - 2, -1, -1):
                trace[j] = self.lambd * trace[j + 1]
                move = trajectory[j]
                s = move[0] + " " + str(move[idx + 1])
                print(self.Q)
                a = move[1 if idx == 0 else 3]

                if a not in self.Q[s]:
                    self.Q[s][a] = 0
                if winner == player:
                    av_return += 1
                    self.Q[s][a] += self.ep * (trace[j] - self.Q[s][a])
                elif winner == -1:
                    self.Q[s][a] += self.ep * (-self.Q[s][a])
                else:
                    av_return -= 1
                    self.Q[s][a] += self.ep * (-trace[j] - self.Q[s][a])
                idx = (idx + 1) % 2

            returns.append(av_return/i)

            opp = cached


    def choice_function(self, board, options):
        st = board.to_string() + " " + str(options)
        if st not in self.Q:
            self.Q[st] = {}
        if rn.rand() <= self.ep:
            return rn.choice(options)
        entry = self.Q[st]
        return max(entry, key=entry.get)

    def piece_function(self, board, piece):
        st = board.to_string() + " " + str(piece)
        if st not in self.Q:
            self.Q[st] = {}
            
        if rn.rand() <= self.ep:
            sq = board.open_squares
            return sq[rn.randint(0, len(sq))]
        entry = self.Q[st]
        return max(entry, key=entry.get)