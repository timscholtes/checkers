""" rewrite of the first version, checkers.py, so we have a more logical structure to play.
This will allow for computerised players to play, and for minimax algo's to function well"""

from games import *
import numpy as np
import time
from nn_methods import *

######
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
        opponent_temp = state.turn * -1
        primary_pos = [i for i in list(range(1,33)) if np.sign(state.board[i-1]) == np.sign(state.turn)]
        
        available = []
        if state.jump_loc is None:
            avail_jumps = []
            avail_simps = []
            # if any jumps are found for any positions, then it will not evaluate any possible simple moves.
            jumpables = False
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
                        avail_jumps.append([pos,i])
                else:
                    # evaluate the simple moves (requiring forward empty space)
                    pos_simps = [i for i in X['simp'] if state.board[i-1] ==0]
                    if len(pos_simps)>0:
                        for i in pos_simps:
                            avail_simps.append([pos,i])
            if len(avail_jumps)==0:
                available = avail_simps
            else:
                available = avail_jumps
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
               # print('promoting ', move[1], 'to King')
                board[move[1]-1] = state.turn*self.K
            return state_class(board=board,turn=state.turn*-1,jump_loc=None)

        if move_type == 'jump':
            new_state = self.make_jump(board,state.turn,move)

                    # if it's made to the kings row, turn into a king, hand over control
            if move[1] in self.KINGS_ROW[state.turn]:
                #print('promoting ', move[1], 'to King')
                board[move[1]-1] = state.turn*self.K
                return state_class(board=board,turn=state.turn*-1,jump_loc=None)
            available = self.legal_moves(new_state)

            # if there's only 1 available jump, then keep running it until there's either 0 or more than 1.
            if len(available)==1:
                in_jump=True
                while not len(available)==0:
                    new_move = available[0]
                    #print("Chaining move: ",new_move)
                    new_state = self.make_jump(new_state.board,new_state.turn,new_move)
                    available = self.legal_moves(new_state)
                    in_jump = not len(available)==0
                    #print(in_jump)
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
        state2 = state_class(state.board,jump_loc=None,turn=state.turn*-1)
        no_moves2 = len(self.legal_moves(state2)) == 0
    
        return no_moves or pieces_left or no_moves2



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
        output_utility = -1 if (no_moves or no_pieces) else 1
        return output_utility

####

def eval_fn(x,game,nn):
    if game.terminal_test(x):
        return game.utility(x,player=x.turn)
    else:
        return predict_nn2(nn,x.board,x.turn)

def alphabeta_search(state, game, eval_fn,nnets, d=3, cutoff_test=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = state.turn  #game.to_move(state)
    nn = nnets[player]

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state,game,nn)
        v = -infinity
        GS = game.successors(state)
        for (a, s) in GS:
            if len(GS[0]) == 0:
                v = max(v, min_value(s, alpha, beta, depth))
            else:
                v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state,game,nn)
        v = infinity
        GS = game.successors(state)
        for (a, s) in GS:
            if len(GS[0]) == 0:
                v = min(v, max_value(s, alpha, beta, depth))
            else:
                v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    states  = [i[1] for i in game.successors(state)]
    actions = [i[0] for i in game.successors(state)]
    # if there's only 1 available action, just take it
    if len(actions) == 0:
        action=actions[0]
    else:
        Z = argmax(states,lambda s: min_value(s, -infinity, infinity, 0))
        action=actions[Z]
    return action

def alphabeta_player(game, state,eval_fn,nnets,d=3):
    return alphabeta_search(state, game,eval_fn,nnets,d=d)

def random_player(game, state,*extra):
    "A player that chooses a legal move at random."
    return random.choice(game.legal_moves(state))

def query_player(game, state,*extra):
    "Make a move by querying standard input."
    a = [int(x) for x in input('Your move? ').split()]
    return(a)

def play_game(game,nnets, *players,verbose=False,d=3):
    "Play an n-person, move-alternating game."
    state = game.initial
    counter = 0
    move_store = []
    while counter<200:
        for player in players:
            if verbose:
                print(counter)
                game.print_board(state)
            if verbose:
                print('legal moves: ', game.legal_moves(state))
            move = player(game, state,eval_fn,nnets,d)
            if verbose:
                print('turn: ',state.turn)
                print('making move: ',move)
            state = game.make_move(move, state)
            np.append(move_store,move)
            move_store[len(move_store):] = [move]
            #print('making move: ', move)

            #check if the same series of moves has been played over:
            if counter>20:
                repeat_check = [move_store[counter-i][1] == move_store[counter-i-4][1] and
                 move_store[counter-i][0] == move_store[counter-i-4][0] for i in range(4)]
                if all(repeat_check):
                    if verbose:
                        print('stuck in a loop')
                        game.print_board(state)
                    return [0,0]
            if game.terminal_test(state):
                if verbose:
                    print(counter)
                    game.print_board(state)
                return [game.utility(state_class(state.board,turn=1,jump_loc=None), 1),
                game.utility(state_class(state.board,turn=-1,jump_loc=None), -1)]
            counter += 1
    else:
        if verbose:
            game.print_board(state)
        return [0,0]


def play_game_from_state(game,state,nnets, *players,verbose=False,d=3):
    "Play an n-person, move-alternating game."
    counter = 0
    move_store = []
    if state.turn==-1:
        players = players[::-1]
    while counter<200:
        for player in players:
            move = player(game, state,eval_fn,nnets,d)
            state = game.make_move(move, state)
            np.append(move_store,move)
            move_store[len(move_store):] = [move]
            #print('making move: ', move)
            if verbose:
                print(counter)
                game.print_board(state)
                print('p1 thinks: ',eval_fn(state,game,nnets[1]))
                print('p2 thinks: ',eval_fn(state,game,nnets[-1]))
            #check if the same series of moves has been played over:
            if counter>20:
                repeat_check = [move_store[counter-i][1] == move_store[counter-i-4][1] and
                 move_store[counter-i][0] == move_store[counter-i-4][0] for i in range(4)]
                if all(repeat_check):
                    print('stuck in a loop')
                    game.print_board(state)
                    return [0,0]
            if game.terminal_test(state):
                print(counter)
                game.print_board(state)
                return [game.utility(state_class(state.board,turn=1,jump_loc=None), 1),
                game.utility(state_class(state.board,turn=-1,jump_loc=None), -1)]
            counter += 1
    else:
        game.print_board(state)
        return [0,0]

#################

"""
player1=alphabeta_player
player2=alphabeta_player
#player1=random_player
#player2=random_player


nnets = {1: generate_player_nn(),-1: generate_player_nn()}

checkers=checkers_class()
result1 = play_game(checkers,nnets,player1,player2)
#result2 = play_game2(checkers,nnets,player1,player2)
"""