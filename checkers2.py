""" rewrite of the first version, checkers.py, so we have a more logical structure to play.
This will allow for computerised players to play, and for minimax algo's to function well"""

from games import *
import numpy as np

def rank(s):
    """Return the rank of the given squares. Counting starts from zero."""
    return ((s-1)//4)

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
        if ((pos-1) // 4) == 7:
            pos_dict = {'simp': [],
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
        if ((pos-1) // 4) == 0:
            pos_dict = {'simp': [],
            'jump': [],
            'mid': []}
           
    
    return pos_dict


class state_class(object):

    def __init__(self,board,turn,jump_loc):
        self.board=board
        self.jump_loc=jump_loc
        self.turn=turn


class checkers_class(Game):

    RED = 1
    WHITE = -1
    KINGS_ROW  = {RED: list(range(29, 33)),WHITE: list(range(1, 5))}
    
    def __init__(self):
        self.forward_move_dict = {value: forward_move_function(value,1) for value in list(range(1,33))}
        self.back_move_dict = {value: forward_move_function(value,-1) for value in list(range(1,33))}
        self.both_move_dict = copy.deepcopy(self.forward_move_dict)

        for key,value in self.both_move_dict.items():
            [self.both_move_dict[key]['jump'].append(i) for i in self.back_move_dict[key]['jump']]
            [self.both_move_dict[key]['simp'].append(i) for i in self.back_move_dict[key]['simp']]
            [self.both_move_dict[key]['mid'].append(i) for i in self.back_move_dict[key]['mid']]

        self.K = 2

        self.initial = state_class(
            board=[val for sublist in [[1]*12,[0]*8,[-1]*12] for val in sublist],
            turn=1,
            jump_loc=None)

    def available_jumps(self,move_dict,state):
        X = [move_dict['jump'][i] for i in range(len(move_dict['jump'])) if
         state.board[move_dict['jump'][i]-1] ==0 and
          np.sign(state.board[move_dict['mid'][i]-1]) == np.sign(state.turn*-1)]
        return X

    def legal_moves(self,state):
        opponent_temp = -state.turn
        primary_pos = [i for i in list(range(1,33)) if np.sign(state.board[i-1]) == np.sign(state.turn)]
        
        available = []
        if state.jump_loc is None:
            # if any jumps are found for any positions, then it will not evaluate any possible simple moves.
            # Declared as False, outside the loop. The first time a jump is found, it will revert to True
            # meaning simps will not be evaluated.
            jumpables=False
            for pos in primary_pos:
                if state.board[pos-1] == self.K*state.turn:
                    X = self.both_move_dict[pos]
                elif state.turn == 1:
                    X = self.forward_move_dict[pos]
                else:
                    X = self.back_move_dict[pos]
                # for jump, there needs to be empty space to jump into AND an opposition piece in the same simp. space
                pos_jumps = self.available_jumps(move_dict=X,state=state)
                
                if len(pos_jumps)>0:
                    for i in pos_jumps:
                        available.append([pos,i])
                    jumpables = True
                elif not jumpables:
                    # evaluate the simple moves (requiring forward empty space)
                    pos_simps = [i for i in X['simp'] if state.board[i-1] ==0]
                    if len(pos_simps)>0:
                        for i in pos_simps:
                            available.append([pos,i])
            return available

        else:
            if state.board[state.jump_loc-1] == self.K*state.turn:
                X = self.both_move_dict[state.jump_loc]
            elif state.turn == 1:
                X = self.forward_move_dict[state.jump_loc]
            else:
                X = self.back_move_dict[state.jump_loc]
            # for jump, there needs to be empty space to jump into AND an opposition piece in the same simp. space
            pos_jumps = self.available_jumps(move_dict=X,state=state)
            if len(pos_jumps)>0:
                for i in pos_jumps:
                            available.append([state.jump_loc,i])
            return available

    def movables(self,moves):
        [i[0] for i in moves]

    def make_jump(self,board,turn,move):
        # get the pairs of mids and jumps
        if board[move[0]-1] == self.K*turn:
            move_dict = self.both_move_dict[move[0]]
        elif turn == 1:
            move_dict = self.forward_move_dict[move[0]]
        else:
            move_dict = self.back_move_dict[move[0]]
        # make the move
        board[move[1]-1] = board[move[0]-1]
        board[move[0]-1] = 0
        # identify the captured piece, remove from play
        jumped = (move_dict['mid'])[move_dict['jump'].index(move[1])]
        board[jumped-1] = 0
        
        new_state=state_class(
            board= board,turn=turn,
            jump_loc=move[1])
        return new_state


    def make_move(self,move,state):
        # the move must be a list of length two - starting position and ending position.
        #classify move type
        move_type = 'jump' if abs(move[0]-move[1])>5 else 'simp'

        board = state.board.copy()

        if move_type == 'simp':
            board[move[1]-1] = board[move[0]-1]
            board[move[0]-1] = 0
            if move[1] in self.KINGS_ROW[state.turn]:
                print('promoting ', move[1], 'to King')
                board[move[1]-1] = state.turn*self.K
            return state_class(board=board,turn=state.turn*-1,jump_loc=None)

        if move_type == 'jump':
            new_state = self.make_jump(board,state.turn,move)

                    # if it's made to the kings row, turn into a king, hand over control
            if move[1] in self.KINGS_ROW[state.turn]:
                print('promoting ', move[1], 'to King')
                board[move[1]-1] = state.turn*self.K
                return state_class(board=board,turn=state.turn*-1,jump_loc=None)
            available = self.legal_moves(new_state)

            # if there's only 1 available jump, then keep running it until there's either 0 or more than 1.
            if len(available)==1:
                in_jump=True
                while not len(available)==0:
                    new_move = available[0]
                    print("Chaining move: ",new_move)
                    new_state = self.make_jump(new_state.board,new_state.turn,new_move)
                    available = self.legal_moves(new_state)
                    in_jump = not len(available)==0
                    print(in_jump)
                else:
                    if len(available)==0:
                        return state_class(board= new_state.board,turn=state.turn*-1,jump_loc=None)
                    else:
                        return state_class(board= new_state.board,turn=state.turn,jump_loc=new_move[1])
            elif len(available)==0:
                return state_class(board= new_state.board,turn=state.turn*-1,jump_loc=None)
            else:
                return state_class(board= new_state.board,turn=state.turn,jump_loc=move[1])


    def successors(self,state):
        return [(move, self.make_move(move, state)) for move in self.legal_moves(state)]
    
    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        pieces_left = all(np.sign(i) == 1 for i in state.board) or all(np.sign(i) == -1 for i in state.board)
        no_moves = len(self.legal_moves(state))==0
        return no_moves or pieces_left



    def print_board(self,state):
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
                char = player_ch.upper() if abs(state.board[square-1]) == self.K else player_ch
                # == is used as an XNOR operator here
                if (rank(square) % 2 == 0):
                    line.append('   {}'.format(char))
                else:
                    line.append(' {}  '.format(char))
            line.append('   ')
            for square in row:
                if (rank(square) % 2 == 0):
                    line.append('   {0:02d}'.format(square))
                else:
                    line.append(' {0:02d}  '.format(square))
            print(''.join(line))
            line = []

    def utility(self,state,player):
        pieces_left = [i for i in list(range(1,33)) if np.sign(state.board[i-1]) == np.sign(player)]
        no_pieces = len(pieces_left)==0

        available = self.legal_moves(state)
        no_moves = len(available)==0
        return (no_moves or no_pieces)



checkers=checkers_class()

####

def play_game(game, *players):
    "Play an n-person, move-alternating game."
    state = game.initial
    counter = 0
    while counter<100:
        print(counter)
        for player in players:
            move = player(game=game, state=state,eval_fun_dict=eval_fun_dict)
            state = game.make_move(move, state)
            print('making move: ', move)
            game.print_board(state)
            if game.terminal_test(state):
                game.print_board(state)
                return game.utility(state_class(state.board,turn=1,jump_loc=None), 1)
        counter += 1
    else:
        return 0

def random_player(game, state):
    "A player that chooses a legal move at random."
    print('legal moves: ',game.legal_moves(state))
    return random.choice(game.legal_moves(state))

"""
player1 = random_player
player2 = random_player

result = play_game(checkers,player1,player2)
print(result)

"""#################

def alphabeta_search(state, game, eval_fun_dict, d=4, cutoff_test=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = state.turn  #game.to_move(state)
    eval_fn = eval_fun_dict[player]

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state,game)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state,game)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    #eval_fn = eval_fn #or (lambda state: game.utility(state, player))
    #action, state = argmax(game.successors(state),
    #                       lambda a, s: min_value(s, -infinity, infinity, 0))
    states  = [i[1] for i in game.successors(state)]
    actions = [i[0] for i in game.successors(state)]
    Z = argmax(states,lambda s: min_value(s, -infinity, infinity, 0))

    action=actions[Z]

    return action

############
import numpy as np
import time
######
def predict(model, x):
    x = np.append(x,1)
    W1, W2, W3 = model['W1'], model['W2'], model['W3']
    # Forward propagation
    z1 = np.dot(W1,x)
    a1 = np.tanh(z1)
    z2 = np.dot(W2,np.append(a1,1))
    a2 = np.tanh(z2)
    z3 = np.dot(W3,np.append(a2,1))
    a3 = np.tanh(z3)
    return a3
######
N_hl_1 = 40
N_hl_2 = 10
k = 32


W1 = np.empty((0, k+1)) # 33 because we want the bias term too!

for line in range(1,N_hl_1+1):
    W1 = np.append(W1, [2*np.random.random(k+1)-1], axis=0)

W2 = np.empty((0, N_hl_1+1)) # 41 because we want the bias term too!
for line in range(1,N_hl_2+1):
    W2 = np.append(W2, [2*np.random.random(N_hl_1+1)-1], axis=0)

W3 = np.array([2*np.random.random(N_hl_2+1)-1])

mod1 = {'W1': W1,'W2': W2,'W3': W3}


W1 = np.empty((0, k+1)) # 33 because we want the bias term too!

for line in range(1,N_hl_1+1):
    W1 = np.append(W1, [2*np.random.random(k+1)-1], axis=0)

W2 = np.empty((0, N_hl_1+1)) # 41 because we want the bias term too!
for line in range(1,N_hl_2+1):
    W2 = np.append(W2, [2*np.random.random(N_hl_1+1)-1], axis=0)

W3 = np.array([2*np.random.random(N_hl_2+1)-1])

mod2 = {'W1': W1,'W2': W2,'W3': W3}

def eval_fn1(x,game):
    if game.terminal_test(x):
        return game.utility(x,player=state.turn)
    else:
        return predict(mod1,x.board)
def eval_fn2(x,game):
    if game.terminal_test(x):
        return game.utility(x,player=state.turn)
    else:
        return predict(mod1,x.board)

eval_fun_dict = {1: eval_fn1, -1: eval_fn2}


def alphabeta_player(game, state,eval_fun_dict):
    return alphabeta_search(state, game,eval_fun_dict,d=3)

player1=alphabeta_player
player2=alphabeta_player

#X = checkers.successors(checkers.initial)
#Y = [i[1] for i in X]
#print(Y)

result = play_game(checkers,player1,player2)
