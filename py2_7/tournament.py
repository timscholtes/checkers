## build a tournament
from nn_methods import *
import random
from checkers2 import *
import json
import multiprocessing as mp
import os
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
		scores.append(play_game(checkers,nnets,verbose,d,player1,player2))
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
	outcome = play_game(game,nnets,False,d,player1,player2)
	return outcome

def reconcile_scores(schedule,scores,N_players):
	rec_scores = [0 for i in range(N_players)]
	for i in range(len(scores)):
		rec_scores[schedule[i][0]] += scores[i][0]
		rec_scores[schedule[i][1]] += scores[i][1]
	return rec_scores


def play_parallel_tourn(schedule,players,num_cores,d):
	checkers=checkers_class()
	player1=alphabeta_player
	player2=alphabeta_player
	game_counter=0
	total_games = len(schedule)
	inputs = [(checkers,m,players,d) for m in schedule]
	pool = mp.Pool(processes=num_cores)
	scores = pool.map(setup_play_game,inputs)
	pool.close()
	pool.join()
	rec_scores = reconcile_scores(schedule,scores,len(players))
	return(rec_scores)



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

def parallel_evolve(N_gen,N_players,matches_per_player,carry_forward,sigma,d,num_cores,verbose):
	gen_counter = 1
	spawn_ratio = int(N_players / carry_forward)
	while gen_counter <= N_gen:
		print("Running generation ",gen_counter)
		print(time.time())
		if gen_counter == 1:
			prev_gen = None
		else:
			prev_gen = {i: gen[i] for i in prev_gen} 
		gen = regeneration(prev_gen=prev_gen,N_players=N_players,sigma=sigma,spawn_ratio = spawn_ratio)
		schedule = generate_schedule(N_players,matches_per_player)
		scores = play_parallel_tourn(schedule=schedule,players=gen,num_cores=num_cores,d=d)
		prev_gen = list(cull(scores,carry_forward))
		if gen_counter % 10 == 0:
			top_player = gen[list(cull(scores,1))[0]]
			directory = 'data/gen'+str(gen_counter)+'/'
			if not os.path.exists(directory):
				os.makedirs(directory)
			np.save('data/gen'+str(gen_counter)+'/W1.npy',top_player['W1'])
			np.save('data/gen'+str(gen_counter)+'/W2.npy',top_player['W2'])
			np.save('data/gen'+str(gen_counter)+'/W3.npy',top_player['W3'])
			np.save('data/gen'+str(gen_counter)+'/W4.npy',top_player['W4'])

		gen_counter += 1


	top_player = gen[list(cull(scores,1))[0]]

	#with open('data/top_player.txt', 'w') as f:
	#	json.dump(top_player,f)

	np.save('data/top_player/W1.npy',top_player['W1'])
	np.save('data/top_player/W2.npy',top_player['W2'])
	np.save('data/top_player/W3.npy',top_player['W3'])
	np.save('data/top_player/W4.npy',top_player['W4'])

	return top_player

num_cores = mp.cpu_count()

start_time = time.time()
print('starting at:',start_time)
X = parallel_evolve(
	N_gen=250,
	N_players=32,
	matches_per_player=5,
	carry_forward=1,
	sigma=0.05,
	d=2,
	num_cores=num_cores,
	verbose=False)

end_time = time.time()
print('ending at:',end_time)
print(end_time-start_time)
"""
gen1 = regeneration(N_players=3)
schedule1 = generate_schedule(3,1)"""
"""tourn_start = time.time()
A = play_tournament(schedule=schedule1,players=gen1,d=1,verbose=False)
tourn_end = time.time()
""""""
tourn_start2 = time.time()
B = play_parallel_tourn(schedule=schedule1,players=gen1,num_cores=4,d=1)
tourn_end2 = time.time()

print(tourn_end2-tourn_start2)
print(B)
"""
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