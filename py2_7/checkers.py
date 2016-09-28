## simple checkers program

import numpy as np
from collections import namedtuple
from itertools import cycle
from itertools import chain

def new_board_viz():
	odd_row      = ["r","."]*4
	even_row     = [".","r"]*4

	even_row_opp = [".","b"]*4
	odd_row_opp  = ["b","."]*4

	mid_row_even = [".","_"]*4
	mid_row_odd  = ["_","."]*4

	board = np.array(
		[odd_row,even_row,odd_row,
		mid_row_even,mid_row_odd,
		even_row_opp,odd_row_opp,even_row_opp])

	return board


### utilities
def forward_move_function(pos,turn):
	if turn == 1:
		if ((pos-1) // 4) % 2 == 0:
			if pos % 4 == 0:
				pos_dict = {'simp': [pos+4],
				'jump': [pos+7],
				'mid': [pos+4]}
			elif pos % 4 == 1:
				pos_dict = {'simp': [pos+4,pos+5],
				'jump': [pos+9],
				'mid': [pos+5]}
			else:
				pos_dict = {'simp': [pos+4,pos+5],
				'jump': [pos+7,pos+9],
				'mid': [pos+4,pos+5]}
		else:
			if pos % 4 == 0:
				pos_dict = {'simp': [pos+3,pos+4],
				'jump': [pos+7],
				'mid': [pos+3]}
			elif pos % 4 == 1:
				pos_dict = {'simp': [pos+4],
				'jump': [pos+9],
				'mid': [pos+4]}
			else:
				pos_dict = {'simp': [pos+3,pos+4],
				'jump': [pos+7,pos+9],
				'mid': [pos+3,pos+4]}
		## near end of board, no jumps or mids!
		if ((pos-1) // 4) == 6:
			if pos % 4 == 0:
				pos_dict = {'simp': [pos+4],
				'jump': [],
				'mid': []}
			elif pos % 4 == 1:
				pos_dict = {'simp': [pos+4,pos+5],
				'jump': [],
				'mid': []}
			else:
				pos_dict = {'simp': [pos+4,pos+5],
				'jump': [],
				'mid': []}

	if turn == -1:
		if ((pos-1) // 4) % 2 == 0:
			if pos % 4 == 0:
				pos_dict = {'simp': [pos-4],
				'jump': [pos-9],
				'mid': [pos-4]}
			elif pos % 4 == 1:
				pos_dict = {'simp': [pos-4,pos-3],
				'jump': [pos-7],
				'mid': [pos-3]}
			else:
				pos_dict = {'simp': [pos-4,pos-3],
				'jump': [pos-7,pos-9],
				'mid': [pos-4,pos-3]}
		else:
			if pos % 4 == 0:
				pos_dict = {'simp': [pos-5,pos-4],
				'jump': [pos-9],
				'mid': [pos-5]}
			elif pos % 4 == 1:
				pos_dict = {'simp': [pos-4],
				'jump': [pos-7],
				'mid': [pos-4]}
			else:
				pos_dict = {'simp': [pos-5,pos-4],
				'jump': [pos-9,pos-7],
				'mid': [pos-5,pos-4]}
		## near end of board, no jumps or mids!
		if ((pos-1) // 4) == 1:
			if pos % 4 == 0:
				pos_dict = {'simp': [pos-5,pos-4],
				'jump': [],
				'mid': []}
			elif pos % 4 == 1:
				pos_dict = {'simp': [pos-4],
				'jump': [],
				'mid': []}
			else:
				pos_dict = {'simp': [pos-5,pos-4],
				'jump': [],
				'mid': []}
	
	return pos_dict

class State(object):
 	
	RED   = 1
	WHITE = -1
	KINGS_ROW  = {RED: list(range(29, 33)),WHITE: list(range(1, 5))}
	
	def __init__(self,turn,board,jump_location,K):
		
		self.turn=turn
		self.board=board
		self.jump_location=jump_location
		self.K = K
		
		self.opponent = self.WHITE if turn == self.RED else self.RED
		
		# build a dict of legal forward steps for each position.
		self.forward_move_dict = {value: forward_move_function(value,self.turn) for value in list(range(1,33))}
		self.back_move_dict = {value: forward_move_function(value,self.opponent) for value in list(range(1,33))}
		self.both_move_dict = [val for sublist in [self.forward_move_dict,self.back_move_dict] for val in sublist]

		# where are the blank, primary and opponent pieces?
		self.empties = [i for i in list(range(1,33)) if self.board[i-1] == 0]
		self.opponent_pos = [i for i in list(range(1,33)) if np.sign(self.board[i-1]) == np.sign(self.opponent)]
		self.primary_pos = [i for i in list(range(1,33)) if np.sign(self.board[i-1]) == np.sign(self.turn)]
		

	def available_moves(self,player):
		"""Here  we evaluate all of the available moves to the player, simple moves and jumps separately.
		This is useful later on as we expect the computer to search over all available moves, so it is faster to
		have a list of them rather than search all pieces and check for legality."""
		opponent_temp = -player
		if self.jump_location is None:
			available_simp = dict()
			available_jump = dict()
			for pos in self.primary_pos:
				if self.board[pos-1] == self.K*player:
					X = self.both_move_dict[pos]
				else:
					X = self.forward_move_dict[pos]
				# evaluate the simple moves (requiring forward empty space)
				pos_simps = [i for i in X['simp'] if self.board[i-1] ==0]
				# for jump, there needs to be empty space to jump into AND an opposition piece in the same simp. space
				pos_jumps = [X['jump'][i] for i in range(len(X['jump'])) if self.board[X['jump'][i]-1] ==0 and np.sign(self.board[X['simp'][i]-1]) == np.sign(opponent_temp)]
				
				if len(pos_simps)>0:
					available_simp[pos] = pos_simps
				if len(pos_jumps)>0:
					available_jump[pos] = pos_jumps
			return {'jumps': available_jump,'simps': available_simp}
		else:
			available_simp = dict()
			available_jump = dict()
			if self.board[self.jump_location-1] == self.K*player:
				X = self.both_move_dict[self.jump_location]
			else:
				X = self.forward_move_dict[self.jump_location]
			
			# for jump, there needs to be empty space to jump into AND an opposition piece in the same simp. space
			
			pos_jumps = [X['jump'][i] for i in range(len(X['jump'])) if self.board[X['jump'][i]-1] ==0 and np.sign(self.board[X['simp'][i]-1]) == np.sign(opponent_temp)]

			if len(pos_jumps)>0:
				available_jump[self.jump_location] = pos_jumps
			return {'jumps': available_jump,'simps': available_simp}
	
	def move(self,move):
		# the move must be a list of length two - starting position and ending position.
		available = self.available_moves(self.turn)
		
		#1. check the move is one of required jumps
		if len(available['jumps'])>0:
			available = available['jumps']
			move_type = 'jump'
		else:
			available = available['simps']
			move_type = 'simp'

		check1 = move[0] in list(available.keys())
		check2 = move[1] in available[move[0]]
		
		if not (check1 and check2):
			raise ValueError("Not Legal")
		else:
			print("Legal")

		if move_type == 'simp':
			self.board[move[1]-1] = self.board[move[0]-1]
			self.board[move[0]-1] = 0
			if move[1] in self.KINGS_ROW[self.turn]:
				print('promoting ', move[1], 'to King')
				self.board[move[1]-1] = self.turn*self.K
			return State(self.opponent, self.board,None,self.K)

		if move_type == 'jump':
			# make the move
			self.board[move[1]-1] = self.board[move[0]-1]
			self.board[move[0]-1] = 0
			# identify the captured piece, remove from play
			jumped = (self.forward_move_dict[move[0]]['mid'])[self.forward_move_dict[move[0]]['jump'].index(move[1])]
			self.board[jumped-1] = 0
			print(jumped, 'has been captured')
			
			# if it's made to the kings row, turn into a king
			if move[1] in self.KINGS_ROW[self.turn]:
				print('promoting ', move[1], 'to King')
				self.board[move[1]-1] = self.turn*self.K
				return State(self.opponent, self.board,None,self.K)

			# input jump_location and check for more jumps
			self.jump_location = move[1]
			print('only can move current piece: jump location set to ',self.jump_location)
			available = self.available_moves(self.turn)['jumps']
			if move[1] in list(available.keys()):
				return State(self.turn, self.board,move[1],self.K)
			else:
				return State(self.opponent, self.board,None,self.K)

	def loss_check(self,player):
		""" if the player has no pieces left or no available moves then they lose.
		we check for loss on each player to decide if the game is over"""
		pieces_left = [i for i in list(range(1,33)) if np.sign(self.board[i-1]) == np.sign(player)]
		no_pieces = len(pieces_left)==0

		available = self.available_moves(player)
		no_moves = len(available['jumps'])==0 and len(available['simps'])==0
		return (no_moves or no_pieces)

def rank(s):
    """Return the rank of the given squares. Counting starts from zero."""
    return ((s-1)//4)

def play_checkers():
	start_board = [val for sublist in [[1]*12,[0]*8,[-1]*12] for val in sublist]
	state = State(State.RED,start_board,None,2)

	player = state.turn
	in_play = True
	play_count = 0

	while in_play and play_count < 40:
		player = state.turn
		player_colour = "Red" if player == 1 else "White"

		print_board(state)
		print("Current Player: ",player_colour)
		print("These are the legal moves:", state.available_moves(player))
		
		input_move = [int(x) for x in input("Input your move as X Y (space): ").split()]
		state = state.move(input_move)
		in_play = not state.loss_check(player)
		in_play = not state.loss_check(-player)
		play_count += 1
	else:
		player1 = state.loss_check(1)
		player2 = state.loss_check(-1)
		print('Red wins' if player2 else 'White wins')
		print(state['board'])

def print_board(state, upper_color=State.RED):
    """Print the given state to the user as a board."""
    line = []
    # the first squares should be the upper ones.
    squares = [s for s in range(1, 33)]
    # zip(*[iterator]*n) clusters the iterator elements into n-length groups.
    rows = zip(*[iter(squares)]*4)
    for row in rows:
        for square in row:
            player_ch = ('r' if  np.sign(state.board[square-1])==1
                         else 'w' if np.sign(state.board[square-1])==-1 else '.')
            char = player_ch.upper() if abs(state.board[square-1]) == state.K else player_ch
            # == is used as an XNOR operator here
            if (rank(square) % 2 == 0):
                line.append('   {}'.format(char))
            else:
                line.append(' {}  '.format(char))
        line.append('	')
        for square in row:
            if (rank(square) % 2 == 0):
                line.append('   {0:02d}'.format(square))
            else:
                line.append(' {0:02d}  '.format(square))
        print(''.join(line))
        line = []

# start the board with +1's for the first player, -1's for second player, 0 for empty spots 
# (+K for first player Kings, -K for second player Kings)
start_board = [val for sublist in [[1]*12,[0]*8,[-1]*12] for val in sublist]
#start_board = [val for sublist in [[1]*12,[-1]*4,[0]*4,[-1]*4,[0]*8] for val in sublist]


#START = State(State.RED, start_board,None,2)
#print(START.forward_move_dict)
#print_board(START)

#print(START.available_moves(START.turn))

#moved = START.move([10,14])

#print_board(moved)


########

play_checkers()