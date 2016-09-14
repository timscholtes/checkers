import time
import copy

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


forward_move_dict = {value: forward_move_function(value,1) for value in list(range(1,33))}
back_move_dict = {value: forward_move_function(value,-1) for value in list(range(1,33))}
both_move_dict = copy.deepcopy(forward_move_dict)

for key,value in both_move_dict.items():
	[both_move_dict[key]['jump'].append(i) for i in back_move_dict[key]['jump']]
	[both_move_dict[key]['simp'].append(i) for i in back_move_dict[key]['simp']]
	[both_move_dict[key]['mid'].append(i) for i in back_move_dict[key]['mid']]

#for key,value in forward_move_dict.items():
#	print(key,value)
print('forward')
for key,value in forward_move_dict.items():
	print(key,value)

print('back')
for key,value in back_move_dict.items():
	print(key,value)

print('both')
for key,value in both_move_dict.items():
	print(key,value)