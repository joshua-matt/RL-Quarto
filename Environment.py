from engine import *
from QuartoMDP import *
import matplotlib.pyplot as plt
agent = QuartoMDP(1.0,0.9)
plt.plot(list(range(1001)), agent.train_self_play(1000))