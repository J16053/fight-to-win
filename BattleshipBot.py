import network
import random,time,os

def update(location): #updates probability of everything near guess
	global board
	for n in neighbourhood:
		row = location[0]+n[0]
		col = location[1]+n[1]
		if status([row,col]) != -1:
			board[row][col] = probability([row,col])

def clue(location, area): #appends all locations outside of area to guesses
	global board
	valid = []
	for n in area:
		pos = [location[0]+n[0],location[1]+n[1]]
		if status(pos) != -1:
			valid.append(pos)
	for i in range(size):
		for j in range(size):
			if not [i,j] in valid:
				guesses.append([i,j])
	board = pdensity()

def randomGuess(): #returns guess based on highest probability
	for v in range(8,0,-1): #v for value
		for i in range(size):
			for j in range(size):
				if board[i][j] == v and [i,j] not in hit:
					return str(i)+','+str(j)

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
	for n in neighbours:
		for i in range(1,shipSize):
			pos = [row+i*n[0],col+i*n[1]]
			if status(pos) == 0:
				if pos[0] == row: #if pos is to the left or right of location
					horizontal += 1
				else: #if pos is above or below location
					vertical += 1
			else:
				break
	overlap = shipSize-2
	if vertical < overlap:
		vertical = overlap
	if horizontal < overlap:
		horizontal = overlap
	p = vertical + horizontal - 2*overlap
	return p

name = 'Jacinta'
#name = input ("Please enter your name")

# create boards
dispBoard, size, shipSize, mines = network.createBoards(name, True)
#hidboard, dispBoard, size, shipSize, mines = network.createBoards(name)


neighbours = [[0,-1],[0,1],[-1,0],[1,0]] #left, right, up, down
neighbourhood = [[n[0]*i,n[1]*i] for n in neighbours for i in range(1,shipSize)]
neighbourhood.append([0,0])
hinted = [[i,j] for i in range(-4,5) for j in range(-4,5) if not (abs(i) > 1 and abs(j) > 1)]

board = pdensity()
hit = [] #locations of opponent's ship
guesses = [] #locations that definitely do not contain ship

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
		clue([ans[0],ans[1]], hinted)

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
	#guess = input("Enter your guess: ")
	
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
