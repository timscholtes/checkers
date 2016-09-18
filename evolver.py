# evolver
import json
import numpy as np

X = [0,4,2,7,5,2]


def cull(scores,k):
	return np.argsort(scores)[::-1][range(k)]


with open('data/tournament_scores.txt', 'r') as fp:
    data = json.load(fp)

print(np.argsort(X)[::-1][range(3)])
