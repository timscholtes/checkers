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
start_board = np.array([val for sublist in [[1]*12,[0]*8,[-1]*12] for val in sublist])

###
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

print('W1',mod1['W1'].shape)
print('W2',mod1['W2'].shape)
print('W3',mod1['W3'].shape)