from engine import *
from QuartoMDP import *
import matplotlib.pyplot as plt
#mdp = MDP()
mdp = QuartoMDP(0.05, 0)
mdp.train_self_play(100)

p1, p2= HumanPlayer(), AIPlayer(MDP())
#p1, p2= AIPlayer(MDP()), AIPlayer(MDP())
#p1, p2 = HumanPlayer(), HumanPlayer()
game = Game(p1, p2)
game.play_game(verbose=True)

#plt.plot(list(range(1001)), agent.train_self_play(1000))