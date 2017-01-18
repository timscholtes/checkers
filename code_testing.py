from checkers2 import *
from nn_methods import *

player1=alphabeta_player
player2=alphabeta_player

W1 = np.load('gcp_results/checkers-144720/data_4/top_player/W1.npy')
W2 = np.load('gcp_results/checkers-144720/data_4/top_player/W2.npy')
W3 = np.load('gcp_results/checkers-144720/data_4/top_player/W3.npy')
W4 = np.load('gcp_results/checkers-144720/data_4/top_player/W4.npy')
nnet_1 = {'W1': W1,'W2': W2,'W3': W3, 'W4': W4}

W1 = np.load('gcp_results/checkers-144720/data/top_player/W1.npy')
W2 = np.load('gcp_results/checkers-144720/data/top_player/W2.npy')
W3 = np.load('gcp_results/checkers-144720/data/top_player/W3.npy')
W4 = np.load('gcp_results/checkers-144720/data/top_player/W4.npy')
nnet_2 = {'W1': W1,'W2': W2,'W3': W3, 'W4': W4}


print(nnet_2['W4'])
nnets = {1: nnet_2,-1: nnet_1}

checkers=checkers_class()


#result1 = play_game(checkers,nnets,True,4,player1,player2)

