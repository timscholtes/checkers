## build a tournament
from nn_methods import *
import random
from checkers2 import *
import json
def generate_schedule(N_players,N_opponents):
	return {i: random.sample([x for x in range(N_players) if x!=i],N_opponents) for i in range(N_players)}

def generate_scoreboard(N_players):
	return [0 for i in range(N_players)]



def play_tournament(schedule,players,d,verbose):
	score = generate_scoreboard(len(players))
	checkers=checkers_class()
	player1=alphabeta_player
	player2=alphabeta_player
	game_counter=0
	total_games = len(schedule)*len(schedule[0])
	for p1,opp_list in schedule.items():
		for p2 in opp_list:
			game_counter+= 1
			if verbose:
				print('Game: ',game_counter,' out of ',total_games,': ',p1,' vs ',p2)
			nnets = {1: players[p1],-1: players[p2]}
			start_time = time.clock()
			flip = random.random()
			# randomise start order
			if flip<0.5:
				outcome = play_game(checkers,nnets,player1,player2,d=d,verbose=verbose)
			else:
				outcome = play_game(checkers,nnets,player2,player1,d=d,verbose=verbose)
			end_time = time.clock()
			score[p1] += outcome[0]
			score[p2] += outcome[1]
			if verbose:
				print(outcome)
				print(end_time-start_time)

	return score

def cull(scores,k):
	return np.argsort(scores)[::-1][range(k)]

def log_progress():
	pass

def evolve(N_gen,N_players,matches_per_player,carry_forward,sigma,d,verbose=False):
	gen_counter = 1
	while gen_counter <= N_gen:
		print("Running generation ",gen_counter)
		if gen_counter == 1:
			prev_gen = None
		else:
			prev_gen = {i: gen[i] for i in prev_gen} 
		gen = regeneration(prev_gen=prev_gen,N_players=N_players,sigma=sigma)
		schedule = generate_schedule(N_players,matches_per_player)
		scores = play_tournament(schedule=schedule,players=gen,verbose=verbose,d=d)
		prev_gen = list(cull(scores,carry_forward))
		gen_counter += 1

	top_player = gen[list(cull(scores,1))[0]]

	#with open('data/top_player.txt', 'w') as f:
	#	json.dump(top_player,f)

	np.save('data/top_player/W1.npy',top_player['W1'])
	np.save('data/top_player/W2.npy',top_player['W2'])
	np.save('data/top_player/W3.npy',top_player['W3'])
	np.save('data/top_player/W4.npy',top_player['W4'])

	return top_player


X = evolve(1,9,2,3,0.05,1)



"""
gen1 = regeneration(N_players=15)
schedule1 = generate_schedule(15,5)
tourn_start = time.clock()
X = play_tournament(schedule=schedule1,players=gen1,d=1)
tourn_end = time.clock()
"""





