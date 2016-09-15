from checkers2 import *

checkers=checkers_class()


player1=random_player
player2=alphabeta_player




nnets = {1: generate_player_nn(),-1: generate_player_nn()}
print(nnets[1]['W4'])
print(nnets[-1]['W4'])
checkers=checkers_class()
start_time = time.clock()
result1 = play_game(checkers,nnets,player1,player2,verbose=True,d=5)
end_time = time.clock()
print(end_time-start_time)