import network
import random,time,os

neighbours = [[0,-1],[0,1],[-1,0],[1,0]]
neighbourhood = [[0,0],[0,-1],[-1,0],[0,1],[1,0],[0,-2],[-2,0],[0,2],[2,0],[0,-3],[-3,0],[0,3],[3,0]]

hint = []
hit = []
guesses = []
shipSize = 4

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

def clue(location, area): #appends all locations outside of area to guesses
	global board
	row = location[0]
	col = location[1]
	valid = []
	for n in area:	#everything in 3*4 area on either side:
		pos = [row+n[0],col+n[1]]
		if status(pos) != -1:
			valid.append(pos)
	for i in range(size):
		for j in range(size):
			if not [i,j] in valid:
				guesses.append([i,j])
	board = pdensity()

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

def probability(location): #returns number of ship orientations possible at location
	if status(location) != 0:
		return 0
	row = location[0]
	col = location[1]
	vertical = 0
	horizontal = 0
	for n in neighbours[:2]:
		for i in range(1,shipSize):
			pos = [row+i*n[0],col+i*n[1]]
			if status(pos) == 0:
				horizontal += 1
			else:
				break
	for n in neighbours[2:]:
		for i in range(1,shipSize):
			pos = [row+i*n[0],col+i*n[1]]
			if status(pos) == 0:
				vertical += 1
			else:
				break
	if vertical < (shipSize-2) and horizontal < (shipSize-2):
		p = 0
	elif vertical < (shipSize-2):
		p = horizontal-(shipSize-2)
	elif horizontal < (shipSize-2):
		p = vertical-(shipSize-2)
	else:
		p = vertical+horizontal-2*(shipSize-2)
	return p

name = 'Jacinta'	#input ("Please enter your name")

# create boards
dispBoard, size, shipSize, mines = network.createBoards(name, True)
# hidboard, dispBoard, size, shipSize, mines = network.createBoards(name)

board = pdensity()

moves = 0

while True:
	################################################################################
	# Opponents time to hit (waiting for opponent hit)
	# - either you will lose
	# - or opponent hit empty location or a ship location
	# - or opponent hit a mine 
	# 	- You get additional info about a nearby location to the opponent's ship
	################################################################################
	ans = network.receive()

	if ans == 'lost':
		break
	elif ans != None:
		ans = list(map(int,ans.split(',')))
		print (ans[0],ans[1], "is nearby location of the ship")
		if len(hit) == 0:
			clue([ans[0],ans[1]], hinted)
		hint.append([ans[0],ans[1]])

	################################################################################
	# Your turn to hit
	# You will get back either ' ', 'x', 'M'
	#
	# need to make your own logic to come up with a string "r,c" to send to opponent
	################################################################################	
	if len(hit) > 0:
		clue(hit[-1], neighbourhood)
		guess = randomGuess()
	else:
		guess = randomGuess()
	
	ans = network.send(guess)
	location = [int(guess[0]),int(guess[-1])]
	guesses.append(location)

	if ans == 'win':
		break
	elif ans == 'wrong input':
		print ("Your input was wrong")
	else:
		# assign result to board
		guessList = list(map(int,guess.split(',')))
		dispBoard[guessList[0]][guessList[1]]=ans
		if ans == 'x':
			hit.append([int(guess[0]),int(guess[-1])])
			guesses.remove(location)
	update(location)

# Printing final result
if ans == 'win':
	guessList = list(map(int,guess.split(',')))
	dispBoard[guessList[0]][guessList[1]]='x'
	network.printBoard()
	print ("you have won the game")
else:
	network.printBoard()
	print ("you have lost the game")
