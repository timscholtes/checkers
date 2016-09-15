## build a tournament
from nn_methods import *
import random
from checkers2 import *
import json
def generate_schedule(N_players,N_opponents):
	return {i: random.sample([x for x in range(N_players) if x!=i],N_opponents) for i in range(N_players)}

def generate_scoreboard(N_players):
	return {i: 0 for i in range(N_players)}



def play_tournament(schedule,players):
	score = generate_scoreboard(len(players))
	checkers=checkers_class()
	player1=alphabeta_player
	player2=alphabeta_player
	game_counter=0
	total_games = len(schedule)*len(schedule[0])
	for p1,opp_list in schedule.items():
		for p2 in opp_list:
			game_counter+= 1
			print('Game: ',game_counter,' out of ',total_games,': ',p1,' vs ',p2)
			nnets = {1: players[p1],-1: players[p2]}
			start_time = time.clock()
			outcome = play_game(checkers,nnets,player1,player2)
			end_time = time.clock()
			score[p1] += outcome[0]
			score[p2] += outcome[1]
			print(outcome)
			print(end_time-start_time)

	return score

gen1 = regeneration(N_players=15)
schedule1 = generate_schedule(15,5)

X = play_tournament(schedule=schedule1,players=gen1)
print(X)

with open('data/tournament_scores.txt', 'w') as f:
    json.dump(X,f)