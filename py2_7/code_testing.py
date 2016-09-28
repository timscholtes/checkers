from checkers2 import *
from nn_methods import *

player1=alphabeta_player
player2=alphabeta_player


nnets = {1: generate_player_nn(),-1: generate_player_nn()}

checkers=checkers_class()
result1 = play_game(checkers,nnets,True,2,player1,player2)

W1 = np.load('data/top_player/W1.npy')
W2 = np.load('data/top_player/W2.npy')
W3 = np.load('data/top_player/W3.npy')
W4 = np.load('data/top_player/W4.npy')
