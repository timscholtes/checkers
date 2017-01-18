from checkers2 import *
from nn_methods import *

player1=alphabeta_player
player2=alphabeta_player


nnets = {1: generate_player_nn(),-1: generate_player_nn()}

checkers=checkers_class()


#result1 = play_game(checkers,nnets,True,2,player1,player2)


def cull(scores,k):
	return np.argsort(scores)[::-1][range(k)]

print cull([1,2,3,4,5,6],6)