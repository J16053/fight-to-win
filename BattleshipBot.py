import network
import random,time,os

neighbours = [[0,-1],[-1,0],[0,1],[1,0]]
diagonals = [[-1,-1],[-1,1],[1,1],[1,-1],[0,0]]
direction = ' '
neighbourhood = [[0,0],[0,-1],[-1,0],[0,1],[1,0],[0,-2],[-2,0],[0,2],[2,0],[0,-3],[-3,0],[0,3],[3,0]]

hint = []
hit = []
guesses = []

hinted = [[i,j] for i in range(-4,5) for j in range(-4,5) if not (abs(i) > 1 and abs(j) > 1)]

def update(location): #updates probability of everything near guess
	global board
	row = location[0]
	col = location[1]
	for n in neighbourhood:
		r = row+n[0]
		c = col+n[1]
		pos = [r,c]
		if status(pos) != -1:
			board[r][c] = probability(pos)

def newHint(location): #changes status of every location not near hint to guessed
	global board
	row = location[0]
	col = location[1]
	valid = []
	for n in hinted:	#everything in 3*4 area on either side:
		pos = [row+n[0],col+n[1]]
		if status(pos) != -1:
			valid.append(pos)
	for i in range(size):
		for j in range(size):
			if not [i,j] in valid:
				guesses.append([i,j])
	board = pdensity()

def kill(location): #changes status of every location not in line with hit to guessed, returns guess
	global board
	row = location[0]
	col = location[1]
	valid = []
	for n in neighbourhood:
		pos = [row+n[0],col+n[1]]
		if status(pos) != -1:
			valid.append(pos)
	for i in range(size):
		for j in range(size):
			if not [i,j] in valid:
				guesses.append([i,j])
	board = pdensity()
	return randomGuess()

def randomGuess(): #returns guess based on highest probability
	mostLikely = []
	for v in range(8,0,-1):
		for i in range(size):
			for j in range(size):
				if board[i][j] == v and [i,j] not in hit:
					s = str(i)+','+str(j)
					mostLikely.append(s)
		if len(mostLikely) > 0:
			break
	return mostLikely[0]

def pdensity(): #populates board with probabilities
	board = []
	for i in range(size):
		temp = []
		for j in range(size):
			p = probability([i,j])
			temp.append(p)
		board.append(temp)
	return board

def status(location): #returns status of location
	if location[0] < 0 or location[0] > size-1 or location[1] < 0 or location[1] > size-1:
		return -1 #out of range
	for g in guesses:
		if g[0] == location[0] and g[1] == location[1]:
			return 1 #empty water
	return 0 #ship could be here

