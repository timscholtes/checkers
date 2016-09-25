from checkers2 import *
from nn_methods import *

player1=query_player
player2=query_player


nnets = {1: generate_player_nn(),-1: generate_player_nn()}

checkers=checkers_class()
result1 = play_game(checkers,nnets,player1,player2,verbose=True)