import numpy as np
import copy 

test = True

# initialize board (inaccessible states are represented with 'X')
grid = [[0, 0, 0, 0],
        [0, 'X', 0, -1],
		[0, 0, 0, 1]]

# specify goal states
goal_states = [(1,3),(2,3)]

# specify hyperparameters
discount = 0.9
R = -0.05
threshold = 0.001

# we're assuming that if a move is not deterministic, there is equal probability of 
# agent moving in the two perpendicular directions
# ie. if the action_probability is 0.8, if we choose to go left, there is 80%
# chance that we go left, 10% chance we go down, and 10% chance we go up
action_probability = 0.8

# outputs the current utility values of the board to stdout
def print_board(grid, it_num):

	print('ITERATION', it_num)
	len_x = len(grid)
	len_y = len(grid[0])
	for row in grid:
		for col in row:
			if col == 'X':
				print(col, end=" ") 
			else:
				print(round(col, 3), end=" ")
		print()
	print()

# checks whether the two grids are similar enough
def meets_criteria(grid1, grid2, threshold):
	len_y = len(grid)
	len_x = len(grid[0])
	
	for i in range(len_y):
		for j in range(len_x):

			if not (i == 1 and j == 1):
				if abs(grid1[i][j] - grid2[i][j]) > threshold:
					return False
	return True

# algorithm that iterates for optimal grid
def find_optimal_grid(grid, discount, R, threshold, goal_states, action_probability, print_intermediary):
	itnum = 0
	perpendicular_probability = (1.000-action_probability)/2.000
	# print_intermediary dictates whether the steps are printed
	if print_intermediary:
		print_board(grid, itnum)
	
	len_y = len(grid)
	len_x = len(grid[0])
	
	# find all inaccessible states
	inaccessible_states = []
	for i in range(len_y):
			for j in range(len_x):
				if grid[i][j] == 'X':
					inaccessible_states.append((i,j))
 
	while True:
		itnum += 1
		old_grid = copy.deepcopy(grid)
		
		# iterate through each cell in grid
		for i in range(len_y):
			for j in range(len_x):
				
				# check if cell is a terminal or inaccessible cell
				if (i,j) in goal_states or (i,j) in inaccessible_states:
					continue
				else:
					
					# iterative equations
					if (i-1,j) in inaccessible_states or (i-1 < 0):
						up_value = old_grid[i][j]
					else:
						up_value = old_grid[i-1][j]
					
					if (i+1,j) in inaccessible_states or (i+1 > 2):
						down_value = old_grid[i][j]
					else:
						down_value = old_grid[i+1][j]
					
					if (i,j+1) in inaccessible_states or (j+1 > 3):
						left_value = old_grid[i][j]
					else:
						left_value = old_grid[i][j+1]
					
					if (i,j-1) in inaccessible_states or (j-1 < 0):
						right_value = old_grid[i][j]
					else:
						right_value = old_grid[i][j-1]
					
					best = max((action_probability*up_value+perpendicular_probability*left_value+perpendicular_probability*right_value), 
										(action_probability*right_value+perpendicular_probability*up_value+perpendicular_probability*down_value), 
										(action_probability*down_value+perpendicular_probability*right_value+perpendicular_probability*left_value),
										(action_probability*left_value+perpendicular_probability*up_value+perpendicular_probability*down_value))

					grid[i][j] = discount * best + R
		if print_intermediary:
			print_board(grid, itnum)
		if meets_criteria(grid, old_grid, threshold):
			break
	
	# print optimal policy
	print('OPTIMAL POLICY')
	for i in range(len_y):
		for j in range(len_x):
			best_move = 'unset'
			best_move_value = float('-inf')

			if (i,j) in goal_states or (i,j) in inaccessible_states:
				pass
			else:
				best_move = []
				if (i==0) or (i-1,j) in inaccessible_states:
					up = grid[i][j]
				else:
					up = grid[i-1][j]
				
				if (i==2) or (i+1,j) in inaccessible_states:
					down = grid[i][j]
				else:
					down = grid[i+1][j]

				if (j==3) or (i,j+1) in inaccessible_states:
					right = grid[i][j]
				else:
					right = grid[i][j+1]
				
				if (j==0) or (i,j-1) in inaccessible_states:
					left = grid[i][j]
				else:
					left = grid[i][j-1]
			
				up_move = action_probability*up+perpendicular_probability*left+perpendicular_probability*right
				if up_move > best_move_value+0.001:
					best_move_value = up_move
					best_move = ['up']
				elif up_move >= best_move_value-0.001:
					best_move.append('up')

				down_move = action_probability*down+perpendicular_probability*left+perpendicular_probability*right
				if down_move > best_move_value+0.001:
					best_move_value = down_move
					best_move = ['down']
				elif down_move >= best_move_value-0.001:
					best_move.append('down')

				right_move = action_probability*right+perpendicular_probability*up+perpendicular_probability*down
				if right_move > best_move_value+0.001:
					best_move_value = right_move
					best_move = ['right']
				elif right_move >= best_move_value-0.001:
					best_move.append('right')

				left_move = action_probability*left+perpendicular_probability*up+perpendicular_probability*down
				if left_move > best_move_value+0.001:
					best_move_value = left_move
					best_move = ['left']
				elif left_move >= best_move_value-0.001:
					best_move.append('left')

			if best_move == 'unset':
				print(grid[i][j], end=' ')
			else:
				for k in range(len(best_move)):
					print(best_move[k], end=' ')
			print('|', end=' ')
		print()

if test:
	find_optimal_grid(grid, discount, R, threshold, goal_states, action_probability, True)