def probability(location): #returns number of ship orientations that could occupy location
	if status(location) != 0:
		return 0 #no ships if already guessed / out of range
	row = location[0]
	col = location[1]
	layer1 = [] #immediately adjacent tiles
	layer2 = [] #two away tiles
	layer3 = [] #three away tiles
	for i in neighbours:
		pos = [row+i[0],col+i[1]]
		if status(pos) == 0:
			layer1.append(i)
	if len(layer1) == 0:
		return 0
	elif len(layer1) == 1:
		if status([row+2*layer1[0][0],col+2*layer1[0][1]]) == 0 \
		and status([row+3*layer1[0][0],col+3*layer1[0][1]]) == 0:
			return 1
		else:
			return 0
	elif len(layer1) == 2:
		if abs(layer1[0][0]) == abs(layer1[1][0]): #opposite
			if status([row+2*layer1[0][0],col+2*layer1[0][1]]) == 0 \
			and status([row+2*layer1[1][0],col+2*layer1[1][1]]) == 0: #len(layer2) == 2
				if status([row+3*layer1[0][0],col+3*layer1[0][1]]) == 0 \
				and status([row+3*layer1[1][0],col+3*layer1[1][1]]) == 0: #len(layer3) == 2
					return 4
				elif status([row+3*layer1[0][0],col+3*layer1[0][1]]) == 0 \
				or status([row+3*layer1[1][0],col+3*layer1[1][1]]) == 0: #len(layer3) == 1
					return 3
				else: #len(layer3) == 0:
					return 2
			elif status([row+2*layer1[0][0],col+2*layer1[0][1]]) == 0 \
			or status([row+2*layer1[1][0],col+2*layer1[1][1]]) == 0: #len(layer2) == 1
				if status([row+3*layer1[1][0],col+3*layer1[1][1]]) == 0:
					return 2
				else: #len(layer3) == 0:
					return 1
			else: #len(layer3) == 0:
				return 0
		else: #adjacent
			if status([row+2*layer1[0][0],col+2*layer1[0][1]]) == 0 \
			and status([row+2*layer1[1][0],col+2*layer1[1][1]]) == 0: #len(layer2) == 2
				if status([row+3*layer1[0][0],col+3*layer1[0][1]]) == 0 \
				and status([row+3*layer1[1][0],col+3*layer1[1][1]]) == 0: #len(layer3) == 2
					return 2
				elif status([row+3*layer1[0][0],col+3*layer1[0][1]]) == 0 \
				or status([row+3*layer1[1][0],col+3*layer1[1][1]]) == 0: #len(layer3) == 1
					return 1
				else: #len(layer3) == 0:
					return 0
			elif status([row+2*layer1[0][0],col+2*layer1[0][1]]) == 0 \
			or status([row+2*layer1[1][0],col+2*layer1[1][1]]) == 0: #len(layer2) == 1
				if status([row+3*layer1[1][0],col+3*layer1[1][1]]) == 0:
					return 1
				else: #len(layer3) == 0:
					return 0
			else: #len(layer3) == 0:
				return 0
	elif len(layer1) == 3:
		for i in layer1:
			pos = [row+2*i[0],col+2*i[1]]
			if status(pos) == 0:
				layer2.append(i)
		if len(layer2) == 0:
			return 0
		elif len(layer2) == 1:
			blocked = [x for x in layer1 if x not in layer2]
			if abs(blocked[0][0]) == abs(blocked[1][0]): #opposite
				if status([row+3*layer2[0][0],col+3*layer2[0][1]]): #len(layer3) == 1
					return 1
				else: #len(layer3) == 0:
					return 0
			else: #adjacent
				if status([row+3*layer2[0][0],col+3*layer2[0][1]]): #len(layer3) == 1
					return 2
				else: #len(layer3) == 0:
					return 1
		elif len(layer2) == 2:
			if abs(layer2[0][0]) == abs(layer2[1][0]): #opposite
				if status([row+3*layer2[0][0],col+3*layer2[0][1]]) == 0 \
				and status([row+3*layer2[1][0],col+3*layer2[1][1]]) == 0: #len(layer3) == 2
					return 4
				elif status([row+3*layer2[0][0],col+3*layer2[0][1]]) == 0 \
				or status([row+3*layer2[1][0],col+3*layer2[1][1]]) == 0: #len(layer3) == 1
					return 3
				else: #len(layer3) == 0:
					return 2
			else: #adjacent
				if status([row+3*layer2[0][0],col+3*layer2[0][1]]) == 0 \
				and status([row+3*layer2[1][0],col+3*layer2[1][1]]) == 0: #len(layer3) == 2
					return 3
				elif status([row+3*layer2[0][0],col+3*layer2[0][1]]) == 0 \
				or status([row+3*layer2[1][0],col+3*layer2[1][1]]) == 0: #len(layer3) == 1
					return 2
				else: #len(layer3) == 0:
					return 1
		else: # len(layer2) == 3:
			for i in layer2:
				pos = [row+3*i[0],col+3*i[1]]
				if status(pos) == 0:
					layer3.append(i)
			if len(layer3) == 0:
				return 1
			elif len(layer3) == 1:
				blocked = [x for x in layer2 if x not in layer3]
				if abs(blocked[0][0]) == abs(blocked[1][0]): #opposite
					return 3
				else: #adjacent
					return 2
			elif len(layer3) == 2:
				return 4
			else: # len(layer3) == 3:
				return 5
	else: #len(layer1) == 4:
		for i in layer1:
			pos = [row+2*i[0],col+2*i[1]]
			if status(pos) == 0:
				layer2.append(i)
		if len(layer2) == 0:
			return 0
		elif len(layer2) == 1:
			if status([row+3*layer2[0][0],col+3*layer2[0][1]]) == 0:
				return 1
			else:
				return 0
		elif len(layer2) == 2:
			if status([row+3*layer2[0][0],col+3*layer2[0][1]]) == 0 \
			and status([row+3*layer2[1][0],col+3*layer2[1][1]]) == 0: #len(layer3) == 2
				return 4
			elif status([row+3*layer2[0][0],col+3*layer2[0][1]]) == 0 \
			or status([row+3*layer2[1][0],col+3*layer2[1][1]]) == 0: #len(layer3) == 1
				return 3
			else: #len(layer3) == 0:
				return 2
		elif len(layer2) == 3:
			for i in layer2:
				pos = [row+3*i[0],col+3*i[1]]
				if status(pos) == 0:
					layer3.append(i)
			if len(layer3) == 0:
				return 3
			elif len(layer3) == 1:
				return 4
			elif len(layer3) == 2:
				if abs(layer2[0][0]) == abs(layer2[1][0]): #opposite
					return 5
				else: #adjacent
					return 4
			else: #len(layer3) == 3:
				return 6
		else: #len(layer3) == 4:
			for i in layer2:
				pos = [row+3*i[0],col+3*i[1]]
				if status(pos) == 0:
					layer3.append(i)
			if len(layer3) == 0:
				return 4
			elif len(layer3) == 1:
				return 5
			elif len(layer3) == 2:
				return 6
			elif len(layer3) == 3:
				return 7
			else: #len(layer3)==4:
				return 8
	return -1

