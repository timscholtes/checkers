
def intersperse(seq, value):
    res = [value] * (2 * len(seq) - 1)
    res[::2] = seq
    return res


def board_list_viz():
	
	mid_row_even = [".","_"]*4
	mid_row_odd  = ["_","."]*4
	blank_board  = [
	mid_row_even,mid_row_odd,
	mid_row_even,mid_row_odd,
	mid_row_even,mid_row_odd,
	mid_row_even,mid_row_odd,
	mid_row_even,mid_row_odd,
	mid_row_even,mid_row_odd,
	mid_row_even,mid_row_odd,
	mid_row_even,mid_row_odd
	]
	
	return blank_board

#print(board_list_viz())

start_board = [val for sublist in [["1"]*12,["0"]*8,["-1"]*12] for val in sublist]

start_board2 = intersperse(start_board,".")

n = 8


start_board2 = [start_board2[i:i + n] for i in range(0, len(start_board2), n)]
print(start_board2)
