## build a tournament
from nn_methods import *
import random
from checkers2 import *
import json
import multiprocessing as mp
def generate_schedule(N_players,N_opponents):
	X = {i: random.sample([x for x in range(N_players) if x!=i],N_opponents) for i in range(N_players)}
	games_list = []
	for p1,opp_list in X.items():
		for p2 in opp_list:
			flip = random.random()
		# randomise start order
			if flip<0.5:
				Y = [p1,p2]
			else:
				Y = [p2,p1]
			games_list.append(Y)
	return games_list

def generate_scoreboard(N_players):
	return [0 for i in range(N_players)]



def play_tournament(schedule,players,d,verbose):
	score = generate_scoreboard(len(players))
	checkers=checkers_class()
	player1=alphabeta_player
	player2=alphabeta_player
	game_counter=0
	total_games = len(schedule)
	scores = []
	for match in schedule:
		p1 = match[0]
		p2 = match[1]
		game_counter+= 1
		if verbose:
			print('Game: ',game_counter,' out of ',total_games,': ',p1,' vs ',p2)
		nnets = {1: players[p1],-1: players[p2]}
		scores.append(play_game(checkers,nnets,player1,player2,d=d,verbose=verbose))
		#score[p1] += outcome[0]
		#score[p2] += outcome[1]
		if verbose:
			print(outcome)
	return scores

def setup_play_game(input_list):
	game=input_list[0]
	match=input_list[1]
	players=input_list[2]
	d=input_list[3]
	p1 = match[0]
	p2 = match[1]
	player1=alphabeta_player
	player2=alphabeta_player
	nnets = {1: players[p1],-1: players[p2]}
	outcome = play_game(game,nnets,player1,player2,d=d,verbose=False)
	return outcome

def play_parallel_tourn(schedule,players,num_cores,d):
	score = generate_scoreboard(len(players))
	checkers=checkers_class()
	player1=alphabeta_player
	player2=alphabeta_player
	game_counter=0
	total_games = len(schedule)
	inputs = [(checkers,m,players,d) for m in schedule]
	pool = mp.Pool(processes=num_cores)
	scores = pool.map(setup_play_game,inputs)
	return(scores)



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


#X = evolve(1,9,2,3,0.05,1)


gen1 = regeneration(N_players=30)
schedule1 = generate_schedule(30,5)
"""tourn_start = time.time()
A = play_tournament(schedule=schedule1,players=gen1,d=1,verbose=False)
tourn_end = time.time()
"""
tourn_start2 = time.time()
B = play_parallel_tourn(schedule=schedule1,players=gen1,num_cores=4,d=4)
tourn_end2 = time.time()

print(tourn_end2-tourn_start2)
print(B)


"""
result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def apply_async_with_callback(schedule,players,num_cores,d):
	score = generate_scoreboard(len(players))
	checkers=checkers_class()
	player1=alphabeta_player
	player2=alphabeta_player
	game_counter=0
	total_games = len(schedule)
	inputs = [(checkers,m,players,d) for m in schedule]
	pool = mp.Pool(processes=num_cores)
	#scores = pool.map(setup_play_game,inputs)

	#pool = mp.Pool()
	for i in inputs:
		pool.apply_async(setup_play_game, args = (i, ), callback = log_result)
	pool.close()
	pool.join()
	print(result_list)



tourn_start2 = time.time()
C = apply_async_with_callback(schedule=schedule1,players=gen1,num_cores=4,d=1)
tourn_end2 = time.time()

print(tourn_end2-tourn_start2)
print(C)

"""