name = 'Jacinta'	#input ("Please enter your name")

# create boards
dispBoard, size, shipSize, mines = network.createBoards(name, True)
# hidboard, dispBoard, size, shipSize, mines = network.createBoards(name)

board = pdensity()
turns = 0

while True:
	################################################################################
	# Opponents time to hit (waiting for opponent hit)
	# - either you will lose
	# - or opponent hit empty location or a ship location
	# - or opponent hit a mine 
	# 	- You get additional info about a nearby location to the opponent's ship
	################################################################################
	ans = network.receive()

	#if ans == 'lost':
		#break
	#elif ans != None:
	if ans != None and ans != 'lost':
		ans = list(map(int,ans.split(',')))
		print (ans[0],ans[1], "is nearby location of the ship")
		if len(hit) == 0:
			newHint([ans[0],ans[1]])
		hint.append([ans[0],ans[1]])

	################################################################################
	# Your turn to hit
	# You will get back either ' ', 'x', 'M'
	#
	# need to make your own logic to come up with a string "r,c" to send to opponent
	################################################################################	
	if len(hit) > 0:
		guess = kill(hit[-1])
	else:
		guess = randomGuess()
	
	ans = network.send(guess)
	location = [int(guess[0]),int(guess[-1])]
	guesses.append(location)
	turns += 1

	if ans == 'win':
		break
	elif ans == 'wrong input':
		print ("Your input was wrong")
		print(guess)
		printBoard(board)
		time.sleep(10)
	else:
		# assign result to board
		guessList = list(map(int,guess.split(',')))
		dispBoard[guessList[0]][guessList[1]]=ans
		if ans == 'x':
			hit.append([int(guess[0]),int(guess[-1])])
			guesses.remove(location)
	update(location)
			
file = open('score.txt','a')
record = open('moves.txt','a')

# Printing final result
if ans == 'win':
	guessList = list(map(int,guess.split(',')))
	dispBoard[guessList[0]][guessList[1]]='x'
	network.printBoard()
	print ("you have won the game")
	record.write(str(turns)+'\n')
	file.write('1')
else:
	network.printBoard()
	print ("you have lost the game")
	file.write('0')

file.close()
record.close()

def printBoard(board): #matrix formatting for debugging purposes
	for i in board:
		for j in i:
			print(j, end=' ')
		print('\n')
